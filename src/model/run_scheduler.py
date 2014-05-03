'''
Created on 20.09.2010

@author: Florian Hartig http://florianhartig.wordpress.com/
'''

class Scheduler(object):
    '''
    classdocs
    '''


    def __init__(self, model, preprocessing=None, postprocessing=None):
        '''
        Constructor
        '''
        self.model = model
        self.preprocessing = preprocessing
        self.postprocessing = postprocessing
        
    def run(self, runlist):
        while runlist.len() > 0:
            pass
        