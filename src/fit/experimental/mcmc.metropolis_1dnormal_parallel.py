'''
Created on 01.02.2010

@author: floha
'''

import numpy as np 
from scipy import stats
from matplotlib import pyplot
from mcmc import proposalgenerator, mcmc, mcmc_parallel
import copy


def model_factory(n):
    return [stats.norm.pdf for i in range(n)] 

startvalue = 0
proposal = proposalgenerator.Multi_Normal_Proposalgenerator(1)



mcmcsampler = mcmc_parallel.Metropolis_Like_MCMC_Parallel_Copied(model_factory,startvalue, proposal)

mcmcsampler.run(10)
