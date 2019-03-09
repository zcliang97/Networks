from __future__ import division
from ExponentialRandomVariableGenerator import ExponentialRandomVariableGenerator
from Packet import Packet
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
        self.collision_counter_medium = 0
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

            # add packet to queue
            self.queue.append(Packet(currentTime))

    # Checks if next packet is during a transmission. If next packet
    # Arrives before the sender's first bit arrives, bus appears to be idle
    def checkIfBusy(self, firstBitArrivalTime, lastBitArrivaltime):
        return firstBitArrivalTime < self.getFirstPacketTimestamp() and self.getFirstPacketTimestamp() < lastBitArrivaltime

    # If packet arrival < arrival of transmitted first bit, bus appears to be idle
    def checkCollision(self, firstBitArrivalTime):
        return self.getFirstPacketTimestamp() <= firstBitArrivalTime

    def waitExponentialBackoff(self):
        self.collision_counter += 1
        if self.collision_counter > COLLISION_LIMIT:
            self.removeFirstPacket()
        else: 
            # Each node waits backoff time. Means we start waiting from our first packet time
            newArrivalTime = self.getFirstPacketTimestamp() + self.genExponentialBackoffTime()
            self.bufferPackets(0, newArrivalTime)

    def waitExponentialBackoffMediumSensing(self, lowerLimit, upperLimit):
        if self.getFirstPacketTimestamp >= lowerLimit and self.getFirstPacketTimestamp <= upperLimit:
            self.collision_counter_medium += 1
            if self.collision_counter_medium > COLLISION_LIMIT:
                self.collision_counter_medium = 0
            else:
                newArrivalTime = self.getFirstPacketTimestamp() + self.genExponentialBackoffTime()
                self.bufferPackets(0, newArrivalTime)

    # Pushes packet timestamps to an upper limit given a range
    def bufferPackets(self, lowerLimit, upperLimit):
        for packet in self.queue:
            if packet.timestamp >= lowerLimit and packet.timestamp <= upperLimit:
                packet.timestamp = upperLimit
            elif packet.timestamp > upperLimit:
                break

    def genExponentialBackoffTime(self):
        # generate a random number between 0 and 2^i-1
        R = random.randint(0, (2**self.collision_counter) - 1)
        # random number * 512 bit-time
        backoff = R * 512 * (1.0 / TRANSMISSION_RATE)
        return backoff

    def removeFirstPacket(self):
        self.queue.popleft()
        self.collision_counter = 0

    def getFirstPacketTimestamp(self):
        if self.queue:
            return self.queue[0].timestamp
        else:
            return float('inf')

    def getNodePosition(self):
        return self.position
