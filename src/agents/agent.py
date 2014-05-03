'''
Created on 22.01.2010

@author: Florian Hartig http://florianhartig.wordpress.com/
'''

class Generic_Agent(object):
    '''
    classdocs
    '''


    def __init__(self, id, population=None):
        '''
        Constructor
        '''
        self.id = id 
        self.population = population
        
        
    
class Spatial_Agent(Generic_Agent):
    '''
    classdocs
    '''


    def __init__(self, id, position, system = None):
        '''
        Constructor
        '''
        Generic_Agent.__init__(self, id)
        self.id = id 
        self.position = position
        self.system = system
    

class Fitness_Agent(Generic_Agent):
    '''
    classdocs
    '''
    

    def __init__(self, id, strategy=None, fitness=0):
        '''
        Constructor
        '''
        Generic_Agent.__init__(self, id)
        self.strategy = strategy
        self.fitness = fitness
    
    def update_fitness(self):
        self.fitness = self.strategy
        
        
        
        