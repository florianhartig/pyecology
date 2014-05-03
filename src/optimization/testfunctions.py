'''
Created on 19.12.2011

@summary: reference functions for testing the optimizers
@author: Florian Hartig http://florianhartig.wordpress.com/
'''


import numpy as np 


'''
@summary: n-dimensional quadratic function centered around 0
'''
def quadratic_testfunction(x):
    out = np.sum(np.square(x))
    return(out)

