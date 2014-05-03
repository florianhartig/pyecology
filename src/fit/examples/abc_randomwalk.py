'''
Created on 27.01.2010

@author: floha
'''
import profile
import numpy as np 
import scipy
from scipy import stats
import matplotlib.pyplot as pyplot
from fit.mcmc import Marjoram_Like_ABC
from fit import sampler

class randomwalkmodel(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
    
    data = []
    datavariance = float
    numberwalks = int
    numbersteps = int
     
    def create_multiple_randomwalks(self, walks, steps, length):
        '''
        Creates and array with the end points of multiple random walks
        '''
        x = np.empty([walks])
        for i in xrange(walks):
            x[i] = sum((np.random.random_sample(steps) - 0.5) * length )
        return(x)
            
    def setdata(self, walks, steps, length):
        '''
        Creates test data
        '''
        self.data = self.create_multiple_randomwalks(walks, steps, length)
        self.numberwalks = walks
        self.numbersteps = steps
        self.datavariance = scipy.std(self.data)
         
    def plotdata(self):
        pyplot.hist(self.data, 100)
        pyplot.show()
    
    def get_acceptance_ABC(self, a):
        '''
        Creates test data
        '''
        x = self.create_multiple_randomwalks(self.numberwalks, self.numbersteps, a)
        if abs(scipy.std(x)- self.datavariance)< 0.1:
            return(True)
        else:
            return(False)
    
   

model = randomwalkmodel() 
model.setdata(10,10,1)
start = 1.1
proposal = sampler.Multivariate_Normal_Sampler(scale = 0.05)
abcsampler = Marjoram_Like_ABC(model.get_acceptance_ABC, start, proposal)

abcsampler.chain.debug = False
abcsampler.run(100000)
abcsampler.chain.plot_histograms([0])
print "finished"
pyplot.show()

#fit()
#profile.run('fit()')



