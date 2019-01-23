import numpy as np
from DiscreteEventSimulator import DiscreteEventSimulator
import time

question_number = raw_input("Enter Question Number ")
question_number = int(question_number)

start_time = time.time()
if question_number == 3:
    rho_values = np.arange(0.25, 1.05, 0.1)
    for rho in rho_values:
        print(" --- Rho Value: %s --- " % rho)
        # Run simulator Passing in events and packets
        simulator = DiscreteEventSimulator(rho).run()

elif question_number == 4:
    # Run simulator Passing in events and packets
    rho = 1.2
    print(" --- Rho Value: %s --- " % rho)
    simulator = DiscreteEventSimulator(rho).run()

print("--- %s seconds ---" % (time.time() - start_time))
# DES for M/M/1/K
