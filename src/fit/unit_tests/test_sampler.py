'''
Created on 19.03.2010

@author: floha
'''
from __future__ import division
import unittest
from fit.sampler import *
import numpy as np
import cProfile



class Test(unittest.TestCase):


    def setUp(self):
        self.x1 = np.array([0,0]) 
        self.x2 = np.array([0.0, 0.0, 0.0])
        self.x3 = [0,0,0]
        self.x4 = (0,0.0,0)
        self.x5 = np.zeros([10])

    def tearDown(self):
        pass

    def standardtests(self,generator):
        generator.set_covariance( np.diagflat(np.array([1,1])))
        generator.set_scale(np.array([1,10]))

        sample = np.array(generator.get_proposal(self.x1, 10000))
        mean = [np.mean(sample[:,i]) for i in xrange(len(self.x1))]
        assert np.abs(mean[0]) < 0.1
        std = [np.std(sample[:,i]) for i in xrange(len(self.x1))]
        assert np.round(std[0]) == 1 
        assert np.round(std[1]) == 10
        cov = np.cov(sample.transpose())
        assert np.all(np.abs(np.diagflat(np.array([1,100])) - cov) < 5)
        
        covariance = np.array([[1,0.5],[0.5,1]])
        generator.set_covariance(covariance)
        generator.set_scale(None)
        sample = np.array(generator.get_proposal(self.x1, 10000))

        mean = [np.mean(sample[:,i]) for i in xrange(len(self.x1))]
        assert np.abs(mean[0]) < 0.05
        std = [np.std(sample[:,i]) for i in xrange(len(self.x1))]
        assert np.round(std[0]) == 1 
        assert np.round(std[1]) == 1
        cov = np.cov(sample.transpose())
        assert np.all(np.abs(covariance - cov) < 3)
        cov = np.cov(sample.transpose())
        
        generator.set_covariance(None)
        generator.set_scale((1,1))
        generator.set_boundaries(0,1)
        
        sample = np.array(generator.get_proposal(self.x1, 1000))
        assert np.all(sample >= 0)
        
        generator.set_boundaries()
        generator.set_dimension_proposal(1)
        sample = np.array(generator.get_proposal(self.x1, 100))
        assert np.any(sample == 0)
        assert np.any(sample != 0)
        
        generator.set_dimension_proposal(2)
        sample = np.array(generator.get_proposal(self.x1, 100))
        assert np.all(sample != 0)
   
    def speed_test(self, generator):
        # doesn't work
        function = generator.get_proposal
        cProfile.run('function(np.array([0,0,0]), 10000)')        
        
        

    def testMultivariate_Normal(self):
        generator = Multivariate_Normal_Sampler() 
        self.standardtests(generator)
        
        
    def testMultivariate_Uniform(self):
        generator = Multivariate_Uniform_Sampler()
        self.standardtests(generator)
        
        generator = Multivariate_Uniform_Sampler()
        generator.set_scale(lower = 5, upper = 10)
        generator.dimension_proposal = None
        x = generator.get_proposal(0.0, 500)
        assert min(x) > 4.5 and min(x) < 5.5 
        assert max(x) > 9.5 and max(x) < 10.5       
        generator.set_scale(width = 1)
        x = generator.get_proposal(0.0, 500)
        assert min(x) > - 0.6 and min(x) < - 0.4 
        assert max(x) > 0.4 and max(x) < 0.6

    def test_Covariance_fileio(self):
        generator = Multivariate_Normal_Sampler()
        cov = np.array([[1,0],[0,1]]) 
        generator.set_covariance(cov)
        generator.load_covariance(filename = "testfile.txt", path = ".")

         
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    

    