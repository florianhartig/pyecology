'''
Created on 15.03.2010

@author: floha
'''

'''
Created on 14.03.2010

@author: floha
'''

from scipy import stats
from matplotlib import pyplot
from fit import sampler, bayesian
from fit.annealing import Simmulated_Annealing
from fit.bayesian import Parallel_Posterior
from parallel.parallel_python import *
import pp
import time

print "================================="
print "optimizing 1d-nomal function"
print "Examples shows basic use of the simmulated annealing "
print "time per run is: "


single_execution_time = 0.01

server = pp.Server()   
cores = server.get_ncpus()

def target(x):
    #return 0
    time.sleep(0.01)
    return stats.norm.pdf(x)

def priorfunction(x):
    if (np.min(x) < 0.0):
        return(0.0)
    else:
        return(1.0)
    
def likelihood(x, parallel=False):
    if parallel:
        jobs = [server.submit(target, (par,), depfuncs=(), modules = ("scipy","scipy.stats","time")) for par in x]
        out = [job() for job in jobs]
        return out
    else:
        return stats.norm.pdf(x)

prior = bayesian.Prior_Adapter(priorfunction, nll=False)
post = Parallel_Posterior(likelihood, prior, nll=False)



startvalue = 2
proposal = sampler.Multivariate_Normal_Sampler(scale = 0.4)

optimizer = Simmulated_Annealing(post.get_value, startvalue, proposal, parallel_cores=cores)
optimizer.temperature_decay = 0.02
optimizer.temperature = 1

print "========================================"
print "single core execution"

optimizer.parallel_cores = 1
optimizer.run(300)
server.print_stats()

print "========================================"
print "multi-core execution"
optimizer.parallel_cores = cores
optimizer.run(300)
server.print_stats()

print "========================================"
print "notice the difference in difference in runtime "
print "(time is counted from the beginning of the scipt)"
print "========================================"


print "best value", optimizer.best_parameter
optimizer.chain.convert_list_to_nparray()
#plotting 
pyplot.figure(num=2) 
pyplot.plot(10 * np.exp(- optimizer.temperature_decay * np.arange(1,len(optimizer.chain.states),1)))
pyplot.plot(optimizer.chain.statearray[:,0])
pyplot.show()



if __name__ == '__main__':
    pass