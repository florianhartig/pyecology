'''
Created on 01.02.2010

@author: floha
'''

print "================================================"
print "example using a negative log likelihood function"
print "posterior is defined as the sum of squares"

import numpy as np 
from scipy import stats
from matplotlib import pyplot
from fit import sampler, mcmc



def posterior(x):
    return np.square(x)

# remember, np scales with exp( (x/scale)^2 /2)
def pdf(x):
    return (stats.norm.pdf(x, scale = 1.0/np.sqrt(2) ))

startvalue = 0.2
proposal = sampler.Multivariate_Normal_Sampler(scale=2)

mcmcsampler = mcmc.Metropolis_Like_MCMC(posterior,startvalue, proposal, nll=True)
mcmcsampler.save_intervals = 1000
mcmcsampler.run(10000)

mcmcsampler.chain.convert_list_to_nparray()
#plotting 
pyplot.figure(num=3) 
pyplot.plot(np.arange(-1,1,0.01), posterior(np.arange(-1,1,0.01)))
pyplot.title("target distribution")
pyplot.hist(mcmcsampler.chain.statearray[:,0], bins=100, normed=True)
pyplot.plot(np.arange(-5,5,0.01), pdf(np.arange(-5,5,0.01)))
pyplot.show()


