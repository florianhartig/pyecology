'''
Created on 05.11.2010

@author: floha
'''
import unittest
from model.base import *


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_abstract_markov_process(self):
        test = Markov_Model(1)
        assert test.tick == 0
        assert type(test.current) == np.ndarray
        #checking type conversions, tupel
        test = Markov_Model((1))
        assert type(test.current) == np.ndarray
        #checking type conversions, mixed list
        test = Markov_Model([1,"x", 3])
        assert type(test.current) == np.ndarray
        test.load_random_seed()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()