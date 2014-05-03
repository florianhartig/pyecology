'''
Created on 22.03.2010

@author: floha
'''

from mcmc.mcmc import *
import time
from model.base import Markov_Model

class MCMC_Wrapper(Markov_Model):
    '''
    classdocs
    '''
    

    def __init__(self, mcmcs, cores = None):
        '''
        Constructor
        '''
        self.mcmcs = mcmcs
        self.cores = cores
        self.cores_mcmc = None 
#        for i in xrange(chains):
#            self.mcmcs.append(MCMC(model, startvalue, proposalgenerator, self.acceptancefunction.get_acceptance, nll=nll, parallel_cores=parallel_cores))

    def _step_actions(self):
        for mcmc in self.mcmcs:
            mcmc.step()
            
    def _run_finalize(self):
        for mcmc in self.mcmcs:
            print("Steps finished, acceptance rate: " + str(mcmc.chain.get_acceptance_rate()) + " time since mcmc init: " + str(time.time() - mcmc.initializationtime))        
