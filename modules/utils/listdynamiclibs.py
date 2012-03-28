import os
import sys
import subprocess
import logging
import subprocess

def listdynamiclibs(binary, verbose):
    """
    Return a list of paths to dynamic libraries

    @arg:       binary    string

    @return:    dynlibs     list
    """
    if verbose['set'] is True:
        print(binary)
    cmd = []
    cmd.append('ldd')
    logging.debug(binary)

    cmd.append(binary)

    # p = subprocess.check_output(cmd)#, stdout=subprocess.PIPE) #, stderr=f) #, shell = True) # , close_fds=True)
    p = subprocess.getoutput(' '.join(cmd))
   
    logging.debug(p)

    dynlibs = []

    for i in p.split():
        if i.startswith('/lib'):
            dynlibs.append(i)
            
    logging.debug(binary + ' dynamic libraries found are:')
    logging.debug(dynlibs)

    return dynlibs
