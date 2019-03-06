import numpy as np
import time

from DiscreteEventSimulator import DiscreteEventSimulator
from DiscreteEventBufferSimulator import DiscreteEventBufferSimulator
from ExponentialRandomVariableGenerator import ExponentialRandomVariableGenerator

def generateGraph(lines, p_loss):
    # for (x, y) in lines:
    #     plt.plot(x, y)
    # plt.show()
    print lines
    print p_loss

def question_1():
    generator_lambda = 75
    generator = ExponentialRandomVariableGenerator(lmbda=generator_lambda)

    exponentialRandomVariables = []
    # Generate 1000 Exponential Random Variables
    for i in range(0, 999):
        exponentialRandomVariables.append(generator.genValue())

    # Compute Theoretical and Experimental Expected Value
    theoretical_expected_value =  1.0 / generator_lambda
    experimental_expected_value = np.mean(exponentialRandomVariables)
    
    # Compute Theoretical and Experimental Variance
    theoretical_variance = 1.0/(generator_lambda * generator_lambda)
    experimental_variance = np.var(exponentialRandomVariables)

    print("Theoretical Expected Value: %f" % theoretical_expected_value)
    print("Experimental Expected Value: %f" % experimental_expected_value)
    print("Theoretical Variance: %f" % theoretical_variance)
    print("Experimental Variance: %f" % experimental_variance)

def question_3():
    # 0.25 with 0.1 steps up to a max value of 1.05 => 0.25 to 0.95
    rho_values = np.arange(0.25, 1.05, 0.1)
    average_packet = []
    idle_proportions = []
    # Run simulator passing in varied rho
    for rho in rho_values:
        print(" --- Rho Value: %s --- " % rho)
        simulator = DiscreteEventSimulator(rho)
        simulator.run()
        average_packet.append(simulator.getAveragePacketsInQueue())
        idle_proportions.append(simulator.getIdleProportion())

    print("E[N] Values: ", average_packet)
    print("Pidle Values: ", idle_proportions)

def question_4():
    rho = 1.2
    print(" --- Rho Value: %s --- " % rho)
    simulator = DiscreteEventSimulator(rho).run()

def question_6():
    lines = []
    packet_loss = []
    buffer_lengths = [10, 25, 50]
    rho_values = np.arange(0.5, 1.6, 0.1)
    for length in buffer_lengths:
        x, y, ploss = [], [], []
        for rho in rho_values:
            print " --- Buffer Length: {length}, Rho Value: {rho} --- ".format(length=length, rho=rho)
            avgPacketsInQueue, packetLoss = DiscreteEventBufferSimulator(rho, length).run()
            print("--- %s seconds to run range ---" % (time.time() - start_time))
            x.append(rho)
            y.append(avgPacketsInQueue)
	    ploss.append(packetLoss)
        lines.append((x, y))
        packet_loss.append(ploss)
    
    generateGraph(lines, packet_loss)

# main
question_number = raw_input("Enter Question Number [1, 3, 4, 6] ")
question_number = int(question_number)

start_time = time.time()

if question_number == 1:
    question_1()
elif question_number == 3:
    question_3()
elif question_number == 4:
    question_4()
elif question_number == 6:
    question_6()
