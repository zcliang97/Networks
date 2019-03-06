from __future__ import division
from Node import Node

SIMULATION_TIME = 1000
TRANSMISSION_RATE = 1000000 # 1 Mbps
AVERAGE_PACKET_LENGTH = 1500 # assume all packets are the same length
TRANSMISSION_DELAY = 1.0 / AVERAGE_PACKET_LENGTH

DISTANCE_BETWEEN_NODES = 10.0
PROPAGATION_SPEED = (2/3) * 300000000
UNIT_PROPAGATION_DELAY = DISTANCE_BETWEEN_NODES / PROPAGATION_SPEED

class DiscreteEventSimulator:

    def __init__(self, numNodes, avgPacketArrivalRate):
        self.nodes = []

        self.numNodes = numNodes
        self.avgPacketArrivalRate = avgPacketArrivalRate

        # metrics
        self.transmittedPackets = 0
        self.successfullyTransmittedPackets = 0

    def run(self):
        self.createNodes()
        self.processEvents()
        self.printResults()

    def createNodes(self):
        for i in range(self.numNodes):
            # lambda is the mean for a Poisson distribution
            # so to get avgPacketArrivalRate lambda, we have to multiply lambda by the avgPacketArrivalRate
            arrivalTimeLambda = self.avgPacketArrivalRate * TRANSMISSION_RATE / AVERAGE_PACKET_LENGTH
            self.nodes.append(Node(arrivalTimeLambda, SIMULATION_TIME))

    def processEvents(self):
        currentTime = 0
        while currentTime < SIMULATION_TIME:
            # get the index of the node with the smallest packet arrival time
            firstEvent = {}
            for i, node in enumerate(self.nodes):
                if node.queue: firstEvent[node.queue[0].timestamp] = i
            if firstEvent: sender_index = firstEvent[min(firstEvent)]
            else: return

            # update the currentTime
            currentTime = self.nodes[sender_index].queue[0].timestamp

            # process arrival
            self.nodes[sender_index].processArrival()

            # broadcast arrival event
            for i, node in enumerate(self.nodes):
                firstBitArrivalTime = currentTime + (UNIT_PROPAGATION_DELAY * abs(i - sender_index))
                lastBitArrivalTime = firstBitArrivalTime + TRANSMISSION_DELAY
                if node.broadcast(firstBitArrivalTime, lastBitArrivalTime):
                    self.transmittedPackets += 1
                else:
                    self.transmittedPackets += 1
                    self.successfullyTransmittedPackets += 1

    def printResults(self):
        print "================ RESULTS ================"
        print "SuccessFully Transmitted Packets: {}".format(self.successfullyTransmittedPackets)
        print "Total Transmitted Packets: {}".format(self.transmittedPackets)
        print "Efficiency of CSMA/CD: {}".format((self.successfullyTransmittedPackets / self.transmittedPackets))