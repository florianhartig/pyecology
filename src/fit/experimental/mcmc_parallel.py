'''
Created on 07.03.2010

@summary: parallel version of the mcmc module. 
Uses / requires Parallel Python: http://www.parallelpython.com

@author: floha
'''

import sys, copy
from fit.mcmc import Metropolis_Like_MCMC
from parallel.parallel_python import Job_Server

class Metropolis_Like_MCMC_Parallel_Copied(Metropolis_Like_MCMC, Job_Server):
    '''
    classdocs
    '''
    def __init__(self, model_factory, startvalue, proposalgenerator, nll=False, id=None, servers=None):
        '''
        Constructor
        '''
        Metropolis_Like_MCMC.__init__(self, model=model_factory, startvalue=startvalue, proposalgenerator=proposalgenerator, nll=nll, id=id)
        Job_Server.__init__(self, servers)
        self.modellist = self.model(self.number_of_cores)
           
    def testfunction(self, par):
        print "run parameters", par
        return(par)
    
         
    def run(self, times=1): 
        for _ in xrange(times):
            new_parameters = self.proposalgenerator.get_n_proposals(self.current, self.self.number_of_cores)
            jobs = []
            for par in xrange(self.number_of_cores):
                pass
#                jobs.append(self.job_server.submit(self.testfunction[i], (par[i],), modules=()  ))
            #self.job_server.wait(group="MCMC")#
#            print(run_results)
#            for _ in xrange(self.number_of_cores):
#                pass
            
        self.job_server.print_stats()






