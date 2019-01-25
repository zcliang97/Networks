from __future__ import division
from collections import deque
from Event import Event
from ExponentialRandomVariableGenerator import ExponentialRandomVariableGenerator
from Packet import Packet

AVERAGE_PACKET_LENGTH = 2000
SIMULATION_TIME = 1000
TRANSMISSION_RATE = 1000000 # 1 Mbps

class DiscreteEventBufferSimulator:
    def __init__(self, rho, buffer_length):
        self.events = []
        self.departures = deque() 
        self.packets = deque()
        self.buffer = deque()
        self.rho = rho
        self.buffer_length = buffer_length

        # Counters for metrics
        self.arrival_count = 0
        self.departure_count = 0
        self.observer_count = 0
        self.idle_count = 0
        self.packet_sum = 0
        self.packet_loss_count = 0
        self.prevDepartureTime = 0

        # Metrics
        self.proportion_idle = 0
        self.packet_loss = 0
        self.average_packets_in_queue = 0

    def run(self):
        self.genEventsAndPackets()
        self.processEvents()
        self.printResults()
        return self.average_packets_in_queue

    def genEventsAndPackets(self):
        arrival_time_lambda = self.rho * TRANSMISSION_RATE / AVERAGE_PACKET_LENGTH
        packet_length_lambda = 1.0 / AVERAGE_PACKET_LENGTH
        observer_time_lambda = 5 * arrival_time_lambda

        # Exponential Random Variable Generators
        arrivalTimeGenerator = ExponentialRandomVariableGenerator(lmbda=arrival_time_lambda)
        packetLengthGenerator = ExponentialRandomVariableGenerator(lmbda=packet_length_lambda)
        observationTimeGenerator = ExponentialRandomVariableGenerator(lmbda=observer_time_lambda)

        currentTime = 0
        # Generate Arrival, and if M/M/1, generate Departure
        while currentTime < SIMULATION_TIME:
            # Add inter-arrival time to arrive at current timestamp
            interArrivalTime = arrivalTimeGenerator.genValue()
            currentTime += interArrivalTime

            # Generate packet and its length
            packet = Packet(length=packetLengthGenerator.genValue())
            self.packets.append(packet)
            self.events.append(Event("Arrival", currentTime))
            
        # Generate Observer Events
        currentTime = 0
        while currentTime < SIMULATION_TIME:
            interArrivalTime = observationTimeGenerator.genValue()
            currentTime += interArrivalTime
            self.events.append(Event("Observer", currentTime))

        # Sort Events
        self.events.sort(key=lambda event: event.timestamp)
        self.events = deque(self.events)

    def processEvents(self):
        while self.events or self.departures:
            if self.departures:
                eventsTime = self.events[0].timestamp
                departureTime = self.departures[0].timestamp
                if eventsTime > departureTime:
                    event = self.departures.popleft()
                else:
                    event = self.events.popleft()
            else:
                event = self.events.popleft()

            if event.event_type == "Arrival":
                self.processArrival(event.timestamp)
            elif event.event_type == "Departure":
                self.processDeparture()
            elif event.event_type == "Observer":
                self.processObserver()

    def processArrival(self, timestamp):
        packet = self.packets.popleft()
        self.arrival_count += 1
        if len(self.buffer) < self.buffer_length:
            # Generate its departure time based on queue status
            transmissionTime = packet.getTransmissionTime()
            if timestamp < self.prevDepartureTime:
                departureTime = self.prevDepartureTime + transmissionTime
            else:
                departureTime = timestamp + transmissionTime

            if departureTime < SIMULATION_TIME:
                self.prevDepartureTime = departureTime
                self.departures.append(Event("Departure", departureTime))

            self.buffer.append(packet)
        else:
            self.packet_loss_count += 1

    def processDeparture(self):
        self.buffer.popleft()
        self.departure_count += 1

    def processObserver(self):
        self.observer_count += 1
        if not self.buffer:
            self.idle_count += 1
        
        buffer_size = len(self.buffer)
        self.packet_sum += buffer_size
        self.average_packets_in_queue = self.packet_sum / self.observer_count
        self.proportion_idle = self.idle_count / self.observer_count
        self.packet_loss = self.packet_loss_count / (1 + self.arrival_count)

    def printResults(self):
        print("Counts", self.arrival_count, self.departure_count, self.observer_count)
        print("Average Packets In Queue ", self.average_packets_in_queue)
        print("Idle Proportion ", self.proportion_idle)
        print("Probability of Packet Loss ", self.packet_loss)
