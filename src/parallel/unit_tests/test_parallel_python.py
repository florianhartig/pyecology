'''
Created on 07.03.2010

@author: floha
'''
import unittest
from parallel.parallel_python import *
from fit.bayesian import Parallel_Posterior


class Test(unittest.TestCase):


    def test_get_pp_server(self):
        server = Job_Server()
        server.destroy()
       
    def test_Job_Server(self):
        server_object = Job_Server()
        server_object.job_server.destroy()
        
    def test_Posterior(self):
        def prior(x):
            if (np.min(x) < 0.0):
                return(inf)
            else:
                return(1.0)
            
        def likelihood(x, parallel=False):
            if parallel:
                return [np.exp(np.square(par)) for par in x]
            else:
                return np.exp(np.square(x))
        
        post = Parallel_Posterior(likelihood, prior, nll=True)
        
        output1 = post.get_value(0)
        assert(output1 == 1)
        
        testparameters = [-1,0,1,2]
        output2 = post.get_value(testparameters, parallel = True)
        assert(output2 == [inf, 1.0, 2.7182818284590451, 54.598150033144236])


        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()