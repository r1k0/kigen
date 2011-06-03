import os
import sys
import re
import subprocess
import logging
import glob

# FIXME rewrite me
# to detect and autosplit lists: I don't know how 
# to do them all in one function, gotta split in 3 functions

def process_pipe(cmd, verbose):
    """
    SINGLE Piped process launcher
    Automagically detects | and concatene into multiple lists
    
    @arg cmd		string

    @return: ret, output #, err
    """
    if verbose['set'] is True:
        print(cmd)
    cmd = cmd.split("|")
    logging.debug(cmd)

    cmdlines = [process.split() for process in cmd]

    p1 = subprocess.Popen(cmdlines[0], stdout=subprocess.PIPE)  #, close_fds=True)
    p2 = subprocess.Popen(cmdlines[1], stdin=p1.stdout)         #, stderr=p1.stdout)#, close_fds=True)
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
        print(cmd)
    cmd = cmd.split(">")
    logging.debug(cmd)

    cmdlines = [process.split() for process in cmd]

    p = subprocess.Popen(cmdlines[0], stdout=subprocess.PIPE)#, close_fds=True)
    ret = p.wait()

    # FIXME single pass
    # does not loop else you passd multiple files
    for k in cmdlines[1]:
        f = open(k,'wb')
        f.writelines(p.stdout)
        f.close

    logging.debug(p.stdout)

    return ret , p.stdout #, p.stderr

def process_append(cmd, verbose):
    """
    SINGLE Append Piped process launcher
    Automagically detects >> and concatene into multiple lists

    @arg cmd		string

    @return: ret, output #, err
    """
    if verbose['set'] is True:
        print(cmd)
    cmd = cmd.split(">>")
    logging.debug(cmd)

    cmdlines = [process.split() for process in cmd]

    p = subprocess.Popen(cmdlines[0],  stdout=subprocess.PIPE)#, close_fds=True)
    ret = p.wait()

    # FIXME single pass
    # does not loop else you passd multiple files
    for k in cmdlines[1]:
        f = open(k,'ab')
        f.writelines(p.stdout)
        f.close

    return ret, p.stdout #, p2.stderr

def process_star(cmd, verbose):
    """
    Single process launcher

    @arg cmd    string

    Handles a single start * :(
    Don't use for anything else than 'cp' or 'rm'
    """
    if verbose['set'] is True:
        print(cmd)

    cmd = cmd.split()

    if cmd[0] == 'cp':
        dest = cmd[-1]
        cmd.remove(dest)

    for i in cmd:
        # expand single *
        if i == '*':
            for j in glob.glob('*'):
                cmd.append(j)
            cmd.remove('*')
        # expand k* *k
        if '*' in i and i != '*':
            for k in glob.glob(i):
                cmd.append(k)
            cmd.remove(i)
   
    if cmd[0] == 'cp':
         cmd.append(dest)
    logging.debug(cmd)
    f = open(verbose['logfile'])
    p = subprocess.Popen(cmd , stdout=f) #, stderr=f) #, shell = True) # , close_fds=True)

    return p.wait() # , p.stdout #, p.stderr

# | > >> < 
# processes < >> > logic
# > -> stdout=open('whatever', 'wb'); >> -> stdout=open('whatever', 'ab'); < -> stdin=open('whatever', 'rb')
def process(cmd, verbose):
    """
    Single process launcher

    @arg cmd	string

    @return: ret, output #, err
    """
    if verbose['set'] is True:
        print(cmd)
    cmd = cmd.split()
    logging.debug(cmd)

    f = open(verbose['logfile'])
    p = subprocess.Popen(cmd , stdout=f) #, stderr=f) #, shell = True) # , close_fds=True)

    return p.wait() # , p.stdout #, p.stderr
