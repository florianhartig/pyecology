'''
Created on 21.10.2010

@author: Florian Hartig http://florianhartig.wordpress.com/
'''

class Borg:
    '''
    @summary: Implements the Borg pattern 
    '''
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state


class Singleton(object):
    '''
    @summary: Example of the Singleton pattern, can not be subclassed (at least not straightforwardly) 
    '''
    def __call__(self):
        return self


