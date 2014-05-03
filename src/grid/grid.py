'''
Created on 26.02.2010

@author: Florian Hartig http://florianhartig.wordpress.com/
'''

import numpy as np
from coordinates import Coordinatesystem

class Grid(np.array, Coordinatesystem):
    '''
    classdocs
    '''
    def __init__(self, coordinatesystem, dimensions, cellsize=(1,1), datatype = np.object):
        '''
        Constructor
        @param cellsize: size of the grid cells 
        '''
        self.coordinatesystem = coordinatesystem
        self.cellsize = cellsize 
        self.dimensions = dimensions
        self.elements = np.empty(dimensions, dtype = datatype) 

                