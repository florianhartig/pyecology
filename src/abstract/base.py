'''
Created on 16.03.2010

@author: Florian Hartig http://florianhartig.wordpress.com/
'''

import numpy as np
import time, os , cPickle
from pattern import Borg

class Shared(Borg):
    '''
    @summary: Borg class that collects shared variables
    '''    
    def __init__(self):
        Borg.__init__(self)



class Saveable(object):
    '''
    @summary: PyEcology - Abstract base class that should be implemented by all
    objects that save data
    @param savepath: class specific folder for data saved by the class
    @param globalsavepath: Global path that is shared by all classes 
    @warning: Changing globalsavepath will affect all running pyecology classes  
    '''    
    def __init__(self, savepath=None, globalsavepath = None):
        self.shared = Shared()
        if globalsavepath == None:
            try:
                self.shared.global_save_path
            except:
                globalsavepath = os.getcwd() + "\\output"
        if savepath == None:
            savepath = self.__class__.__name__ + str(id(self))
        self.set_savepath(savepath = savepath, globalsavepath = globalsavepath)
            

    def set_savepath(self, savepath=None, globalsavepath=None):
        '''
        @param savepath: class specific folder for data saved by the class
        @param globalsavepath: Global path that is shared by all classes 
        @warning: Changing globalsavepath will affect all running pyecology classes  
        '''
        if savepath != None:
            self._savepath = savepath 
        if globalsavepath!=None:
            self.shared.global_save_path = globalsavepath    
        if not os.path.exists(self.get_savepath()):
            os.makedirs(self.get_savepath())


    def get_savepath(self, filename=None, savepath =None, default = None):
        '''
        @summary: returns the save path
        @param filename: if filename is specified, returns savepath + filename as one string  
        @param savepath: optional, savepath of the file
        @param default: optional, for use in other classes if one wants to call the function with a default  
        '''        
        # no default file name set
        if default==None:
            if savepath == None:
                if filename == None:
                    return(os.path.join(self.shared.global_save_path, self._savepath) + "\\")
                else:
                    return os.path.join(self.shared.global_save_path, self._savepath, filename)
            else:
                if filename == None:
                    raise ValueError, "not all three parameters can be None"
                else:
                    return os.path.join(savepath, filename)
        
        # default file name set, this option is usually only used for other 
        else:
            if savepath == None:
                if filename == None:
                    return(os.path.join(self.shared.global_save_path, self._savepath, default))
                else:
                    return(os.path.join(self.shared.global_save_path, self._savepath, filename))
            else:
                if filename == None:
                    return(os.path.join(savepath, default))
                else:
                    return(os.path.join(savepath, filename))

            
# TODO: add code to print svn revision number to savepath        
#        revision = 0
#        fileRev = popen("svn info .", "r")
#        for line in fileRev:
#            if 'Revision' in line:
#             revision = match("Revision: (\d+)", line).group(1) 
#        
#        os.path.abspath(__file__)
                    
    def pickle(self, savepath = None, filename = None):
        '''
        @summary: tries to pickle class information
        @param savepath: optional, savepath
        @param filename: filename, optional, default is "pickled.txt"
        '''
        filename = self._create_default_savepath("classpickle.txt", savepath, filename)
        raise NotImplementedError    
        #try:
            #cpickle()
        #except:
            #try:
                #pickle:
            #except:
                
    
    def save_classdata(self):
        '''
        TODO: svn info
        '''
        f = file.open(self._savepath  + "classdata.txt", "wb")
        f.write("")
        f.close()
        raise NotImplementedError


    def _create_default_savepath(self, default, savepath = None, filename = None):
        '''
        @summary: help function to create get a savepath with "default" behavior
        @param default: default file name
        @param savepath: savepath, default is the class savepath
        @param filename: filename, if None default is used 
        '''
        if savepath == None:
            if filename == None:
                filename = self.get_savepath(default)
            else:
                filename = self.get_savepath(filename)
        else:
            if filename == None:
                filename = os.path.join(savepath, default)
            else:
                filename = os.path.join(savepath, filename)


