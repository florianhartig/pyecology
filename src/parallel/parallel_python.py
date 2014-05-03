'''
Created on 07.03.2010

@author: Florian Hartig http://florianhartig.wordpress.com/
'''
import sys
from scipy import inf
from fit.bayesian import Posterior
import numpy as np



def Abstract_PP_Function(value, parallel = False):
    '''
    @summary: abstract interface for parallelized functions to be used
    in mcmc and optimization algorithms.
    
    @param value: value is expected to be an object (usually np-array) 
    if parallel = false, else a list of objects of the same type
    
    @param parallel: must be in the parameter List, and the function needs to
    implement a switch for parallel. Automatic choice is discouraged because 
    we don't explicitly check for value not being a list
    
    @return: returns something, usually np-numeric type
    '''     
    raise NotImplementedError





class Job_Server(object):
    '''
    @summary: Parent class for classes that implement pp functionality
    @param servers: tuple of all parallel python servers to connect with, example ("*",) = auto-discover, ("10.0.0.1","10.0.0.2") # list of static IPs
    @param ncpus: number of CPUs to reserve 
    '''
    def __init__(self, servers=None, ncpus=None):
        '''
        Constructor
        @param servers: tuple of all parallel python servers to connect with, example ("*",) = auto-discover, ("10.0.0.1","10.0.0.2") # list of static IPs
        @param ncpus: number of CPUs to reserve 
        '''    
        self.job_server = None
        self.number_of_cores = None
        self.parallelmode = False    
        self._renew_pp_server(servers=servers, ncpus=ncpus)


    def print_pp_stats(self):
        if self.parallelmode:
            self.job_server.print_stats()
        else:
            print "Job server in serial model"
   
    def _renew_pp_server(self, servers = None, ncpus = None):
        '''
        @summary: renews the pp server
        @param servers: tuple of all parallel python servers to connect with, example ("*",) = auto-discover, ("10.0.0.1","10.0.0.2") # list of static IPs
        @param ncpus: number of CPUs to reserve 
        '''     
        try:
            self.job_server.destroy()
        except:
            pass
        
        if servers == "serial":
            self.job_server = None
            self.number_of_cores = None
            self.parallelmode = False
        else:
            import pp
            if servers == "auto":
                servers = None    
            if (servers == None) and (ncpus == None):
                self.job_server = pp.Server()     
            elif (servers == None) and (ncpus != None):
                self.job_server = pp.Server(ncpus = ncpus)
            elif (servers!= None) and (ncpus == None):
                self.job_server = pp.Server(ppservers=servers)
            elif (servers!= None) and (ncpus != None):
                self.job_server = pp.Server(ppservers=servers, ncpus = ncpus)
                
            self.number_of_cores = self.job_server.get_ncpus()
            self.parallelmode = True
            print "Parallel Python option started with", str(self.number_of_cores), "cores"
        

        
        

        

