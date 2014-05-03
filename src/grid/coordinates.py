'''
Created on 26.02.2010

@author: Florian Hartig http://florianhartig.wordpress.com/
'''
import numpy as np


class Coordinatesystem(object):
    '''
    classdocs
    '''
    def __init__(self, size, topology):
        '''
        Constructor
        @param dimensions: integer 
        @param topology: np.array. 0 standing for line, 1 for S1, 2 for S2 ... thus, [2,0] is S2xR Topology 
        '''
        self.size = size
        self.dimensions = len(self.size)
        self.topology = topology
        
    def get_distance(self, x, y):
        raise NotImplementedError
    
    def euclidian_distance(self, x, y):
        assert len(x) == len(y) == self.dimensions
        return np.sqrt(np.sum(np.square(np.x - np.y))) 