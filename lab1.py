import numpy as np
import matplotlib.pyplot as plt
from DataGenerator import DataGenerator, Packet, Event

AVERAGE_BIT_LENGTH = 2000
TRANSMISSION_RATE = 1000000
NUM_OF_PACKETS = 1000

ARRIVAL_TIME_LAMBDA = 75
BIT_LENGTH_LAMBDA = 1/AVERAGE_BIT_LENGTH

arrivalTimes = DataGenerator(lmbda=ARRIVAL_TIME_LAMBDA, NUM_OF_PACKETS)
bitLengths = DataGenerator(lmbda=BIT_LENGTH_LAMBDA, NUM_OF_PACKETS)

packets = []
events = []

# Arrival Time
for i in range(NUM_OF_PACKETS):
    events.append(Event("ARRIVAL", arrivalTimes[i]))

# Departure Time
prevDepartureTime = 0
for i in range(NUM_OF_PACKETS):
    
    departureTime = prevDepartureTime + packets[i].getServiceTime(1000000)
    


observation = DataGenerator(lmbda=75*5)
arrival.run()