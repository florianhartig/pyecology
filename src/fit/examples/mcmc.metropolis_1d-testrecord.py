'''
Created on 01.02.2010


@author: floha
'''

import numpy as np 
from scipy import stats
from matplotlib import pyplot
from fit import sampler, mcmc

print "================================="
print "explains the recording of additional information, for the rest see 1dnormal"

model = stats.norm.pdf

def testfunction():
    return 3 

startvalue = 0
proposal = sampler.Multivariate_Normal_Sampler(covariance = 100)
mcmcsampler = mcmc.Metropolis_Like_MCMC(model,startvalue, proposal)
mcmcsampler.set_recording_function(testfunction, 10)
mcmcsampler.run(100)
mcmcsampler.chain.save_data()

print "done, look at the record file in the chain output folder"
print "here's a printout"
print mcmcsampler.chain.records