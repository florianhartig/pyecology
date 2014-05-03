'''
Created on 05.11.2010

@author: Florian Hartig http://florianhartig.wordpress.com/
'''

from abstract.base import *

class Model(Logable, Debugable):
    '''
    @summary: PyEcology - Abstract base class that should be implemented by all
    model-type objects
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        Logable.__init__(self) 
        Debugable.__init__(self) 
        
    def run(self):
        raise NotImplementedError
        
  
class Stochastic_Model(Model, Stochastic):
    '''
    @summary: Stochastic Base Class
    '''
    def __init__(self):
        '''
        Constructor
        '''
        Model.__init__(self)
        Stochastic.__init__(self)
          
        
        
class Markov_Model(Model, Stochastic):
    '''
    @summary: PyEcology - Abstract base class that should be implemented 
    by all markov process type objects
    '''
      
    def __init__(self, startvalue):
        '''
        Constructor
        '''
        Model.__init__(self)
        Stochastic.__init__(self)
        self.current = np.ravel(startvalue)
        self.dimensions = np.size(self.current)
        self.tick = 0
           
    def step(self):
        '''
        for speed reasons, step should not necessarily implement all the three functions
        '''
        self._step_pre()
        self._step_actions()
        self._step_post()

    def _step_pre(self):
        pass
        
    def _step_actions(self):
        raise NotImplementedError

    def _step_post(self):
        self.tick += 1
        
    def run(self, times):
        '''
        for speed reasons, step should not necessarily implement all the three functions
        '''
        for _ in xrange(times):
            self._step_pre()
            self._step_actions()
            self._step_post()
        self._run_finalize()
    
    def _run_finalize(self):
        pass
    
