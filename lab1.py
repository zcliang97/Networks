import numpy as np
from DiscreteEventSimulator import DiscreteEventSimulator
from DiscreteEventBufferSimulator import DiscreteEventBufferSimulator
import time

# question_number = raw_input("Enter Question Number ")
# question_number = int(question_number)

start_time = time.time()
def question_3():
    rho_values = np.arange(0.25, 1.05, 0.1)
    for rho in rho_values:
        print(" --- Rho Value: %s --- " % rho)
        # Run simulator Passing in events and packets
        simulator = DiscreteEventSimulator(rho).run()

def question_4():
    # Run simulator Passing in events and packets
    rho = 1.2
    print(" --- Rho Value: %s --- " % rho)
    simulator = DiscreteEventSimulator(rho).run()

def question_5():
    buffer_lengths = [10, 25, 50]
    rho_range1 = np.arange(0.4, 2, 0.1)
    rho_range2 = np.arange(2, 5, 0.2)
    rho_range3 = np.arange(5, 10, 0.4)
    for length in buffer_lengths:
        for rho in rho_range1:
            print " --- Buffer Length: {length}, Rho Value: {rho} --- ".format(length=length, rho=rho)
            simulator = DiscreteEventBufferSimulator(rho, length).run()
        for rho in rho_range2:
            print " --- Buffer Length: {length}, Rho Value: {rho} --- ".format(length=length, rho=rho)
            simulator = DiscreteEventBufferSimulator(rho, length).run()
        for rho in rho_range3:
            print " --- Buffer Length: {length}, Rho Value: {rho} --- ".format(length=length, rho=rho)
            simulator = DiscreteEventBufferSimulator(rho, length).run()
        print("--- %s seconds to run range ---" % (time.time() - start_time))

question_5()