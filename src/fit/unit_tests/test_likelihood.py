'''
Created on 25.03.2010

@author: floha
'''
import unittest
from fit.likelihood import *
from scipy import stats
import numpy as np
from scipy import inf


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testNormal(self):
        assert(normal_likelihood(0, 0, 1) == 0)
        assert(normal_likelihood(3, 0, 1) > 0)
        assert(normal_likelihood(1, 0, 1) > normal_likelihood(1, 0, 2))
        assert(normal_likelihood(1, 0, 0) == inf)


    def testMulti(self):
        cov = [[1,0.5],[0.5,1]]
        assert((multivariate_normal_likelihood([0,0], [0,0], covariance = cov) - 1.694036) <0.01)
        assert((multivariate_normal_likelihood([3,3], [0,0], covariance = cov) - 7.694036) <0.01)
        std = [1,1]
        cov = [[1,0],[0,1]]
        compare = -np.log(stats.norm.pdf(1))
                
        assert multivariate_normal_likelihood([1,np.NaN], [0,0], covariance = cov, checkNaNofA = True) == compare
        assert multivariate_normal_likelihood([1,np.NaN], [0,0], standarddeviation = std, checkNaNofA = True) == compare
        
        cov = [[1,0.5],[0.0,0.0]]
        assert(multivariate_normal_likelihood([0,0], [0,0], covariance = cov) == inf)
 
        cov = [[1,0,1],[0,1,0.1],[-0.1,0.1,3]]
        assert( multivariate_normal_likelihood([np.NaN,1,1], [0,0,0], covariance = cov, checkNaNofA = True) - 3.020965 < 0.01)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()