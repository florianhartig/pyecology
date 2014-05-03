'''
Created on 11.02.2010

@author: Florian Hartig
'''

print "Diagonsis File for pyecology"
print "=========================================="
import sys
print "sys.path=", sys.path
print "version", sys.version

print "======== checking essential packages ======="


try:
	import numpy
	print "numpy version " + str(numpy.version.version) +  " installed"
	print "for full compatibility, 1.4 and higher should be used"
except ImportError:
	"numpy is lacking, pyecology won't work"

try:
	import scipy
	print "scipy version " + str(scipy.version.version) +  " installed"
except ImportError:
	"numpy is lacking, pyecology won't work"


print "======== checking non - essential packages ======="

try:
	import matplotlib
	print "matplotlib installed"
except ImportError:
	"parallel python is lacking, some features of pyecology won't work"

try:
	import pp
	print "parallel python installed"
except ImportError:
	"parallel python is lacking, some features of pyecology won't work"


print "========== other information =================="
print
print "builtin modules", sys.builtin_module_names

print "operation system information:"
import os
print "os.onviron", os.environ