'''
Created on 22.03.2010

@author: floha
'''
import unittest
from fit.bayesian import *
import numpy as np

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass
    
    def ll(self, x, parallel = False):
        if parallel:
            out = []
            for a in x:
                out.append(np.exp(-a))
            return out 
        else:
            return np.exp(-x)
    
    def testPosterior(self):
        prior = Uniform_Prior(0)
        post = Posterior(self.ll, prior = prior, nll = False)
        assert post.get_value(0) == 1
        assert post.get_value(-1) == 0

    def testParallelPosterior(self):

        prior = Uniform_Prior(0)
        post = Parallel_Posterior(self.ll, prior = prior, nll = False)
        assert post.get_value([-1,0], parallel=True) == [0, 1.0]
        assert post.get_value(-1, parallel=False) == 0
        assert post.get_value(0, parallel=False) == 1


    def testUniformPrior(self):
        priorfunction = Uniform_Prior(-1,1,nll=False)
        assert priorfunction.get_value([0]) == 1
        assert priorfunction.get_value([-2]) == 0
        assert priorfunction.get_value([-1]) == 1
        priorfunction.accept_boundary = False
        assert priorfunction.get_value([-1]) == 0
        priorfunction = Uniform_Prior(-1,1,nll=True)
        assert priorfunction.get_value([0]) == 0
        assert priorfunction.get_value([-2]) == inf
        priorfunction.load_data("parameter_ranges.txt")
        assert(priorfunction.get_value(priorfunction.data[:,2]) == 0)
        assert(priorfunction.get_value(np.array([0.604771878249, 0.0636543266931, 0.0500196921668, 0.0593884047622, 226.161509738, -3.96484392677, 11.3259224622, 0.00291860290854, -0.0446679927192, 0.106365842131, 0.463479795087, 0.140392714491, 0.215134505111, 1.90297092614])) == inf)
        priorfunction = Uniform_Prior(0)
        assert priorfunction.get_value(1) == 1
        assert priorfunction.get_value(-1) == 0
    def testTriangularPrior(self):
        priorfunction = Triangular_Prior(nll=False)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testPrior']
    unittest.main()