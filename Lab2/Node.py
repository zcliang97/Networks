from ExponentialRandomVariableGenerator import ExponentialRandomVariableGenerator
from Packet import Packet
from Event import Event
import random

TRANSMISSION_RATE = 1000000 # 1 Mbps

class Node:
    def __init__(self, arrivalTimeLambda, simulationTime):
        self.queue = []
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
        
        # Sort Events for processing chronologically
        self.queue.sort(key=lambda event: event.timestamp)

    # update all arrival times less than new timestamp to be the new timestamp
    def collisionDetection(self, firstBitArrivalTime):
        if self.queue[0].timestamp < firstBitArrivalTime:
            # collision occurred
            if self.collision_counter > 10:
                self.queue.pop(0)
                self.collision_counter = 0
            else:
                self.collision_counter += 1
                waitingTime = self.exponentialBackoffTime()
                self.updateTimestamps(waitingTime)
            return True
        else: return False
    
    def broadcast(self, firstBitArrivalTime, lastBitArrivalTime):
        if self.collisionDetection(firstBitArrivalTime):
            return True
        else:
            self.updateTimestamps(lastBitArrivalTime)
            return False

    def updateTimestamps(self, timestamp):
        for event in self.queue:
            if event.timestamp < timestamp: event.timestamp = timestamp
            elif event.timestamp >= timestamp: break

    def exponentialBackoffTime(self):
        R = random.randint(0, 2**self.collision_counter)    # generate a random number between 0 and 2^i-1
        backoff = R * 512 * (1 / TRANSMISSION_RATE)       # random number * 512 bit-time
        return backoff

    def processArrival(self):
        event = self.queue.pop(0)
        self.collision_counter = 0