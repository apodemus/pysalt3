################################# LICENSE ##################################
# Copyright (c) 2009, South African Astronomical Observatory (SAAO)        #
# All rights reserved.                                                     #
#                                                                          #
# Redistribution and use in source and binary forms, with or without       #
# modification, are permitted provided that the following conditions       #
# are met:                                                                 #
#                                                                          #
#     * Redistributions of source code must retain the above copyright     #
#       notice, this list of conditions and the following disclaimer.      #
#     * Redistributions in binary form must reproduce the above copyright  #
#       notice, this list of conditions and the following disclaimer       #
#       in the documentation and/or other materials provided with the      #
#       distribution.                                                      #
#     * Neither the name of the South African Astronomical Observatory     #
#       (SAAO) nor the names of its contributors may be used to endorse    #
#       or promote products derived from this software without specific    #
#       prior written permission.                                          #
#                                                                          #
# THIS SOFTWARE IS PROVIDED BY THE SAAO ''AS IS'' AND ANY EXPRESS OR       #
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED           #
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE   #
# DISCLAIMED. IN NO EVENT SHALL THE SAAO BE LIABLE FOR ANY                 #
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL       #
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS  #
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)    #
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,      #
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN #
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE          #
# POSSIBILITY OF SUCH DAMAGE.                                              #
############################################################################

"""SALTFPEVELOCITY  It uses T. Williams code. 

Updates:

20100716
    * First wrote the code
"""

# Ensure python 2.5 compatibility


import os
import sys
import numpy as np
#import pyfits

from pyraf import iraf
from pyraf.iraf import pysalt
import saltsafekey
import saltsafeio
from . import fpsafeio
from saltsafelog import logging

import evelocity_wrapper2

debug=True

def saltfpevelocity(infile,existfit,xc,yc,rmax,logfile, verbose):  

    """XXX"""
        
# getting paths for filenames

    pathin = os.path.dirname(infile)
    basein = os.path.basename(infile)
    pathlog = os.path.dirname(logfile)
    baselog = os.path.basename(logfile)

    print(pathin, basein)
    
# start log now that all parameters are set up          
    with logging(logfile, debug) as log:

# Some basic checks, some tests are done in the FORTRAN code itself
# is the input file specified?
        saltsafeio.filedefined('Input',infile)

# if the input file is a file, does it exist? 
        if basein[0] != '@':
            saltsafeio.fileexists(infile)


# if a list is input throw an error
        if basein[0] == '@':
            raise SaltIOError(basein + ' list input instead of a file' )

# The file contains a list of images, check they exist
# format is 4x dummy lines, then a line/lines containing: x,y,wave0,sn,norm,dnorm,filename

        testfile= open(infile)
        print(testfile)
        for i in range(1, 5):
            line = testfile.readline()

        line = 'dummy'
        infiles=[]
        while (len(line.strip()) != 0):
            line = testfile.readline()
            if (len(line.strip()) > 0):
                linearray = line.split()
                infiles.append(linearray[6])

# check input files exist
        saltsafeio.filesexist(infiles,'','r')

# convert existfile to a one letter string
        if existfit == 'yes':
            existfit == 'y'
        else:
            existfit =='n'


# If all looks OK, run the FORTRAN code
    
        print(infile,  'input filename')
        print(existfit, xc, yc, rmax)

        evelocity_wrapper2.evelocity2(infile,existfit,xc,yc,rmax)

# -----------------------------------------------------------
# main code

parfile = iraf.osfn("saltfp$saltfpevelocity.par")
t = iraf.IrafTaskFactory(taskname="saltfpevelocity",value=parfile,function=saltfpevelocity,pkgname='saltfp')
