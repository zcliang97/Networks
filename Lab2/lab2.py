import numpy as np
import time

from DiscreteEventSimulator import DiscreteEventSimulator
from ExponentialRandomVariableGenerator import ExponentialRandomVariableGenerator

def question_1():
    # for A in [7, 10, 20]:
    for N in [20, 40, 60, 80, 100]:
        simulator = DiscreteEventSimulator(N, 5).run()

def question_2():
    simulator = DiscreteEventSimulator(4, 1.0).run()

# main
question_number = raw_input("Enter Question Number [1, 2] ")
question_number = int(question_number)

start_time = time.time()

if question_number == 1:
    question_1()
elif question_number == 2:
    question_2()