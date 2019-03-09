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
        maxOffset = abs((self.numNodes - 1) - txNode.getNodePosition())
        maxPropagationDelay = maxOffset * UNIT_PROPAGATION_DELAY
        maxFirstBitArrivalTime = currentTime + maxPropagationDelay
        maxLastBitArrivalTime = maxFirstBitArrivalTime + TRANSMISSION_DELAY        
        for node in self.nodes:
            offset = abs(node.getNodePosition() - txNode.getNodePosition())
            propagationDelay = offset * UNIT_PROPAGATION_DELAY
            firstBitArrivalTime = currentTime + propagationDelay
            node.bufferPackets(firstBitArrivalTime, maxLastBitArrivalTime)

    def processPackets(self):
        while True:
            # get the sender node which has the smallest packet arrival time
            txNode = min(self.nodes, key=lambda node: node.getFirstPacketTimestamp())

            # update the currentTime
            currentTime = txNode.getFirstPacketTimestamp()
            if currentTime > SIMULATION_TIME:
                break

            # A packet is trying to be sent
            self.transmittedPackets += 1

            # For each node, calculate when the packet arrives + check collision
            transmissionSuccess = True
            for rxNode in self.nodes:
                offset = abs(rxNode.getNodePosition() - txNode.getNodePosition())
                if (offset == 0):
                    continue
                
                propagationDelay = offset * UNIT_PROPAGATION_DELAY
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
                self.bufferAllPacketsForBusy(currentTime, txNode)
                txNode.removeFirstPacket()

    def printResults(self):
        print("================ RESULTS ================")
        print("Arrival Rate: {}, NumNodes: {}".format(self.avgPacketArrivalRate, self.numNodes))
        print("SuccessFully Transmitted Packets: {}".format(self.successfullyTransmittedPackets))
        print("Total Transmitted Packets: {}".format(self.transmittedPackets))
        print("Efficiency of CSMA/CD: {}".format((self.successfullyTransmittedPackets / self.transmittedPackets)))
        print("Throughput of CSMA/CD: {} Mbps".format(((self.successfullyTransmittedPackets * PACKET_LENGTH / 1000000) / SIMULATION_TIME)))

