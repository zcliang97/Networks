import numpy as np
import time

from PersistentCSMASimulator import PersistentCSMASimulator
from NonpersistentCSMASimulator import NonpersistentCSMASimulator
from ExponentialRandomVariableGenerator import ExponentialRandomVariableGenerator

def question_1():
    for A in [7, 10, 20]:
        for N in [20, 40, 60, 80, 100]:
            simulator = PersistentCSMASimulator(N, 20).run()

def question_2():
    for A in [7, 10, 20]:
        for N in [20, 40, 60, 80, 100]:
            simulator = NonpersistentCSMASimulator(N, 7).run()

# main
question_number = raw_input("Enter Question Number [1, 2] ")
question_number = int(question_number)

start_time = time.time()

if question_number == 1:P
    question_1()
elif question_number == 2:
    question_2()