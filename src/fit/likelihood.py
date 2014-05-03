
'''
Created on 25.03.2010

@author: Florian Hartig http://florianhartig.wordpress.com/
'''
from scipy import inf

import numpy as np
import traceback



def normal_likelihood(a, b, standarddeviation, standardized = False):
    '''
    @summary: goodness of fit function for total biomass or total basa area
    a,b, standarddeviation, are array - like
    @param standardized: if True, the values for a normalized Gaussian are returned, i.e. the integral is one ... usually, this is not needed in a Bayesian Analysis as long as the standard deviation doesn't change 
    '''
    if standarddeviation == 0.0:
        print "got std of 0"
        return inf
    else: 
        if standardized:
            return -np.log(np.power((np.sqrt(2 *np.pi) * standarddeviation ),-1) ) + np.power(((a - b)/standarddeviation),2.0)/2.0
            
        else:
            return np.power(((a - b)/standarddeviation),2.0)/2.0
    
    
    


def multivariate_normal_likelihood(a, b, standarddeviation = None, covariance = None, checkNaNofA = True):
    '''
    @summary: calculates likelihood of a difference between vector a and b based on multivariate normal density
    @param a, b: vectors to be compared, a is usually the data (because of check NaN properties) 
    @param standarddeviation: vector of standarddeviations 
    @param covariance: covariance matrix
    @param checkNaNofA    : check for NaN values in the data - this is erased from the calculations
    @note: either standarddeviation or covariance must be given, but not both.
    '''
    a = np.ravel(a)
    b = np.ravel(b)
    dimensions = np.size(a)
    
    assert((standarddeviation == None or covariance == None) and (standarddeviation != None or covariance != None))
   
    
    if standarddeviation != None:
        standarddeviation = np.ravel(standarddeviation)
        if np.size(standarddeviation) == 1 and np.size(a) > 1:
            standarddeviation = np.ones(np.shape(a)) * standarddeviation
        covariance = np.diag(standarddeviation)
    
    covariance = np.atleast_2d(covariance)
    
    # erase NaN input values
    if checkNaNofA :
        # had originally all inputs checked, but this created problems with some of the formind stuff, so this is commented out for the moment
        # might be reactivated later
        mask = np.logical_not(np.isnan(a)) #| np.isnan(b) | np.isnan(standarddeviation)
        dimensions = np.sum(mask) 
        covmask = np.outer(mask,mask)
        
        #maskindex=np.nonzero(covmask)
        a = a[mask]
        b = b[mask]
        covariance = covariance[covmask]
        covariance.shape=(dimensions,dimensions)
                

    try:
        inverse_cov = np.linalg.inv(covariance)
    except:
        print"covariance singular"
        return inf
    difference = a - b
#    if checkNaNofA:
#        out = np.ma.dot(np.ma.dot(difference, inverse_cov), difference.T)/2.0 
#        covariance = np.ma.compress_rowcols(covariance)
#        return (out - np.log(np.power(np.absolute(np.linalg.det(covariance)),-0.5) * np.power((2* np.pi), -dimensions/2.0))  )
#    else:
    out = np.dot(np.dot(difference, inverse_cov), difference.T)/2.0
    (sign, logdet) = np.linalg.slogdet(covariance) # robust det calculation
    covnor = 0.5 * logdet
    dimnorm = dimensions/2.0 * np.log(2* np.pi)        
    return (out + covnor + dimnorm )
