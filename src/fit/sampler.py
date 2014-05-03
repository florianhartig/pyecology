'''
Created on 02.02.2010

@summary: Contains Classes for sampling from specified distributions. If possible, classes are wrappers for scipy.stats functions, with a few convenience methods that are usually neede when using them as proposalgenerators for an MCMC 
@author: Florian Hartig http://florianhartig.wordpress.com/

'''
from __future__ import division
import numpy as np
from scipy import stats
import random
from abstract.base import Stochastic, Logable

class Abstract_Sampler(Stochastic, Logable):
    '''
    @summary: Abstract base class for samplers
    @note: self._proposalfunction needs to be implement to create a valid propsalgenerator. Some valid functions are already contained, e.g. _multivariate_normal 
    @param scale: scalar or 1d- array for scaling. Default scale for all distributions is is unit variance. 
    @param covariance: Covariance matrix to be applied to the samples
    @param dimension_proposal: optional function that chooses how many parameters to vary at a time. Must return an selection object of nparray, i.e. a int nparray or alike
    
    '''

    def __init__(self, scale = None, covariance = None, dimension_proposal=None, *args, **kwargs):
        '''
        Constructor
        '''
        Stochastic.__init__(self)
        self.tick=0
        self.set_covariance(covariance)
        self.set_scale(scale)
        self.prosalfunction = None
        self._lower = None
        self._upper = None
        self.dimensions_average = None
        self.dimensions_scale = 1
        self.set_dimension_proposal(dimension_proposal, kwargs)
        self.length = None
        self.add_to_log("init complete")
        self._proposal_correction_factor = 1 # for differnt scaling of the proposal generator 

    def _proposalfunction(self, x):
        '''
        pdf with mean 0 and unit variance
        needs to be implemented by deriving classes
        '''
        raise NotImplementedError

    def _propsal_preparator(self,x):
        '''
        @summary: help function - adjusts scale and covariance,
        selects dimensions if applicable
        
        @param x: np-array, proposal origin 
        '''
        proposal = self._proposalfunction(x)
        if self.covariance_decomposed != None:
            proposal = np.dot(self.covariance_decomposed, proposal)
        if self.scale != None:
            proposal = proposal * self.scale
        if x != None:
            proposal = proposal + x
        if self.dimension_proposal==None:
            return proposal
        else:
            out = x.copy()
            out = out.astype(np.float64)
            i = self.dimension_proposal(x)
            out[i] = proposal[i]
            return(out)

    
    def get_proposal(self, x=None, n=None):
        '''
        @summary: applies get proposal  n times. 
        @param x: current parameter, np-array like
        @param n: number of proposals to generate, int   
        @return: returns a list with the proposals
                
        @note: As it simply applies _proposalfunction n times, it always works,
        but it is not necessarily extremely efficient. For speed reasons,
        it may be sensible to overwrite this function in a derived class.
        
        '''
        if isinstance(x, list):
            self.length = len(x)
        elif isinstance(x, np.ndarray):
            self.length = np.size(x)
        else:
            self.length = 1

        if n == None:
            if self._lower == None and self._upper == None:
                return self._propsal_preparator(x)
            else:
                tick = 0
                while True:
                    tick +=1
                    if tick > 10000:
                        raise RuntimeError, "cannot find proposals inside given boundaries"
                    prop = self._propsal_preparator(x)
                    if not(np.any(prop < self._lower) or np.any(prop > self._upper)):
                        return prop
        elif n >= 0:
            out = []
            if self._lower == None and self._upper == None:
                for _ in xrange(n):
                    out.append(self._propsal_preparator(x))
            else:
                for _ in xrange(n):
                    tick = 0
                    while True:
                        tick +=1
                        if tick > 10000:
                            raise RuntimeError, "cannot find proposals inside given boundaries"
                        prop = self._propsal_preparator(x)
                        if not(self._lower != None and np.any(prop <= self._lower) or self._upper != None and np.any(prop >= self._upper)):
                            out.append(prop)
                            break
                            
            return out
        else:
            raise ValueError , "n needs to be larger or equal than 0"
        

    def get_scaling(self):
        if self.scale != None:
            return self.scale
        else:
            return self.covariance_decomposed

    def set_scale(self, scale=None):
        '''
        @summary: sets the scale of the proposalgenerator. 
        @param scale: scalar or 1-d np-array for scale. Default scaling corresponds to [1,1,1 ...1]. 
        '''
        if scale != None:
            try:
                self.scale = np.ravel(scale)
                
                self.add_to_log("scale set, see scale file")
            except:
                raise TypeError            
        else:
            self.scale = None
            self.add_to_log("scale set to None")
            
            
    def adjust_scale(self, scaling):
        '''
        @summary: sets new scale based on the old scale 
        @param scaling: scalar or 1-d np-array for scaling the scale. Default scaling corresponds to [1,1,1 ...1]. 
        '''
        newscale = self.scale * scaling
        self.set_scale(newscale)               
        
    def set_covariance(self, covariance=None):
        '''
        @summary: sets the covariance array covariance matrix. If 1-d array is give, a diagonal matrix is created
        '''
        if covariance != None:
            if np.ndim(covariance) == 1:
                covariance = np.diag(covariance)
            try:
                self.covariance_decomposed = np.linalg.cholesky(np.atleast_2d(covariance))
                self.save_covariance()
                self.add_to_log("covariance set, see covariance file")
            except:
                raise TypeError                      
        else:
            self.covariance_decomposed=None
            self.add_to_log("covariance set to None")
            
    def set_optimal_covariance(self, covariance , dimension_proposal_adjustment=True):
        '''
        @summary: sets optimal covariance from MC covariance matrix
        '''
        if (dimension_proposal_adjustment == True) & (self.dimension_proposal_covariance_correction!= None):
            scaling = 2.38*2.28 / self.dimension_proposal_covariance_correction
        else:    
            scaling = 2.38*2.28 / np.sqrt(np.size(covariance))
        self.set_covariance(covariance * scaling * self._proposal_correction_factor)


    def save_covariance(self, filename = None, path = None):
        '''
        @summary: saves decomposed covariance to file
        '''       
        filename = self.get_savepath(filename = filename, savepath = path, default = "sampler_covariance.txt")        
        if self.covariance_decomposed != None:
            np.savetxt(filename, self.covariance_decomposed)                 
        else:
            raise ValueError, "no covariance set" 

    def load_covariance(self, filename = None, path = None):
        '''
        @summary: loads decomposed covariance from file
        ''' 
        filename = self.get_savepath(filename = filename, savepath = path, default = "sampler_covariance.txt" )
        self.covariance_decomposed = np.loadtxt(filename)                 


    def load_undecomposed_covariance(self, filename = None):
        '''
        @summary: loads standard covariance matrix and sets sampler covariance to this
        @note: unlike load_covariance, load_undecomposed_covariance calls the set_covarinace function, which uses the cholesky decomp to calculate standard format
        ''' 
        self.set_covariance(np.loadtxt(filename)) 

            
    def set_boundaries(self, lower=None, upper=None):
        '''
        @summary: sets ABSOLUTE boundaries of the sampler, not relative to the current x value. Omitted values are set to none
        @param lower: lower boundary
        @param upper: upper boundary  
        @note: Boundaries should usually not be set when sampling proposals for MCMCs, this may destroy the convergence
        @note: Boundaries is implemented as a quick hack. Check the code, RuntimeError may be produced. 
        '''
        self._lower = lower
        self._upper = upper

    def set_dimension_proposal(self, dimension_proposal = None, kwargs=None):
        '''
        @summary: sets how many dimensions are varied at a time
        @param dimension_proposal: either None for all dimensions, a number for a fixed number of dimensions, or a function, or a string for a standard function
        
        '''        
        if dimension_proposal == None:
            self.dimension_proposal = None
            self.dimension_proposal_covariance_correction = None
        elif dimension_proposal == 'one_at_a_time':
            self.dimensions_average = 1
            self.dimension_proposal = self._dimensions_get_fixed_draw
            self.dimension_proposal_covariance_correction = 1
        elif type(dimension_proposal) == int:
            self.dimensions_average = dimension_proposal
            self.dimension_proposal = self._dimensions_get_fixed_draw
            self.dimension_proposal_covariance_correction = dimension_proposal
        elif self.dimension_proposal == 'exponential':
            self.dimension_proposal = self._dimensions_get_exponential_draw          
        elif self.dimension_proposal == 'logseries':
            self.dimension_proposal = self._dimensions_get_logseries_draw
        elif self.dimension_proposal == 'lognormal':
            self.dimension_proposal = self._dimensions_get_lognormal_draw
            if kwargs["sigma"] != None:
                self.dimensions_scale = kwargs["sigma"]
        else:
            raise TypeError
 
 
  
   
    def load_boundaries(self, path, usecols = None):
        '''
        @summary: loads a text file with the data for the prior
        '''
        self.data = np.loadtxt(path, usecols = usecols)
        self.set_boundaries(self.data[:,0], self.data[:,1])
 
   

    def _dimensions_draw_dimensions(self, x, n):
        '''
        @summary: return a random parameter index
        
        @param par: input parameter value of the proposal generator, works with 
        @type par: np-array, list, tupel
        @return: index, npint
        '''
        if n > len(x):
            n = len(x)
        return np.array(random.sample(range(len(x)), n))
        
    def _dimensions_get_fixed_draw(self,x):
        '''
        @summary: draws n=self.dimensions_average dimensions to vary.
        @param x: parameter that is varied
        @return: index, np int array
        '''        
        return self._dimensions_draw_dimensions(x, self.dimensions_average)
    
    def _dimensions_get_exponential_draw(self, x):
        '''
        @summary: draws n dimensions to vary, n drawn from exponential distribution with mean self.dimensions_average.
        @param x: parameter that is varied
        @return: index, np int array
        '''
        n = np.random.exponential(self.dimensions_average)
        n = np.ceil(n)
        return self._dimensions_draw_dimensions(x, n)
    
    def _dimensions_get_lognormal_draw(self, x):
        '''
        @summary: draws n dimensions to vary, n drawn from lognormal distribution with mean self.dimensions_average, sigma=self.dimensions_lognormal_draw_sigma.
        @param x: parameter that is varied
        @return: index, np int array
        '''
        n = np.random.lognormal(mean=self.dimensions_average, sigma=self.dimensions_scale )
        n = np.ceil(n)
        return self._dimensions_draw_dimensions(x, n)

    def _dimensions_get_logseries_draw(self, x):
        '''
        @summary: draws n dimensions to vary, n drawn from lognormal distribution with mean self.dimensions_average, sigma=self.dimensions_lognormal_draw_sigma.
        @param x: parameter that is varied
        @return: index, np int array
        TODO: proper mean integration
        '''
        p = 0.5
        n = np.random.logseries(p)
        print "experimental option logseries, not fully implemented yet"
        return self._dimensions_draw_dimensions(x, n)
    
    def get_latin_hypercube_sample(self, n):
        raise NotImplementedError
        

    
 

        

