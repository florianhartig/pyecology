'''
Created on 16.04.2010

@author: floha
'''
import unittest

from abstract.base import *
import scipy.stats as stats


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_Stochastic(self):
        '''
        creates stochastic class, random seed is automatically recored
        creates random number, loads old state, creates new random number, asserts both are equal
        '''
        test = Stochastic()
        a = stats.uniform.rvs()
        test.load_random_seed(test.get_savepath()+"randomseed-pickle.txt")
        b = stats.uniform.rvs()
        assert(a == b)
    
    def test_Saveable(self):
        b = Saveable()
        b.set_savepath("testpath")
        b.set_savepath(globalsavepath="testglobalpath")
        #assert b.get_savepath() == 'testglobalpath\\testpath\\'

    def test_Logable(self):
        a = Logable()
        a.add_to_log("test", echo=True)

    
    def testName(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()