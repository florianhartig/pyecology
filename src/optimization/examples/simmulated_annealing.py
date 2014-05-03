'''
Created on 14.03.2010

@author: floha
'''

import numpy as np 
from scipy import stats
from matplotlib import pyplot
from fit import sampler
from optimization.annealing import Simmulated_Annealing
from optimization import testfunctions 


print "================================="
print "optimizing 1d-nomal function"
print "Examples shows basic use of the simmulated annealing "


objectivefunction = testfunctions.quadratic_testfunction

startvalue = 2
proposal = sampler.Multivariate_Normal_Sampler(scale = 0.4)

optimizer = Simmulated_Annealing(objectivefunction, startvalue, proposal)
optimizer.temperature_decay = 0.02
optimizer.temperature = 1

optimizer.run(1000)

print "best value", optimizer.best_parameter
optimizer.chain.convert_list_to_nparray()


#plotting 
pyplot.figure(num=2) 
pyplot.plot(10 * np.exp(- optimizer.temperature_decay * np.arange(1,1000,1)))
pyplot.plot(optimizer.chain.statearray[:,0])
pyplot.show()



if __name__ == '__main__':
    pass