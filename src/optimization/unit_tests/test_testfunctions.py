'''
Created on 19.12.2011

@author: Florian Hartig
'''


import unittest
import numpy as np

from optimization.testfunctions import *


class Test(unittest.TestCase):


    def test_quadratic(self):
        assert(quadratic_testfunction(2)==4)
        assert(quadratic_testfunction((2,2))==8)
        assert(quadratic_testfunction(np.array([2,-2]))==8)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()