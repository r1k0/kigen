import os
import sys
import subprocess
import logging
import subprocess

def isstatic(binary, verbose):
    """
    Check if binary is statically or dynamically linked

    @arg binary    string

    @return: ret, output #, err
    """
    if verbose['set'] is True:
        print(binary)
    cmd = []
    cmd.append('file')
    logging.debug(binary)

    cmd.append(binary)

#    p = subprocess.check_output(cmd)#, stdout=subprocess.PIPE) #, stderr=f) #, shell = True) # , close_fds=True)
    p = subprocess.getoutput(' '.join(cmd))
   
    logging.debug(p)

    if 'dynamically' in p:
        return False
    elif 'statically' in p:
        return True
