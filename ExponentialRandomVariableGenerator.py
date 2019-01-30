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
            