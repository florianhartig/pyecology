'''
Created on 01.02.2010

@author: Florian Hartig http://florianhartig.wordpress.com/
'''
from __future__ import division
import time, warnings, os
import numpy as np
from scipy import inf
from chain import Generic_Chain
from acceptancefunctions import Metropolis, Binary
from abstract.base import Debugable
from model.base import Markov_Model
import cPickle




class MCMC(Markov_Model):
    '''
    @summary: Generic base class for MCMC calculations
    '''

    def __init__(self, startvalue):
        '''
        Constructor
        '''
        Markov_Model.__init__(self, startvalue)
        self.chain = Generic_Chain(startvalue)
        self._record = None
        self._record_interval = 1
        
        
    def set_recording_function(self, function, interval=1):
        '''
        @summary: optional function that can be set to store additional calculations during MCMC evaluation
        @note: typically a function of mcmc.model
        @param interval: recording interval 
        '''
        self._record = function
        self._record_interval = interval
        


class MCMC_REJ(MCMC):
    '''
    @summary: Base class for rejection type MCMCs
    '''

    def __init__(self, model, startvalue, proposalgenerator, acceptancefunction, nll=False, parallel_cores = None, restart = True):
        '''
        Constructor
        '''
        MCMC.__init__(self, startvalue)
        self.parallel_cores = parallel_cores
        self.model = model
        self.proposalgenerator = proposalgenerator
        self.acceptancefunction = acceptancefunction
        self.nll = nll
        self._recalculate = False
        self.modelruns = 0
        self.save_intervals = 10000
        self.targetacceptance = 0.3 # for automatic adjustment of proposals
        

    def run(self, times=1, startvalue = None): 
        
        times = int(times)
        
        # potentially update startvalue and calculate the target function value of the startvalue
        if startvalue!= None:
            self.current = startvalue
        self.value_current = self.model(self.current)  
        
        if self.parallel_cores == None: 
            for _ in xrange(times):
                if self._recalculate:
                    self.value_current = self.model(self.current) 
                new = self.proposalgenerator.get_proposal(self.current)
                value_new = self.model(new)
                accepted = self.acceptancefunction(self.value_current, value_new)
                if self.debug:
                    print ("MCMC Step"+str(self.tick) + ", current=" + str(self.value_current)+ ", new=" + str(value_new)+ ", accepted=" + str(accepted))
                if (accepted):
                    self.current = new
                    self.value_current = value_new 
                self.chain.append(state = self.current, value_state = self.value_current, proposed = new, value_proposed = value_new, accepted = accepted)
                self._step_post()
        else:
            assert(self.parallel_cores > 1 or self._recalculate != True) # otherwise could create 
            
            # TODO: propose more than cores, for the case that the prior rejects the runs!!!
            
            for _ in xrange(times):
                
                # self.recalculate recalculates the current value
                # makes sense for stochastic models
                if self._recalculate:
                    new = self.proposalgenerator.get_proposal(self.current, n=(self.parallel_cores-1))
                    new.append(self.current)
                else:
                    new = self.proposalgenerator.get_proposal(self.current, n=self.parallel_cores)
    
                values_new = self.model(new, parallel = True)
                if self._recalculate:
                    self.value_current = values_new.pop()
                    new.pop()
        
                for i in range(len(values_new)):
                    if self.acceptancefunction(self.value_current, values_new[i]):
                        self.current = new[i]
                        self.value_current = values_new[i] 
                        self.chain.append(state = self.current,  value_state = self.value_current, proposed = new[i], value_proposed = values_new[i], accepted = True)
                        self._step_post()
                        if self.debug:
                            print "accepted " + str(i+1) + "-th proposal of " + str(self.parallel_cores)
                        break
                    else:
                        self.chain.append(self.current,  value_state = self.value_current, proposed = new[i], value_proposed = values_new[i], accepted = False)
                        self._step_post()
                self.modelruns += len(values_new)
        self.summary
 
 
    def run_delayed_rejection(self, times=1, delaysteps = None):
        if delaysteps == None:
            delaysteps = self.parallel_cores
        assert(delaysteps > 1)
        assert(self._recalculate == False)
        
        
    
    def run_delayed_rejection_adaptive_metropolis(self, times = 100, n0=2000, n1 = 1000, dimension_proposal_adjustment = True):
        '''
        @summary: from H. Haario, M. Laine, A. Mira and E. Saksman, 2006. DRAM: Efficient adaptive MCMC, Statistics and Computing 16, pp. 339-354. 
        '''
          
        epsilon = 0.000000001 * np.identity(self.dimensions) # to avoid singular covariance
        self.run(n0)
        for _ in xrange(times):
            cov = self.chain.get_covariance() + epsilon
            self.proposalgenerator.set_optimal_covariance(cov)
            self.run(n1)        

    def run_adaptive_metropolis(self, totalsteps = 100000, intermediatesteps = 1000, initialsteps=2000, dimension_proposal_adjustment = True):
        '''
        @summary: following H. Haario, E. Saksman and J. Tamminen, 2001. An adaptive Metropolis algorithm Bernoulli 7, pp. 223-242. 
        @note: In Adaptive Metropolis, (Haario, et al. 2001) the covariance matrix of the Gaussian proposal distribution is adapted on the fly using the past chain. This adaptation destroys the Markovian property of the chain, however, it can be shown that the ergodicity properties of the generated sample remain. How well this works on finite samples and on high dimension is not obvious and must be verified by simulations. (text from http://www.helsinki.fi/~mjlaine/dram/)
        '''

        times = np.round((totalsteps - initialsteps) / intermediatesteps)
        starttick = self.tick + 1 
        self.run(initialsteps)
        
        for _ in xrange(times):
            self._adjust_covariance(lower = starttick)
            self.run(intermediatesteps)        

    def _adjust_covariance(self, lower = None, upper = None, epsilonscale = 0.000000001):
        '''
        @summary: help function to adjust the covariance
        '''
        epsilon = epsilonscale * np.identity(self.dimensions) # to avoid singular covariance
        oldcovariance = self.proposalgenerator.covariance_decomposed
        try:
            cov = self.chain.get_covariance(lower = lower, upper = upper) + epsilon
            self.proposalgenerator.set_optimal_covariance(cov)
            self.proposalgenerator.get_proposal() # to test for potential problems
            if self.debug:
                self.add_to_log("covariance adjusted to" + cov)
        except:
            self.proposalgenerator.covariance_decomposed = oldcovariance
             
    
    def _step_post(self):
        '''
        things to do each step
        '''
        self.tick += 1
        
        if self._record != None: 
            if self.tick % self._record_interval == 0:
                self.chain.append_record(self.tick, self._record()) 
    
        if self.tick % self.save_intervals == 0:
            self.chain.save_data()
            
        
    def adjust_scale(self, totalsteps, adjustmentsteps = 5):
        if self.proposalgenerator.covariance_decomposed != None:
            warnings.warn("covarai was set to None for adjustment of the covariance")
        
        scaling = 2.38 * 2.38 / self.dimensions
        self.proposalgenerator.covariance_decomposed = None
        raise NotImplementedError
    
    
    def balance_scale(self, targetacceptance = 0.3, lower = -1000, upper = None):
        
        acceptance = self.chain.get_acceptance_rate(lower, upper)
        dimacceptance = self.chain.get_acceptance_per_dimension(lower, upper)
        
        assert(self.proposalgenerator.scale!=None)
        
        print acceptance 
        print dimacceptance
        
        
        
    def adjust_covariance(self, totalsteps, adjustmentsteps=5, dimension_proposal_adjustment = True):
        '''
        @summary: function for adjusts covariance prior to mcmc sampling. Runs a chain of lengt totalsteps / adjustmentsteps
        @param totalsteps: number of steps for adjustment. 
        @param adjustmentsteps: covariance adjustemts during totalsteps 
        @param dimension_proposal_adjustment = True adjusts covariance according to dimension proposal setting in the sampler
        @note: see Andrieu and Thomas (2008) 
        '''
        if self.proposalgenerator.scale != None:
            self.proposalgenerator.scale = None
            warnings.warn("proposalgenerator.scale was set to None for adjustment of the covariance")
  
        runs  = np.round(totalsteps/adjustmentsteps)
        for _ in xrange(adjustmentsteps):
            self.run(runs)
            # scaling = scaling * self.chain.get_acceptance_rate(-runs, len(self.chain.states)) /  self.targetacceptance
            # removed in favor of fixed scaling
            self._adjust_covariance(-runs, len(self.chain.states))

            
    @staticmethod
    def get_covariance(filename=None, MCarray=None):
        '''
        @summary: static method to get covariance from array prepared for covariance scaling in sampler
        '''
        assert((filename== None) | (MCarray == None))
        if filename!= None:
            MCarray = np.loadtxt(filename)
        MCcov = np.cov(np.transpose(np.loadtxt(filename)))
        return(MCcov)

    
    def summary(self):
        print("Acceptance rate: " + str(self.chain.get_acceptance_rate()) + " time since mcmc init: " + str(time.time() - self.initializationtime) )        
        if self.parallel_cores != None:
            print "parallel efficiency =", len(self.chain.states)/self.modelruns   

    def pickle_dump(self):
        '''
        Not implemented yet
        '''
        f = open(self.get_savepath() + "pickledstate.dat", "w" )
        cPickle.dump(self, f)
        f.close()


    def set_recalculate(self, recalculate = False):
        '''
        @summary: setting recalculate = True means that likelihood of the current parameter is reevaluated
        @note: has only an influence for stochastic Likelihoods, may lead to faster convergence.
        @warning: Recalculating destroys the MCMC convergence see Andrieu, C. & Roberts, G. The pseudo-marginal approach for efficient Monte Carlo computations Ann. Statist, 2009, 37, 697-725
        ''' 
        self._recalculate = recalculate
     


      
class Metropolis_Like_MCMC(MCMC_REJ):
    '''
    classdocs
    '''

    def __init__(self, model, startvalue, proposalgenerator, nll=False,  parallel_cores = None):
        '''
        Constructor
        '''
        self.acceptancefunction = Metropolis(nll)
        MCMC_REJ.__init__(self, model, startvalue, proposalgenerator, self.acceptancefunction.get_acceptance, nll=nll, parallel_cores=parallel_cores)
     
                
        
class Marjoram_Like_ABC(MCMC_REJ):
    '''
    MCMC for approximate Bayesian computing 
    
    @param model: requires that model already implements the comparison to the data, i.e. that model either returns true or false  
    '''

    def __init__(self, model, startvalue, proposalgenerator, nll=False,  parallel_cores = None):
        '''
        Constructor
        '''
        self.acceptancefunction = Binary()
        MCMC_REJ.__init__(self, model, startvalue, proposalgenerator, self.acceptancefunction.get_acceptance, nll=nll, parallel_cores=parallel_cores)
        
