from __future__ import division
from Node import Node

SIMULATION_TIME = 1000

TRANSMISSION_RATE = 1000000 # 1 Mbps
AVERAGE_PACKET_LENGTH = 1500 # assume all packets are the same length
TRANSMISSION_DELAY = AVERAGE_PACKET_LENGTH / TRANSMISSION_RATE

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
            self.nodes.append(Node(i, self.avgPacketArrivalRate, SIMULATION_TIME))

    def applyCarrierSensing(self, currentTime, txNode):
        # Include transmitting node so that it's next packet also views bus as busy
        for node in self.nodes:
            offset = abs(node.getNodePosition() - txNode.getNodePosition())

            propagationDelay = offset * UNIT_PROPAGATION_DELAY;
            firstBitArrivalTime = currentTime + propagationDelay
            lastBitArrivalTime = firstBitArrivalTime + TRANSMISSION_DELAY
            node.processNoCollision(firstBitArrivalTime, lastBitArrivalTime)

    def processEvents(self):
        currentTime = 0
        while currentTime < SIMULATION_TIME:
            # get the sender node which has the smallest packet arrival time
            txNode = min(self.nodes, key=lambda node: node.getFirstPacketTimestamp())

            # update the currentTime
            currentTime = txNode.getFirstPacketTimestamp()

            # Sender tries to send packet
            self.transmittedPackets += 1

            # For each node, calculate when the packet arrives + check collision
            transferSuccessful = True
            firstCollisionTime = float('inf')
            collisionInvolvedNodes = []
            for rxNode in self.nodes:
                offset = abs(rxNode.getNodePosition() - txNode.getNodePosition())
                if (offset == 0):
                    continue;
                
                propagationDelay = offset * UNIT_PROPAGATION_DELAY;
                firstBitArrivalTime = currentTime + propagationDelay

                collisionDetected = rxNode.checkCollision(firstBitArrivalTime)
                if collisionDetected:
                    firstCollisionTime = min(firstCollisionTime, firstBitArrivalTime)
                    collisionInvolvedNodes.append(rxNode)

            if collisionInvolvedNodes:
                txNode.waitExponentialBackoff(firstCollisionTime)
                for node in collisionInvolvedNodes:
                    self.transmittedPackets += 1
                    node.waitExponentialBackoff(firstCollisionTime)
            else:
                self.successfullyTransmittedPackets += 1
                txNode.removeFirstPacket()
                self.applyCarrierSensing(currentTime, txNode)

    def printResults(self):
        print("================ RESULTS ================")
        print("Arrival Rate: %f, NumNodes: %f", self.avgPacketArrivalRate, self.numNodes)
        print("SuccessFully Transmitted Packets: {}".format(self.successfullyTransmittedPackets))
        print("Total Transmitted Packets: {}".format(self.transmittedPackets))
        print("Efficiency of CSMA/CD: {}".format((self.successfullyTransmittedPackets / self.transmittedPackets)))
