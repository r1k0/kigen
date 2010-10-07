import os
import sys
import re
import subprocess
import logging

def process_pipe(cmd, verbose):
    """
    SINGLE Piped process launcher
    Automagically detects | and concatene into multiple lists
    
    @arg cmd		string

    @return: ret, output #, err
    """
    if verbose['set'] is True:
        print cmd
    cmd = cmd.split("|")
    logging.debug(cmd)

    cmdlines = [process.split() for process in cmd]

    p1 = subprocess.Popen(cmdlines[0], stdout=subprocess.PIPE)#, close_fds=True)
    p2 = subprocess.Popen(cmdlines[1], stdin=p1.stdout, stderr=p1.stdout)#, close_fds=True)
    ret2 = p2.wait()

    return ret2 , p2.stdout #, p2.stderr

def process_redir(cmd, verbose):
    """
    SINGLE Redir Piped process launcher
    Automagically detects > and concatene into multiple lists

    @arg cmd		string

    @return: ret, output #, err
    """
    if verbose['set'] is True:
        print cmd
    cmd = cmd.split(">")
    logging.debug(cmd)

    cmdlines = [process.split() for process in cmd]

    p = subprocess.Popen(cmdlines[0], stdout=subprocess.PIPE)#, close_fds=True)
    ret = p.wait()

    # FIXME single pass
    # does not loop else you passd multiple files
    for k in cmdlines[1]:
        f = open(k,'w')
        f.writelines(p.stdout)
        f.close

    return ret , p.stdout #, p.stderr

def process_append(cmd, verbose):
    """
    SINGLE Append Piped process launcher
    Automagically detects >> and concatene into multiple lists

    @arg cmd		string

    @return: ret, output #, err
    """
    if verbose['set'] is True:
        print cmd
    cmd = cmd.split(">>")
    logging.debug(cmd)

    cmdlines = [process.split() for process in cmd]

    p = subprocess.Popen(cmdlines[0],  stdout=subprocess.PIPE)#, close_fds=True)
    ret = p.wait()

    # FIXME single pass
    # does not loop else you passd multiple files
    for k in cmdlines[1]:
        f = open(k,'a')
        f.writelines(p.stdout)
        f.close

    return ret, p.stdout #, p2.stderr

# TODO rewrite me
# to detect and autosplit lists: impossible to do them all, gotta split in 3 functions
# | > >> < 
# sprocessors < >> > logic
# > -> stdout=open('whatever', 'wb'); >> -> stdout=open('whatever', 'ab'); < -> stdin=open('whatever', 'rb')
def process(cmd, verbose):
    """
    Single process launcher

    @arg cmd	string

    @return: ret, output #, err
    """
    if verbose['set'] is True:
        print cmd
    cmd = cmd.split()
    logging.debug(cmd)

    f = open(verbose['logfile'])
    p = subprocess.Popen(cmd , stdout=f) #, stderr=f) #, shell = True) # , close_fds=True)

    return p.wait() # , p.stdout #, p.stderr
