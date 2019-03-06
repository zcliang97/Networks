import numpy as np
import time

from DiscreteEventSimulator import DiscreteEventSimulator
from ExponentialRandomVariableGenerator import ExponentialRandomVariableGenerator

def question_1():
    simulator = DiscreteEventSimulator(3, 1.0).run()

def question_2():
    rho = 1.2
    simulator = DiscreteEventSimulator(rho).run()

# main
question_number = raw_input("Enter Question Number [1, 2] ")
question_number = int(question_number)

start_time = time.time()

if question_number == 1:
    question_1()
elif question_number == 2:
    question_2()