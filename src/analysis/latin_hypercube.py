'''
Created on 23.09.2010

@author: Florian Hartig http://florianhartig.wordpress.com/
'''

import numpy as np

def get_hypercube_indices(dimensions, times):

    out = np.empty((times, dimensions))
    
    for i in xrange(dimensions):
        arr = np.arange(times)
        np.random.shuffle(arr)
        arr = np.transpose(np.atleast_2d(arr))
        print out[:1]
        out[:i] = arr
     
    return(out)   

print get_hypercube_indices(3, 10)