class Debugable(object):
    '''
    @summary: PyEcology - Abstract class for classes that offer debug switch
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.debug = False
        '''
        turns debugging options for the chosen class on
        '''

              
class Stochastic(Saveable):
    '''
    @summary: PyEcology - Abstract base class that should be implemented by all
    stochastic objects
    '''
  
    def __init__(self):
        '''
        Constructor
        '''
        Saveable.__init__(self)
        try: 
            self.shared.RNG_initialized
        except:
            self.shared.RNG_initialized = True
            self.save_random_seed()
    
    def load_random_seed(self, filename=None):
        '''
        @summary: loads pickled random seed
        @param filename: full filename of pickled random seed, default is self.get_savepath() + "randomseed-pickle.txt"
        '''
        if filename == None:
            filename = self.get_savepath() + "randomseed-pickle.txt"
        f = open(filename, 'r')
        seed = cPickle.load(f)
        f.close()
        self.set_random_seed(seed)

    def set_random_seed(self, seed):
        '''
        @summary: sets the random seed
        '''
        np.random.set_state(seed)

    def get_random_seed(self):
        '''
        @summary: returns the random seed
        '''
        return np.random.get_state()
    
    def save_random_seed(self, filename=None):
        '''
        @summary: saves pickled random seed
        @param filename: full filename of pickled random seed, default is self.get_savepath() + "randomseed-pickle.txt"
        '''
        if filename == None:
            filename = self.get_savepath() + "randomseed-pickle.txt"
        seed = self.get_random_seed()
        f = open(filename, 'w')
        cPickle.dump(seed, f)
        f.close() 
#        f = open(self.get_savepath() + "randomseed-readable.txt", 'w')
#        f.write(str(seed))
#        f.close() 

class Logable(Saveable):
    '''
    @summary: PyEcology - Abstract base class that implements a log procedure
    TODO: umstellen auf python logging module
    '''    
    def __init__(self, savepath = None, globalsavepath = None):
        Saveable.__init__(self, savepath, globalsavepath)     
        self._start_new_log()             
        
    def _start_new_log(self, message = None):
        f = open(self.get_savepath() + 'logfile.txt' , 'w')
        f.write('============================\n' )
        f.write('Log started at ' + time.strftime("%a, %d %b %Y %H:%M:%S ", time.gmtime()) + '\n')
        if message != None:
            f.write(message+"\n")
        f.write('============================\n' )
        f.close
        
                       
    def add_to_log(self, message, metadata = True, echo = False):
        '''
        @summary: adds message to logfile. 
        @param message: log message
        @param metadata: If True (default), Time is added
        @param echo: If True, log message is printed to console 
        '''
        message = str(message)
        f = open(self.get_savepath() + 'logfile.txt', 'a')
        if metadata:
            f.write('=== Log entry at ' + time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime()) + '===\n' )
        f.write(message+"\n")
        f.close
        if echo:
            print message

        
class Pickleable(Saveable):
    '''
    @summary: PyEcology - Abstract base class that implements a pickel functionality
    '''    
    def __init__(self, savepath = None):
        Saveable.__init__(self, savepath)     
        self._start_new_log()         
        raise NotImplementedError


    def save_picklefile(self, filename):
        raise NotImplementedError
        
    
class Observable(object):
    '''
    @summary: to be inherited by classes that should be made observable
    '''
    def __init__(self):
        self._observers = []
    
    def attach_observer(self, observer):
        if not observer in self._observers:
            self._observers.append(observer)
    
    def detach_observer(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass
    
    def notify_observers(self, modifier=None):
        for observer in self._observers:
            if modifier != observer:
                observer.update(self)


class Observer(object):
    '''
    @summary: abstract class, to be inherited by classes that are observers
    '''
    def __init__(self):
        pass
    
    def update(self, Obserable):
        raise NotImplementedError
                
                
