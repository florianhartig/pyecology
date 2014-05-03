'''
Created on 03.03.2010

@author: Florian Hartig http://florianhartig.wordpress.com/
'''

from scipy import inf
import numpy as np
import sampler
from abstract.base import Debugable

class Posterior(object):
    '''
    @summary: Generic Posterior function ... may be used as it is, or to derive 
    specialized posterior functions such as in parallel.parallel_python

    @param likelihood: likelihood function
    @param prior: prior function
    @param nll: working with negative log likelihoods?  
    '''
    
    def __init__(self, likelihood, prior = None, nll = False):
        '''
        constructor
        '''
        self.likelihood = likelihood
        self.prior = prior
        self.set_nll(nll)
        if prior == None:
            self.get_value = likelihood

    def get_value(self, x):
        '''
        @summary: gets posterior value given the current prior and likelihood functions of the class
        
        @param x: model / parameter value (should normally be convertible to np-array )
        '''
        if self.prior.get_value(x) == self.impossible:
            return self.impossible
        else: 
            if self.nll:
                return self.likelihood(x) + self.prior.get_value(x)
            else:
                return self.likelihood(x) * self.prior.get_value(x)

    def set_nll(self, nll = False):
        '''
        @summary: sets standard values for neutral and impossible values of the prior
        '''
        if nll:
            self.impossible = inf
            self.neutral = 0
            self._combine = self._combine_nll
        else:
            self.impossible = 0
            self.neutral = 1
            self._combine = self._combine_normal
        self.nll = nll
        assert self.prior.nll == self.nll
        
    def _combine(self, a, b):
        raise NotImplementedError
    
    def _combine_nll(self, a, b):
        return (a + b)

    def _combine_normal(self, a, b):
        return (a * b)
 
   
class Parallel_Posterior(Posterior):
    '''
    classdocs
    '''
    
    def __init__(self, likelihood, prior=None, nll = False):
        '''
        @summary: The sense of posterior is to help constructing the posterior and 
        to catch unneccessary model runs for the case that the prior returns 0 or inf
        @param likelihood: likelihood function
        @param prior: prior function
        @param nll: working with negative log likelihoods?   
        '''
        Posterior.__init__(self, likelihood=likelihood, prior=prior, nll=nll)
        if prior == None:
            self.get_value = likelihood

    def get_value(self, x, parallel = False):
        '''
        @summary: gets posterior value 
        
        @param x: parameter or list of parameters
        @param parallel: single or parallel run -> if parallel, x must be a list of parameters 
        '''
        if parallel:
            if isinstance(x, np.ndarray):
                x = x.tolist()
            assert isinstance(x,list)
            out = [0]*len(x)
            values_to_be_calculated = []
            index_to_be_calculated = []
            for i in xrange(len(x)):
                if self.prior.get_value(x[i]) == self.impossible:
                    out[i] = self.impossible
                else: 
                    values_to_be_calculated.append(x[i])
                    index_to_be_calculated.append(i)
            parallel_results = self.likelihood(values_to_be_calculated, parallel = True) 
            index_to_be_calculated.reverse()
            if self.nll:
                for j in index_to_be_calculated:
                    out[j] = parallel_results.pop() + self.prior.get_value(values_to_be_calculated.pop())
            else:
                for j in index_to_be_calculated:
                    out[j] = parallel_results.pop() * self.prior.get_value(values_to_be_calculated.pop())
            return out
        else:
            if self.prior.get_value(x) == self.impossible:
                return self.impossible
            else: 
                if self.nll:
                    return self.likelihood(x) + self.prior.get_value(x)
                else:
                    return self.likelihood(x) * self.prior.get_value(x)
   


     
        
