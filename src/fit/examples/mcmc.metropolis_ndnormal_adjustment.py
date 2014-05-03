'''
Created on 01.02.2010


@author: floha
'''

import numpy as np 
from scipy import stats
from fit import sampler, mcmc

def model(x):
    scale = (1,20,0.1,2,20000)
    y = stats.norm.pdf(x, scale = scale)
    return np.multiply.reduce(y)

startvalue = np.array([0,0,0,0,0])
proposal = sampler.Multivariate_Normal_Sampler(scale = 1, dimension_proposal=1)


mcmcsampler = mcmc.Metropolis_Like_MCMC(model,startvalue, proposal)

#mcmcsampler.run(10000)
mcmcsampler.run_adaptive_metropolis(times=20)

print mcmcsampler.chain.get_acceptance_per_dimension(-2000)
print mcmcsampler.chain.get_acceptance_rate(-2000)





