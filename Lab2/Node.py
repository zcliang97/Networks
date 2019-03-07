from ExponentialRandomVariableGenerator import ExponentialRandomVariableGenerator
from Packet import Packet
from Event import Event
from collections import deque
import random

COLLISION_LIMIT = 10
TRANSMISSION_RATE = 1000000 # 1 Mbps

class Node:
    def __init__(self, position, arrivalTimeLambda, simulationTime):
        self.queue = deque()
        self.position = position
        self.arrivalTimeLambda = arrivalTimeLambda
        self.simulationTime = simulationTime
        self.collision_counter = 0
        self.genPacketArrivalEvents()
        
    def genPacketArrivalEvents(self):
        # create Arrival Time generator
        arrivalTimeGenerator = ExponentialRandomVariableGenerator(lmbda=self.arrivalTimeLambda)

        # create arrival events for the simulation
        currentTime = 0
        while currentTime < self.simulationTime:
            # add inter-arrival time to arrive at current timestamp
            interArrivalTime = arrivalTimeGenerator.genValue()
            currentTime += interArrivalTime

            # add arrival event to queue
            self.queue.append(Event("Arrival", currentTime))

    def checkCollision(self, firstBitArrivalTime):
        if self.queue and (self.queue[0].timestamp < firstBitArrivalTime):
            return True
        return False

    def waitExponentialBackoff(self, collisionTime):
        if not self.queue:
            return

        self.collision_counter += 1
        if self.collision_counter > COLLISION_LIMIT:
            # print("Collision Counter exceeded Limit")
            self.removeFirstPacket()
        else: 
            # Start backoff when collision occurs. Collison occurs when first bit arrives
            # and all nodes are notified at the same time
            newArrivalTime = collisionTime + self.genExponentialBackoffTime()
            for packet in self.queue:
                if packet.timestamp > newArrivalTime:
                    break
                elif packet.timestamp <= newArrivalTime: 
                    packet.timestamp = newArrivalTime

    def processNoCollision(self, firstBitArrivalTime, lastBitArrivalTime):
        for packet in self.queue:
            if packet.timestamp > lastBitArrivalTime:
                break
            elif packet.timestamp < firstBitArrivalTime:
                raise Exception('There should not be any prev transmitted nodes when no collisons occur')
            else:
                packet.timestamp = lastBitArrivalTime

    def genExponentialBackoffTime(self):
        # generate a random number between 0 and 2^i-1
        R = random.randint(0, 2**self.collision_counter)
        # random number * 512 bit-time
        backoff = R * 512 * (1 / TRANSMISSION_RATE)
        return backoff

    def removeFirstPacket(self):
        self.queue.popleft()
        self.collision_counter = 0;

    def getFirstPacketTimestamp(self):
        if self.queue:
            return self.queue[0].timestamp
        else:
            return float('inf')

    def getNodePosition(self):
        return self.position
