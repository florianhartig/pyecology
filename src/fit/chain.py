'''
Created on 28.01.2010

@author: Florian Hartig http://florianhartig.wordpress.com/
'''
from __future__ import division
import os
import numpy as np
from abstract.base import Debugable, Saveable
import warnings
import pickle
    
class Generic_Chain(Debugable, Saveable):
    '''
    @summary: Generic chain to store parameter for MCMC and Markov-like optimization
    
    @param startvalue: optional start value 
    @param write_continously: write every new value during  
    '''

    def __init__(self, startvalue=None):
        '''
        Constructor
        '''
        Debugable.__init__(self)
        Saveable.__init__(self)
        self.states = []
        self.value_states = []
        self.proposed = []
        self.value_proposed = []
        self.accepted = []
        self.surpress_nones = False
        self.records = []
        
        self.startvalue = startvalue
        self.continous_output = False
        self.changed = True
                
    def append(self, state = None, value_state = None, proposed = None, value_proposed = None, accepted = None):
        '''
        @summary: appends new element to chain
        '''
        if self.debug:
            print "appending to chain: state: ", state, "value", value_state, "proposed", proposed, "value_proposed", value_proposed, " accepted", accepted  

        if self.surpress_nones == False:
            self.states.append(state)
            self.value_states.append(value_state)
            self.proposed.append(proposed)
            self.value_proposed.append(value_proposed)
            self.accepted.append(accepted)
        else:
            if state !=None:
                self.states.append(state)
            if value_state != None:
                self.value_states.append(value_state)
            if proposed != None:
                self.proposed.append(proposed)
            if value_proposed != None:
                self.value_proposed.append(value_proposed)
            if accepted != None:
                self.accepted.append(accepted)
        
        if self.continous_output:
            self.continous_outputfile.write(str(len(self.states)) + " ")
            for i in state: 
                self.continous_outputfile.write(str(i) + " ")
            if accepted != None:
                self.continous_outputfile.write(str(accepted))
            self.continous_outputfile.write("\n")
        self.changed = True
        
    def append_record(self, tick, record):
        self.records.append([tick, record])

    def reset(self):
        self.states = []
        self.value_states = []
        self.proposed = []
        self.value_proposed = []
        self.accepted = []


    def get_best_values(self, n=1, max = True):
        '''
        TODO: returns the n best values of the chain
        '''
        raise NotImplementedError
        
           
    def convert_list_to_nparray(self):
        '''
        convert list of parameters to a 2-dim np-array
        '''
        self.statearray = np.array(self.states)
        self.proposalarray = np.array(self.proposed)
        self.accetancearray = np.array(self.accepted)
        self.statevaluearray = np.array(self.value_states)
        self.proposalvaluearray = np.array(self.value_proposed)
        self.changed = False
        #names = []
        #for i in range(length)
        #self.chainarray.dtype.names = ('x', 'y')
    

    def convert_nparray_to_list(self):
        '''
        convert list of parameters to a 2-dim np-array
        '''
        try:
            self.states = self.statearray.tolist()
        except:
            print "generic chain conversion error"
            self.states = []
        try:   
            self.proposed = self.proposalarray.tolist()
        except:
            print "generic chain conversion error"
            self.proposed = []
        try:
            self.accepted = self.accetancearray.tolist()
        except:
            print "generic chain conversion error"
            self.accepted = []
        try:
            self.value_states = self.statevaluearray.tolist()
        except:
            print "generic chain conversion error"
            self.value_states = []
        try:
            self.value_proposedself = self.proposalvaluearray.tolist()
        except:
            print "generic chain conversion error"
            self.value_proposed = []
            
    def save_data(self):
        '''
        @summary: saves current chain data to np-array files 
        '''
        try:
            folder = self.get_savepath()
            if len(self.states) > 0:
                np.savetxt(folder + "chain-states.dat", np.array(self.states)) 
            if len(self.value_states) > 0:
                np.savetxt(folder + "chain-statevalues.dat", np.array(self.value_states))  
            if len(self.proposed) > 0:
                np.savetxt(folder + "chain-proposal.dat", np.array(self.proposed))
            if len(self.value_proposed) > 0:
                np.savetxt(folder + "chain-proposalvalues.dat", np.array(self.value_proposed))
            if len(self.accepted) > 0:
                np.savetxt(folder + "chain-acceptance.dat", np.array(self.accepted)) 
            if len(self.records) > 0:
                filehandler = open(folder + "chain-records.dat", 'w') 
                pickle.dump(self.records, filehandler)
        except:
            # catch this warning to avoid cluster crashes
            warnings.warn("could not save state chains")    
 
    def load_data(self, path = None, file = "chain"):
        '''
        loads np array from file 
        '''
        if path == None:
            path = self.get_savepath()
        
        if os.path.exists((path + "\\" + file + "-states.dat")):
            self.statearray = np.loadtxt(path + "\\" +file + "-states.dat")
        else:
            print "states could't be loaded"
        if os.path.exists((path + "\\" + file + "-statevalues.dat")):
            self.statevaluearray = np.loadtxt(path + "\\" +file + "-statevalues.dat")
        else:
            print "statevalues could't be loaded"
        if os.path.exists((path + "\\" + file + "-proposal.dat")):
            self.proposalarray = np.loadtxt(path + "\\" +file + "-proposal.dat")
        else:
            print "proposal could't be loaded"
        if os.path.exists((path + "\\" + file + "-proposalvalues.dat")):
            self.proposalvaluearray = np.loadtxt(path + "\\" +file + "-proposalvalues.dat")  
        else:
            print "proposalvalues could't be loaded"
        if os.path.exists((path + "\\" + file + "-acceptance.dat")):
            self.accetancearray = np.loadtxt(path + "\\" +file + "-acceptance.dat")
        else:
            print "acceptance could't be loaded"         
        
        self.convert_nparray_to_list()  

            
    def plot_histograms(self, parameters=None):
        '''
        plot parameter histograms
        @param parameters: optional tuple or list of the parameters to be plotted 
        '''
        from matplotlib import pyplot 
        if parameters == None:
            parameters = range(len(self.states[1]))
        if self.changed:
            self.convert_list_to_nparray()
        for i in parameters:
            pyplot.figure()
            pyplot.title('Parameter' + str(i+1)) 
            pyplot.hist(self.statearray[:, i], normed = True, bins = 100)
        pyplot.draw()

    def plot_params(self, parameters=None,stitle=None):
        '''
        plot parameter histograms
        @param parameters: optional tuple or list of the parameters to be plotted 
        '''
        from matplotlib import pyplot 
        cdim = len(self.states[1])
        if parameters == None:
            parameters = range(cdim)
        if self.changed:
            self.convert_list_to_nparray()
        pyplot.figure(num=cdim) 
        if (stitle!=None): pyplot.title(stitle) 
        for i in parameters:
            pyplot.plot(self.statearray[:,i])
        pyplot.draw()

    def plot_correlation(self):
        '''
        plot all variables against all variables
        '''
        raise NotImplementedError

            
    def print_to_console(self, lower=None, upper=None):
        '''
        prints chain elements to console
        optional parameters are:
         - lower boundary
         - upper boundary
        uses the range function on a list, i.e. 
        0,10 give the first 10 list elements
        '''
        if (lower == None):
            lower = 0
        if (upper == None):
            upper = len(self.states)
        for i in range(lower, upper ):
            print("chainitem: " + str(i) + " State  " + str(self.states[i])) + " State_value  " + str(self.value_states[i]) +  " proposed  " + str(self.proposed[i]) +" value proposed  " + str(self.value_proposed[i]) +" accepted: "+str(self.accepted[i])

    def print_summary(self):
        print "========================================"
        print "chain summary"
        print "========================================"
        print "acceptancerate =" + str(self.get_acceptance_rate())


    def get_mean(self, lower=None, upper=None):
        '''
        @summary: returns an arary with the mean of the chain elements
        '''
        if (lower == None):
            lower = 0
        if (upper == None):
            upper = len(self.states)
        if self.changed:
            self.convert_list_to_nparray()
        mean = np.mean(self.statearray[lower:upper,:], axis=0)
        return mean

    def get_median(self, lower=None, upper=None):
        '''
        @summary: returns an arary with the median of the chain elements
        '''
        if (lower == None):
            lower = 0
        if (upper == None):
            upper = len(self.states)
        if self.changed:
            self.convert_list_to_nparray()
        median = np.median(self.statearray[lower:upper,:], axis=0)
        return median


    def get_std(self, lower=None, upper=None):
        '''
        @summary: returns an arary with the standarddeviation of the chain elements 
        '''
        if (lower == None):
            lower = 0
        if (upper == None):
            upper = len(self.states)
        if self.changed:
            self.convert_list_to_nparray()
        standarddeviation = np.std(self.statearray[lower:upper,:], axis=0)
        return standarddeviation 
 
    def get_mean_std(self, lower=None, upper=None):
        if (lower == None):
            lower = 0
        if (upper == None):
            upper = len(self.states)
        if self.changed:
            self.convert_list_to_nparray()
        standarddeviation = np.std(self.statearray[lower:upper,:], axis=0)
        mean = np.mean(self.statearray[lower:upper,:], axis=0)
        return mean, standarddeviation
      
    
    def get_covariance(self, lower=None, upper=None):
        '''
        calculates gradient around i-th element of the chain
        '''
        if (lower == None):
            lower = 0
        if (upper == None):
            upper = len(self.states)
        if self.changed:
            self.convert_list_to_nparray()
        return np.cov(np.transpose(self.statearray[lower:upper,:]))

    def get_acceptance_rate(self, lower=None, upper=None):
        if (lower == None):
            lower = 0
        if (upper == None):
            upper = len(self.accepted)
        assert (upper - lower) > 0
        sumacceptance = sum(self.accepted[lower:upper])
        return( sumacceptance /len(self.accepted[lower:upper]))

    
    def get_acceptance_per_dimension(self, lower=None, upper=None):
        if (lower == None):
            lower = 0
        if (upper == None):
            upper = len(self.states)
        assert (upper > lower)
        if self.changed:
            self.convert_list_to_nparray()    
            
        tmp1 = self.proposalarray[lower+1:upper,:]
        tmp2 = self.statearray[lower:upper-1,:]
        all = tmp1 != tmp2
        rejected = self.proposalarray[lower+1:upper,:] != self.statearray[lower+1:upper,:]
        return 1- np.sum(rejected, axis = 0) / np.sum(all, axis = 0)

        