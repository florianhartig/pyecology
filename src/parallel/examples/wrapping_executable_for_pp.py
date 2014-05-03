'''
Created on 18.03.2010

@author: floha
'''

import pp

def execute(dummy):   
    '''
    execute is a function that gives a path to an arbitrary executable
    we assume here that this executable returns a value.
    of cour
    '''
    #add your executable here
    # out = os.system(executable)
    return(1)
    
def call_wrapped_exe(parameters):
    jobs = [job_server.submit(execute, args=(parameter,), depfuncs=(), modules=("os",)) for parameter in parameters] 
    results = [ job() for job in jobs]
    return results


if __name__ == '__main__':
    job_server = pp.Server()
    print "Started pp with", job_server.get_ncpus(), "workers"
    parameters = [0]*job_server.get_ncpus()
    for i in range(5):
        print call_wrapped_exe(parameters)
        job_server.print_stats()
    