from __future__ import division
from Node import Node

SIMULATION_TIME = 1000 # 1000s

TRANSMISSION_RATE = 1000000 # 1 Mbps
PACKET_LENGTH = 1500 # assume all packets are the same length
TRANSMISSION_DELAY = PACKET_LENGTH / TRANSMISSION_RATE

DISTANCE_BETWEEN_NODES = 10
PROPAGATION_SPEED = (2/3) * 300000000
UNIT_PROPAGATION_DELAY = DISTANCE_BETWEEN_NODES / PROPAGATION_SPEED

class PersistentCSMASimulator:
    def __init__(self, numNodes, avgPacketArrivalRate):
        self.nodes = []

        self.numNodes = numNodes
        self.avgPacketArrivalRate = avgPacketArrivalRate

        # metrics
        self.transmittedPackets = 0
        self.successfullyTransmittedPackets = 0

    def run(self):
        self.createNodes()
        self.processPackets()
        self.printResults()

    def createNodes(self):
        for i in range(self.numNodes):
            self.nodes.append(Node(i, self.avgPacketArrivalRate, SIMULATION_TIME))

    def bufferAllPacketsForBusy(self, currentTime, txNode):
        # We know for a fact the transmisison will succeed. The bus will be in use
        # for worst case, transmitting to the farthest node. Nodes should be
        # Buffered for the worst case to avoid collision
        maxOffset = abs(self.numNodes - txNode.getNodePosition())
        propagationDelay = maxOffset * UNIT_PROPAGATION_DELAY;
        for node in self.nodes:
            firstBitArrivalTime = currentTime + propagationDelay
            lastBitArrivalTime = firstBitArrivalTime + TRANSMISSION_DELAY
            node.bufferPackets(firstBitArrivalTime, lastBitArrivalTime)

    def processPackets(self):
        while True:
            # get the sender node which has the smallest packet arrival time
            txNode = min(self.nodes, key=lambda node: node.getFirstPacketTimestamp())
            if not txNode.queue:
                break

            # update the currentTime
            currentTime = txNode.getFirstPacketTimestamp()

            # A packet is trying to be sent
            self.transmittedPackets += 1

            # For each node, calculate when the packet arrives + check collision
            transmissionSuccess = True
            for rxNode in self.nodes:
                offset = abs(rxNode.getNodePosition() - txNode.getNodePosition())
                if (offset == 0):
                    continue;
                
                propagationDelay = offset * UNIT_PROPAGATION_DELAY;
                firstBitArrivalTime = currentTime + propagationDelay
                lastBitArrivalTime = firstBitArrivalTime + TRANSMISSION_DELAY

                if rxNode.checkCollision(firstBitArrivalTime):
                    rxNode.waitExponentialBackoff()
                    self.transmittedPackets += 1
                    transmissionSuccess = False

            if not transmissionSuccess:
                txNode.waitExponentialBackoff()
            else:
                self.successfullyTransmittedPackets += 1
                txNode.removeFirstPacket()
                self.bufferAllPacketsForBusy()

    def printResults(self):
        print("================ RESULTS ================")
        print("Arrival Rate: %f, NumNodes: %f", self.avgPacketArrivalRate, self.numNodes)
        print("SuccessFully Transmitted Packets: {}".format(self.successfullyTransmittedPackets))
        print("Total Transmitted Packets: {}".format(self.transmittedPackets))
        print("Efficiency of CSMA/CD: {}".format((self.successfullyTransmittedPackets / self.transmittedPackets)))
        print("Throughput of CSMA/CD: {} Mbps".format(((self.successfullyTransmittedPackets * PACKET_LENGTH / 1000000) / SIMULATION_TIME)))

