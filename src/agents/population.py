'''
Created on 22.01.2010

@author: Florian Hartig http://florianhartig.wordpress.com/
'''

import agents

class Abstract_Population(object):
    '''
    classdocs
    '''
    

    def __init__(self, agentfactory, id=0):
        '''
        Constructor
        '''
        self.id = id
        self.agentfactory = agentfactory
        self.agents = []
        
    def create_agent(self):
        pass
    
    def get_population_size(self):
        return(len(self.agents))
               
class Non_Spatial_Population(Abstract_Population):
    '''
    classdocs
    '''

    def __init__(self, agentclass):
        '''
        Constructor
        '''
        Abstract_Population.__init__(agentclass)


class Spatial_Population(Abstract_Population):
    '''
    classdocs
    '''

    def __init__(self, agentclass):
        '''
        Constructor
        '''
        Abstract_Population.__init__(agentclass)


    