'''
Created on 20.03.2010

@author: floha
'''

import numpy as np 
from scipy import stats
from matplotlib import pyplot
from fit import sampler, mcmc

current3 = np.array([0,0,0])

generator = sampler.Multivariate_Normal_Sampler((1,1,1))
print generator.get_proposal(current3) # one proposal
print generator.get_proposal(current3,3) # several proposals, as list
print generator.get_proposal(current3,1) # careful, this produces a list with one entry

generator = sampler.Multivariate_Uniform_Sampler()
generator.set_scale(lower = 100, upper = 200)
x = generator.get_proposal(0.0, 5)
print x