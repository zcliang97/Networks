from Event import Event
from ExponentialRandomVariableGenerator import ExponentialRandomVariableGenerator
from Packet import Packet

AVERAGE_PACKET_LENGTH = 2000
SIMULATION_TIME = 1000
TRANSMISSION_RATE = 1000000 # 1 Mbps

class DiscreteEventBufferSimulator:
    def __init__(self, rho, buffer_length):
        self.events = []
        self.departures = []
        self.packets = []
        self.buffer = []
        self.rho = rho
        self.buffer_length = buffer_length

        # Counters for metrics
        self.arrival_count = 0
        self.departure_count = 0
        self.observer_count = 0
        self.idle_count = 0
        self.packet_sum = 0
        self.packet_loss_count = 0

        # Metrics
        self.proportion_idle = 0
        self.packet_loss = 0
        self.average_packets_in_queue = 0

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
            self.packets.append(packet)
            self.events.append(Event("Arrival", currentTime))
            
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
            if len(self.departures) > 0 and event.timestamp >= self.departures[0].timestamp:
                self.processDeparture()
            elif event.event_type == "Arrival":
                self.processArrival(event.timestamp)
            elif event.event_type == "Observer":
                self.processObserver()

    def processArrival(self, timestamp):
        packet = self.packets.pop(0)
        if len(self.buffer) < self.buffer_length:
            # Generate its departure time based on queue status
            departureTime = packet.getTransmissionTime() + timestamp
            self.departures.append(Event("Departure", departureTime))

            self.buffer.append(packet)
            self.arrival_count += 1
        else:
            self.packet_loss_count += 1

    def processDeparture(self):
        self.buffer.pop(0)
        self.departures.pop(0)
        self.departure_count += 1

    def processObserver(self):
        self.observer_count += 1
        if len(self.buffer) <= 0:
            self.idle_count += 1

        self.packet_sum += len(self.buffer)
        self.average_packets_in_queue = float(self.packet_sum) / self.observer_count
        self.proportion_idle = float(self.idle_count) / self.observer_count
        self.packet_loss = float(self.packet_loss_count) / self.observer_count

    def printResults(self):
        print("Counts", self.arrival_count, self.departure_count, self.observer_count)
        print("Average Packets In Queue ", self.average_packets_in_queue)
        print("Idle Proportion ", self.proportion_idle)
        print("Probability of Packet Loss ", self.packet_loss)