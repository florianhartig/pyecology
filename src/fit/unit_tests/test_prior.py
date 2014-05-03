'''
Created on 09.08.2011

@author: Florian Hartig
'''
import unittest
from fit.bayesian import *


class Test(unittest.TestCase):


    def test_uniform(self):
        unif = Uniform_Prior(lower = (4,4), upper = (6,6))
        unif


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()