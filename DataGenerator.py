import numpy as np
import math

class Packet:
    def __init__(self, bit_length):
        self.bit_length = bit_length
    
    def getServiceTime(self, transmission_rate):
        return self.bit_length / transmission_rate

class Event:
    def __init__(self, packet_type, timestamp):
        self.packet_type = packet_type
        self.timestamp = timestamp

class DataGenerator:
    def __init__(self, lmbda, num_variables):
        # input uniform distribution
        self.lmbda = lmbda
        self.num_variables = num_variables
        self.exponentialRandomVariables = self.genExponentialRandomVariable(self.lmbda)

    # out   -> output exponential distribution
    def genExponentialRandomVariable(self, lmbda):
        uniform_random_variable = np.random.uniform(0, 1, self.num_variables)
        return map(lambda x: ((-1.0/lmbda) * math.log(1.0-x)), uniform_random_variable)

    # E[x] = 1/lambda
    def getTheoreticalExpectedValue(self):
        return 1.0/self.lmbda

    def getMeasuredExpectedValue(self):
        return np.mean(self.exponentialRandomVariables)

    # Var[X] = 1/ (lambda)^2
    def getTheoreticalVariance(self):
        return 1.0/(self.lmbda * self.lmbda)

    def getMeasuredVariance(self):
        return np.var(self.exponentialRandomVariables)

    # run through process
    def run(self):
        print 'Theoretical Expected Value: \t\t' + str(self.getTheoreticalExpectedValue())
        print 'Measured Expected Value: \t\t' + str(self.getMeasuredExpectedValue())
        print 'Theoretical Variance: \t\t\t' + str(self.getTheoreticalVariance())
        print 'Measured Variance: \t\t\t' + str(self.getMeasuredVariance())