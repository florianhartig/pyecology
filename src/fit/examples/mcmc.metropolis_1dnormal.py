'''
Created on 01.02.2010


@author: floha
'''

import numpy as np 
from scipy import stats
from matplotlib import pyplot
from fit import sampler, mcmc

print "================================="
print "start sampling 1d-nomal function"
print "Examples shows basic use of the mcmc "
print "and how to use continuous output to file "


print "================================="
print "create model, startvalue and propsalgenerator"
model = stats.norm.pdf
startvalue = 0
proposal = sampler.Multivariate_Normal_Sampler(covariance = 100)

print "================================="
print "create mcmc"
mcmcsampler = mcmc.Metropolis_Like_MCMC(model,startvalue, proposal)

print "================================="
print "Running MCMC sampler with 10 steps"
mcmcsampler.run(10)

print "================================="
print "Automatic adjusting of covariance"
mcmcsampler.adjust_covariance(10000, 20)
mcmcsampler.chain.reset()


# mcmcsampler.recalculate = True # recalculates the model value each run, useful when sampling/optimizing stochastic models 
print "running more steps"
mcmcsampler.run(10000)
print "================================="


mcmcsampler.chain.convert_list_to_nparray()

#plotting 
pyplot.figure(num=2) 
pyplot.plot(np.arange(-5,5,0.01), model(np.arange(-5,5,0.01)))
pyplot.title("target distribution")
pyplot.hist(mcmcsampler.chain.statearray[:,0], bins=100, normed=True)
pyplot.show()


