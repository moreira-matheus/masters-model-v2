#!python3

import os
import time
import pickle
from simulation import Simulation
from param import Param

N, R, T = 1000, 200, 50
results_folder = '../results/'
output_file = 'preliminary_results.pkl'

#biases = [-0.75, -0.50, -0.25, 0.00, 0.25, 0.50, 0.75]
biases = [i/100. for i in range(-100, 101, 20)]

results = {}

param = Param()
param.size = N
param.negative_tax = False
param.basic_income = False

print('\n---> START.')
start = time.time()

for bias in biases:
	print(f'\n\t> Bias: {bias:.2f}')
	
	param.bias = bias
	sim = Simulation(param)
	res = sim.run_many(R, T)
	results[bias] = res['gini']

with open(results_folder + output_file, 'wb') as output:
	pickle.dump(results, output, protocol=pickle.HIGHEST_PROTOCOL)

end = time.time()
print('\n\nRunning time: %.2f seconds.'%(end-start))
print('\n\n---> END.')
