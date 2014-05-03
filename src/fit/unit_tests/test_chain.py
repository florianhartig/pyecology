'''
Created on 10.03.2010

@author: floha
'''

import unittest
from fit.chain import * 
from fit.sampler import *
import numpy as np


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass
    


    def testChain(self):
        chain = Generic_Chain()
        for _ in xrange(100):
            chain.append(state=np.array([0,0,0]), value_state = 1, proposed =np.array([1,1,1]), value_proposed = 1, accepted= False)
        assert chain.get_acceptance_rate() == 0

        for _ in xrange(100):
            chain.append(state=np.array([0,0,0]), value_state = 1, proposed =np.array([1,1,1]), value_proposed = 1, accepted= False)
        chain.reset()
        chain.surpress_nones = True
        for _ in xrange(1000):
            chain.append(state=np.array([0,0,0]))
            
            
    def testStatistics(self):
        chain = Generic_Chain()
        generator = Multivariate_Normal_Sampler()
        covariance = np.array([[1.0,0.5],[0.5,1.0]])
        generator.set_covariance(covariance)
        for _ in xrange(1000):
            chain.append(state = generator.get_proposal(np.array([0,0])), proposed = generator.get_proposal(np.array([0,0])), accepted = np.random.randint(0,2)) #
        x = chain.get_mean_std()
        assert np.all(x[0] < 0.1)
        assert np.all(0.9 < x[1])
        assert np.all(x[1]< 1.1)
        assert np.all((chain.get_covariance() - covariance) < 0.2 )
        
        print chain.get_acceptance_per_dimension()

    def testSaveLoad(self):
        chain = Generic_Chain()
        chain.append(1, 1, 1, 1, 1)
        chain.append(2, 2, 2, 2, 2)
        chain.save_data()
        chain.reset()
        chain.load_data()
        chain.save_data()
        print chain.states


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()