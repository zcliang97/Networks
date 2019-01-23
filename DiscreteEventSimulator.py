from __future__ import division
from Event import Event
from ExponentialRandomVariableGenerator import ExponentialRandomVariableGenerator
from Packet import Packet

AVERAGE_PACKET_LENGTH = 2000
SIMULATION_TIME = 1000
TRANSMISSION_RATE = 1000000 # 1 Mbps

class DiscreteEventSimulator:
    queue = []

    # Counters for metrics
    arrival_count = 0
    departure_count = 0
    observer_count = 0
    idle_count = 0
    packet_sum = 0

    # Metrics
    proportion_idle = 0
    average_packets_in_queue = 0

    def __init__(self, rho):
        self.events = []
        self.packets = []
        self.rho = rho

    def run(self):
        self.genEventsAndPackets()
        self.processEvents()
        self.printResults()

    def genEventsAndPackets(self):
        arrival_time_lambda = self.rho * TRANSMISSION_RATE / AVERAGE_PACKET_LENGTH
        packet_length_lambda = 1.0 / AVERAGE_PACKET_LENGTH
        observer_time_lambda = 5 * arrival_time_lambda

        # Exponential Random Variable Generators
        arrivalTimeGenerator = ExponentialRandomVariableGenerator(lmbda=arrival_time_lambda)
        packetLengthGenerator = ExponentialRandomVariableGenerator(lmbda=packet_length_lambda)
        observationTimeGenerator = ExponentialRandomVariableGenerator(lmbda=observer_time_lambda)

        currentTime = 0
        prevDepartureTime = 0
        # Generate Arrival, and if M/M/1, generate Departure
        while currentTime < SIMULATION_TIME:
            # Add inter-arrival time to arrive at current timestamp
            interArrivalTime = arrivalTimeGenerator.genValue()
            currentTime += interArrivalTime

            # Generate packet and its length
            packet = Packet(length=packetLengthGenerator.genValue())

            # Generate its departure time based on queue status
            departureTime = 0
            transmissionTime = packet.getTransmissionTime();
            if currentTime < prevDepartureTime:
                departureTime = prevDepartureTime + transmissionTime
            else:
                departureTime = currentTime + transmissionTime
            
            # Add to events and packets if time is valid
            if (departureTime < SIMULATION_TIME):
                self.packets.append(packet)
                self.events.append(Event("Arrival", currentTime))
                self.events.append(Event("Departure", departureTime))
            
            prevDepartureTime = departureTime

        # Generate Observer Events
        currentTime = 0
        while currentTime < SIMULATION_TIME:
            interArrivalTime = observationTimeGenerator.genValue()
            currentTime += interArrivalTime
            if (currentTime < SIMULATION_TIME):
                self.events.append(Event("Observer", currentTime))

        # Sort Events
        self.events.sort(key=lambda event: event.timestamp)


    def processEvents(self):
        for event in self.events:
            if event.event_type == "Arrival":
                self.processArrival()
            elif event.event_type == "Departure":
                self.processDeparture()
            elif event.event_type == "Observer":
                self.processObserver()

    def processArrival(self):
        packet = self.packets.pop(0)
        self.queue.append(packet)
        self.arrival_count += 1

    def processDeparture(self):
        self.queue.pop(0)
        self.departure_count += 1

    def processObserver(self):
        self.observer_count += 1
        if len(self.queue) <= 0:
            self.idle_count += 1

        self.packet_sum += len(self.queue)
        self.average_packets_in_queue = self.packet_sum / self.observer_count
        self.proportion_idle = self.idle_count / self.observer_count

    def printResults(self):
        print("Counts", self.arrival_count, self.departure_count, self.observer_count)
        print("Average Packets In Queue ", self.average_packets_in_queue)
        print("Idle Proportion ", self.proportion_idle)