class Multivariate_Normal_Sampler(Abstract_Sampler):
    '''
    @summary: Creates multivariate normal samples

    @param scale: scalar or 1d- array for scaling. Default scale for all distributions is is unit variance. 
    @param covariance: Covariance matrix to be applied to the samples
    @param dimension_proposal: optional function that chooses how many parameters to vary at a time. Must return an selection object of nparray, i.e. a int nparray or alike
        '''
    def __init__(self, scale = None, covariance=None, dimension_proposal=None):
        '''
        Constructor
        '''
        Abstract_Sampler.__init__(self, scale = scale, covariance = covariance, dimension_proposal = dimension_proposal)
        self._proposalfunction = self._multivariate_normal

    def _multivariate_normal(self, x):
        return stats.norm.rvs(size = self.length)

                    
class Multivariate_Uniform_Sampler(Abstract_Sampler):
    '''
    @summary: Creates multivariate uniform proposals

    @param scale: scalar or 1d- array for scaling. Default scale for all distributions is is unit variance. 
    @param width: alternatively, the width (max - min) of the uniform may be specified 
    @param lower: alternatively, lower bound of the uniform distribution may be specified 
    @param upper: alternatively, upper bound of the uniform distribution may be specified
    @param covariance: Covariance matrix to be applied to the samples
    @param dimension_proposal: optional function that chooses how many parameters to vary at a time. Must return an selection object of nparray, i.e. a int nparray or alike
    '''
    def __init__(self, scale=None, covariance = None, dimension_proposal=None, width = None, lower = None, upper = None):
        
        Abstract_Sampler.__init__(self, covariance = covariance, dimension_proposal=dimension_proposal)
        self.set_scale(scale=None, width = None, lower = None, upper = None)
        self._proposalfunction = self._multivariate_uniform


    def set_scale(self, scale=None, dimension_proposal=None, width = None, lower = None, upper = None ):  
        '''
        @summary: sets the scale, or alternatively width or upper and lower bounds of the proposalgenerator. 
        @param scale: scalar or 1d- array for scaling. Default scale for all distributions is is unit variance. 
        @param width: alternatively, the width (max - min) of the uniform may be specified 
        @param lower: alternatively, lower bound of the uniform distribution may be specified 
        @param upper: alternatively, upper bound of the uniform distribution may be specified
        '''
        count = 0 
        if width != None:
            try:
                width = np.ravel(width)
            except:
                raise TypeError  
            self._unif_left = -width/2.0
            self._unif_scale = width
            self.scale = None
            count += 1
        if (lower != None or upper != None):
            assert lower != None and upper != None
            assert np.all(upper > lower)
            try:
                lower = np.ravel(lower)
                upper = np.ravel(upper)
            except:
                raise TypeError  
            self._unif_left = lower
            self._unif_scale = upper - lower
            self.scale = None    
            count += 1      
        if scale != None:
            try:
                self.scale = np.ravel(scale)
            except:
                raise TypeError     
            self._unif_left = - np.sqrt(12)/ 2.0
            self._unif_scale = np.sqrt(12)   
            count += 1       
        if count == 0:
            self.scale = None
            self._unif_left = - np.sqrt(12)/ 2.0
            self._unif_scale = np.sqrt(12) 
            count += 1 
        if count != 1: 
            raise ValueError, 'only one of either scale, width or lower and upper may be specified'

    
                
    def _multivariate_uniform(self, x):
        return stats.uniform.rvs( self._unif_left, self._unif_scale, size = self.length)
        

