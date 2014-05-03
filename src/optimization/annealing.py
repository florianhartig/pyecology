'''
Created on 19.12.2011

@author: Florian Hartig http://florianhartig.wordpress.com/
'''

import numpy as np 
from optimization.base import Generic_Optimizer
from fit.mcmc import MCMC_REJ



class Simmulated_Annealing(MCMC_REJ, Generic_Optimizer):
    '''
    @summary: implements simulated annealing algorithm. Interface similar to MCMC
    
    @param model: function to be optimized, should take np-array or, for parallel runs, list of np-array as input
    @param startvalue: startvalue, usually np-array or convertable
    @param proposalgenerator: Class with interface of mcmc.proposalgenerator.Abstract_Proposalgenerator
    @param acceptancefunction: function with interace of mcmc.acceptancefunction
    '''
    def __init__(self, model, startvalue, proposalgenerator=None, acceptancefunction=None, parallel_cores = None):
        MCMC_REJ.__init__(self, model, startvalue, proposalgenerator, acceptancefunction, parallel_cores = parallel_cores)
        Generic_Optimizer.__init__(self)
        if acceptancefunction == None:
            self.acceptancefunction = self.metropolis_acceptance
        self.best_value = self.model(self.current)
        self.best_parameter = self.current
        self.temperature_decay = 0.05
        self.temperature = 5


    '''
    @summary: checks whether a is better than b under the current optimization constraint
    '''
    def AisBetterB(self,a,b):
        if (a < b):
            return True
        else:
            return False
        
        
    def metropolis_acceptance(self, old, new, temperature=None):
        if temperature == None:
            temperature = self.temperature
        delta = (new - old) 
        if (delta < 0):
            return(True)
        else:
            acceptance_prob = np.exp(-delta/temperature)
            if (np.random.random_sample() < acceptance_prob):
                return(True)
            else:
                return(False)
    
    def adjust_temperature(self):
        '''
        @summary: temperature adjustment function ... may be useful to overwrite this to reach faster convergence
        '''
        self.temperature = self.temperature * (1-self.temperature_decay)

    def _step_post(self):
        self.tick += 1
        self.adjust_temperature()
        if self.AisBetterB(self.value_current,self.best_value):
            self.best_value = self.value_current
            self.best_parameter = self.current
        if self.tick % self.save_intervals == 0:
            self.chain.save_data()

