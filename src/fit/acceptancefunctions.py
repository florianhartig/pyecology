'''
Created on 03.03.2010

@author: Florian Hartig http://florianhartig.wordpress.com/
'''
import numpy as np

class Abstract_Acceptancefunction(object):
    '''
    classdocs
    '''
    
    def __init__(self, nll = False):
        '''
        Constructor
        '''
        self.nll = nll 
    
    def get_acceptance(self):
        raise NotImplementedError


class Metropolis(Abstract_Acceptancefunction):
    '''
    implements Metropolis acceptance function for maximum and 
    default is maximization of likelihood
    nll is chosen when negative log likelihood is minimized
    '''
    
    def __init__(self, nll = False):
        '''
        Constructor
        '''
        Abstract_Acceptancefunction.__init__(self, nll)
    
    def get_acceptance(self, current,proposed):
            
            if(self.nll==True):
                if (proposed < current):
                    return(True)
                else:
                    acceptancerate = np.exp(-(proposed - current))
                    
            else: 
                if (proposed > current):
                    return(True)
                else:
                    acceptancerate = proposed / current
            
            if np.random.random_sample() < acceptancerate:
                return(True)
            else:
                return(False)
            
            
class Binary(Abstract_Acceptancefunction):
    '''
    For ABC algorithms
    '''
    
    def __init__(self, nll = False):
        '''
        Constructor
        '''
        Abstract_Acceptancefunction.__init__(self, nll)
    
    def get_acceptance(self, current, proposed):
        return proposed