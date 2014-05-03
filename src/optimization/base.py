import numpy as np 
#from model.multinormal import MultiNormalModel 
from model.base import Model


class Generic_Optimizer(Model):
    '''
    @summary: PyEcology - Generic Optimization function
    '''

    def __init__(self, maxiter = 200):
        '''
        Constructor
        '''
        Model.__init__(self)
        self._maxiter = maxiter
        
    def check_convergence(self):
        '''
        @summary: temperature adjustment function ... may be useful to overwrite this to reach faster convergence
        TODO: implementation
        '''
        self.best_list =[]
        



