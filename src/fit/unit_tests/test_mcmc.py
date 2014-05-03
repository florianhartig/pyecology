'''
Created on 06.03.2010

@author: floha
'''
import unittest
from fit.mcmc import *
import numpy as np
from scipy import stats
from fit import sampler

def ll_normal(x):
    return np.square(x) 

def ll_normal_noise(x):
    return np.square(x) + stats.norm.rvs()



class MCMC_Test(unittest.TestCase):


    def setUp(self):
        pass

    def tearDown(self):
        pass

        
    def test_mcmc(self):
        pass
#        startvalue = 0.2
#        proposal = sampler.Multivariate_Normal_Sampler(scale=1)
#        mcmc = Metropolis_Like_MCMC(ll_normal_noise, proposal, startvalue)
    
    def test_normal(self):
        pass
        #examples.mcmc

    def test_pickle(self):
        pass
        startvalue = 0.2
        proposal = sampler.Multivariate_Normal_Sampler(scale=1)
        mcmc = Metropolis_Like_MCMC(ll_normal_noise, startvalue, proposal)
        #mcmc.pickle_dump()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()