class Prior(Debugable):
    '''
    Abstract base class for priors
    Needs to implement get_value!
    '''
    
    def __init__(self, nll = False):
        '''
        constructor
        '''
        self.set_nll(nll=nll)
        Debugable.__init__(self)
        
    def set_nll(self, nll = False):
        '''
        @summary: sets standard values for neutral and impossible values of the prior
        '''
        if nll:
            self.impossible = inf
            self.neutral = 0
        else:
            self.impossible = 0
            self.neutral = 1
        self.nll = nll
        
    def get_value(self, x):
        '''
        @summary: gets the prior value at parameter x
        '''
        raise NotImplementedError
    
    def _calculate_statistics(self):
        '''
        @summary: Can be implemented from the derived class to calculated some statistics 
        '''        
        self.mode = None
        self.mean = None
        raise NotImplementedError
    
    def _set_data(self, data):
        '''
        @summary: Generic setter for the properties of the prior
        '''
        raise NotImplementedError

    def _update_sampler(self):
        '''
        @summary: Should be implemented if the derived class implements a sampler to sample from the prior
        '''
        raise NotImplementedError

    def _load_data(self, path, usecols, selection = None):
        '''
        @summary: base implementation to loads a text file with the data for the prior
        '''
        self.data = np.loadtxt(path, usecols = usecols)
        if selection != None:
            self.data = self.data[selection.astype(bool),:]
        self._set_data(self.data)
        self._update_sampler()
        self._calculate_statistics()
   
    def load_data(self, path, usecols, selection = None):
        '''
        @summary: loads a text file with the data for the prior
        @param path: file path to a column organized textfile to be read by numpy
        @param usecols: columns in the text file  
        @param selection: np-array to select specific rows 
        @warning: This is the base implementation which requires a usecols parameter. Derived classes should implement a class specific default 
        '''
        self._load_data(path=path, usecols=usecols, selection=selection)



class Prior_Adapter(Prior):
    '''
    Adapter that can be used to create a prior object from a function to conform with the standard prior interface
    '''
    
    def __init__(self, priorfunction, nll=False):
        '''
        constructor
        '''
        Prior.__init__(self, nll)
        self.get_value = priorfunction
    


class Uniform_Prior(Prior):
    '''
    Uniform prior
    
    @param lower_boundaries: lower boundaries for model parameters, np array like
    @param upper_boundaries: upper boundaries for model paramters, np array like  
    '''
    
    def __init__(self, lower = -inf, upper = inf, nll=False, normalized = True):
        '''
        constructor
        '''
        Prior.__init__(self, nll)
        self.normalized = normalized
        self.set_boundaries(lower, upper)
        self.accept_boundary = True
        self.sampler = sampler.Multivariate_Uniform_Sampler(lower = lower, upper = upper)


            
    def set_boundaries(self, lower, upper):
        self.lower = np.ravel(lower)
        self.upper = np.ravel(upper)           
        if np.any(self.lower >= self.upper):
            raise ValueError, "lower boundaries of uniform prior are higher than upper boundaries"  
        if self.normalized:
            area = np.multiply.reduce(self.upper-self.lower)
            if area == np.Inf:
                area = self.neutral
            if self.nll:
                self.level = np.log(area)  # equals - log(1/area)
            else:
                self.level = 1/area
        else:
            self.level = self.neutral
        

            
    def _set_data(self, data, selection = None):
        lower = data[:,0]
        upper = data[:,1]
        self.set_boundaries(lower, upper)
        
    def _calculate_statistics(self):
        self.mean = (self.upper + self.lower)/2.0
        self.mode = self.mean
        
    def _update_sampler(self):
        '''
        @summary: updates the uniform sampler
        '''
        self.sampler.set_scale(lower = self.lower, upper = self.upper)
      
    def get_value(self, x):
        '''
        @summary: returns prior value for parameter x
        '''
        if self.accept_boundary:
            if np.any(x < self.lower) or np.any(x > self.upper):
                return self.impossible
            else:
                return self.level
        else:
            if np.any(x <= self.lower) or np.any(x >= self.upper):
                return self.impossible
            else:
                return self.level
    
    def load_data(self, path, usecols = (1,2,3), selection = None):
        '''
        @summary: loads a text file with the data for the prior
        @param path: file path to a column organized textfile to be read by numpy
        @param usecols: columns in the text file  
        @param selection: np-array to select specific rows 
        '''
        self._load_data(path=path, usecols=usecols, selection=selection)
            
            
class Triangular_Prior(Prior):
    '''
    @summary: Triangular prior class
    
    @param data: np array, data for the prior, columns: lower, upper, best, confidence
    @param nll: bool, negative log likelihood posterior  
    '''
    
    def __init__(self, data = None, nll=False):
        '''
        constructor
        '''
        Prior.__init__(self, nll)
        if data != None:
            self.data = data
            self.set_boundaries(self.data)

            
    def _set_data(self, array):
        self.lower = array[:,0]
        self.upper = array[:,1]
        assert (np.all(self.lower <= self.upper))
        self.best = array[:,2]
        assert (np.all(self.best <= self.upper) and np.all(self.best >= self.lower))      
        self.certainty = array[:,3]
        assert(np.all(self.certainty < 1) and np.all(self.certainty > 0))
      
    def get_value(self, x):
        '''
        return prior value
        Todo: implementation not efficient
        '''
        return NotImplementedError
