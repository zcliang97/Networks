import numpy as np
import math

class ExponentialRandomVariableGenerator:
    def __init__(self, lmbda):
        # input uniform distribution
        self.lmbda = lmbda

    def genValue(self):
        if (self.lmbda > 0):
            uniform_random_variable = np.random.uniform(0, 1)
            return (-1.0/self.lmbda) * math.log(1.0-uniform_random_variable)
        else:
            raise ValueError('Cannot generate exponential distribution with invalid lambda')

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