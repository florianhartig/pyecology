'''
Created on 12.03.2010

@author: floha
'''


import time
import pp

   
job_server = pp.Server()
print "=============== pp server =========="
print "Starting pp on", job_server.get_ncpus(), "cores"



def wait_function(x):   
    time.sleep(x)
    return x

def option_1():
    '''
    all jobs are submitted, then results are called
    '''
    jobs = []
    results = []
    for i in xrange(5):
        jobs.append(job_server.submit(wait_function, args=(i,), depfuncs=(), modules=("time",)))
    for job in jobs:    
        results.append(job())
        
    print "==== result ======="
    print results
    print "==================="
    job_server.print_stats()

def option_2():
    '''
    jobs are submitted and results are called 
    -> this is blocking, see timing !!!
    '''
    results = []
    for i in xrange(5):
        job = job_server.submit(wait_function, args=(i,), depfuncs=(), modules=("time",))
        results.append(job())

    print "==== result ======="
    print results
    print "==================="
    job_server.print_stats()


if __name__ == '__main__':
    option_1()
    option_2()