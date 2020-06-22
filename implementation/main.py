#!python3

import os
import time
from simulation import Simulation
from param import Param

def save_results(results, filename, folder):
    os.makedirs(folder, exist_ok=True)
    results.to_csv(folder+filename+'.csv', 
                index_label=['time'])

N, R, T = 1000, 200, 50
results_folder = '../results/'

param = Param()
param.size = N
param.bias = -0.25
param.negative_tax = False
param.basic_income = False

print('\n---> START.')
start = time.time()

print('\n\t> Control simulation:')

control = Simulation(param)
results = control.run_many(R, T)

save_results(results=results,
             filename='control',
             folder=results_folder)

print('\n1st Partial running time: %.2f seconds.'%(time.time()-start))

print('\n\t> Treatment simulation 1:')

param.negative_tax = True
param.exemption_quantile = 0.3429
param.subsidy_rate = 0.5
param.basic_income = False

treat1 = Simulation(param)
results = treat1.run_many(R, T)

save_results(results=results,
             filename='treat1',
             folder=results_folder)

print('\n2nd Partial running time: %.2f seconds.'%(time.time()-start))

print('\n\t> Treatment simulation 2:')

param.basic_income = True
param.fixed_benefit = 0.0
param.variable_benefit = 0.25
param.negative_tax = False

treat2 = Simulation(param)
results = treat2.run_many(R, T)

save_results(results=results,
             filename='treat2',
             folder=results_folder)

end = time.time()
print('\n\nOverall running time: %.2f seconds.'%(end-start))
print('\n\n--->END.')
