'''
Created on 01.02.2010

@author: floha
'''

import numpy as np 
import math
from scipy import stats
from matplotlib import pyplot
from fit import sampler, mcmc, bayesian
from parallel.parallel_python import *
import pp

print "================================="
print "start sampling expential function"
print "this example shows the use of the posterior class"
print "together with a parallel execution model, using parallel python"
print "for very fast likelihood models, parallel execution is considerably "
print "slower than linear because of communication overhead"
 
server = pp.Server()   
cores = server.get_ncpus()

def target(x):
    return math.exp(-x)
    
def likelihood(x, parallel=False):
    if parallel:
        jobs = [server.submit(target, (par,), modules = ("math",)) for par in x]
        out = [job() for job in jobs]
        return out
    else:
        return target(x)

prior = bayesian.Uniform_Prior(lower = 0)
post = bayesian.Parallel_Posterior(likelihood, prior, nll=False)

startvalue = 0.1
proposal = sampler.Multivariate_Normal_Sampler(scale = 1)

mcmcsampler = mcmc.Metropolis_Like_MCMC(post.get_value,startvalue, proposal, parallel_cores = cores)

mcmcsampler.run(5000)

server.print_stats()
print "====================================="
print("acceptancerate =" + str(mcmcsampler.chain.get_acceptance_rate()))
print "The number of MCMC steps done is: ", len(mcmcsampler.chain.states)
print "As the parallel mode creates new model runs just in case other runs are  "
print "rejected, the final number of mcmc steps depends stochastically on the acceptance rate"


#recalculates the model values, can be usefulf for stochastic models 
#mcmcsampler.recalculate = True
#mcmcsampler.run(5000)


mcmcsampler.chain.convert_list_to_nparray()
#plotting 
pyplot.figure(num=2) 
pyplot.plot(np.arange(-1,5,0.01), post.get_value(np.arange(-1,5,0.01), parallel=True))
pyplot.title("target distribution")
pyplot.hist(mcmcsampler.chain.statearray[:,0], bins=1000, normed=True)
pyplot.show()

