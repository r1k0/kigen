import os
import sys
import re
import commands
from stdout import green, turquoise, white, red, yellow
import subprocess
import logging

def failed(string):
    print string
    sys.exit(2)

def parse_config_file(filename):
    """
    Parse config file

    @arg: string
    @return: dict
    """
    options = {}
    f = open(filename)
    for line in f:
        # remove comments
        if '#' in line:
            # split on comment char, keep only the part before
            line, comment = line.split('#', 1)
        # find lines with an option=value
        if '=' in line:
            # split on option char
            option, value = line.split('=', 1)
            # strip spaces
            option = option.strip()
            value = value.strip()
            # store in dict
            options[option] = value
    f.close()
    return options # dict

def identify_arch():
    """
    Identifies hosting architecture

    @arg: none
    @return: string
    """
    # TODO test and improve identify_arch()
    # FIXME: x86 for 32 and 64 or x86_64?
    uname = commands.getoutput('uname -m | sed -e "s:i[3-6]86:x86:"') #-e "s:x86_64:amd64:" -e "s:parisc:hppa:"')
    return uname

def identify_os():
    """
    """
#    if os.path.isfile

    return

def chgdir(dir):
    """
    Change to directory

    @arg: string
    @return: none
    """
    if not os.path.isdir(dir):
        print red('ERR') + ': ' + 'cannot change dir to ' + dir
        sys.exit(2)
    if not os.getcwd() == dir:
        os.chdir(dir)

def copy_file(source, dest, quiet):
    """
    Copy file from to

    @arg: string
    @arg: string
    @arg: string
    @return: bool
    """
    cpv = ''
    if quiet is '': cpv = '-v'
    return os.system('cp %s %s %s' % (cpv, source, dest))

def get_kernel_version(kerneldir):
    """
    Get the kernel version number

    @arg: string
    @return: string
    """
    if not os.path.isdir(kerneldir):
        print red('ERR') + ': ' + kerneldir + ' does not exist.'
        sys.exit(2)
    # best way *here* is to get KV from the sources, not the running KV
    with open(kerneldir+'/Makefile') as file:
        # get first 4lines
        head = [file.next().replace(" ","") for x in range(4)]
    import  string
    head = map(string.strip, head)
    head = dict(item.split("=") for item in head )

    return head['VERSION']+"."+head['PATCHLEVEL']+"."+head['SUBLEVEL']+head['EXTRAVERSION']

def is_static(binary_path):
    """
    Check if binary is statis or not

    @arg: string
    @return: bool
    """
    return os.system('LANG="C" LC_ALL="C" objdump -T $1 2>&1 | grep "not a dynamic object" >/dev/null')

def get_portdir(temp):
    """
    Get portage PORTDIR env var content
    will create /var/tmp/kigen/distfiles on non portage systems

    @arg: none
    @return: string
    """
    if os.path.isfile('/usr/bin/portageq'):
        portdir = os.popen('portageq envvar PORTDIR').read().strip()
    else:
        # non Portage system
        portdir = temp['root']
    return portdir

def spprocessor(cmd, verbose):
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

def srprocessor(cmd, verbose):
    """
    SINGLE Redir Piped process launcher
    Automagically detects | and concatene into multiple lists

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

def arprocessor(cmd, verbose):
    """
    SINGLE Append Piped process launcher
    Automagically detects | and concatene into multiple lists

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
# to detect and autosplit lists
# | > >> < 
# sprocessors < >> > logic
# > -> stdout=open('whatever', 'wb'); >> -> stdout=open('whatever', 'ab'); < -> stdin=open('whatever', 'rb')
def sprocessor(cmd, verbose):
    """
    Single process launcher

    @arg cmd	string

    @return: ret, output #, err
    """
    if verbose['set'] is True:
        print cmd
    cmd = cmd.split()
    logging.debug(cmd)

    # TODO pass logfile
    f = open('/var/log/kgen.log')
    p = subprocess.Popen(cmd , stdout=f) #, shell = True) # , close_fds=True)

    return p.wait() # , p.stdout #, p.stderr

def get_sys_modules_list(KV):
	"""
	Get system module list

	@arg: string
	@return: list
	"""
	modlist = []
	moddir  = '/lib/modules/'+KV
	
	for root, subfolders, files in os.walk(moddir):
		for file in files:
			if re.search(".ko", file):
				modlist.append(file)
	return modlist

def get_config_modules_list(master_config):
	"""
	Get configuration module list

	@arg: dict
	@return: list
	"""
	modules_config = master_config['MODULES_ATARAID'] 	\
			+' '+master_config['MODULES_DMRAID'] 	\
			+' '+master_config['MODULES_EVMS'] 	\
			+' '+master_config['MODULES_LVM'] 	\
			+' '+master_config['MODULES_MDADM'] 	\
			+' '+master_config['MODULES_PATA'] 	\
			+' '+master_config['MODULES_SATA'] 	\
			+' '+master_config['MODULES_SCSI'] 	\
			+' '+master_config['MODULES_WAITSCAN'] 	\
			+' '+master_config['MODULES_NET'] 	\
			+' '+master_config['MODULES_ISCSI'] 	\
			+' '+master_config['MODULES_FIREWIRE'] 	\
			+' '+master_config['MODULES_PCMCIA'] 	\
			+' '+master_config['MODULES_USB'] 	\
			+' '+master_config['MODULES_FS']
	return modules_config

def get_config_modules_dict(master_config):
	"""
	Get configuration module dictionary

	@arg: dict
	@return: dict
	"""
	modules_config = { 'MODULES_ATARAID': master_config['MODULES_ATARAID'], \
			'MODULES_DMRAID': master_config['MODULES_DMRAID'], 	\
			'MODULES_EVMS': master_config['MODULES_EVMS'], 		\
			'MODULES_LVM': master_config['MODULES_LVM'], 		\
			'MODULES_MDADM': master_config['MODULES_MDADM'], 	\
			'MODULES_PATA': master_config['MODULES_PATA'], 		\
			'MODULES_SATA': master_config['MODULES_SATA'], 		\
			'MODULES_SCSI': master_config['MODULES_SCSI'], 		\
			'MODULES_WAITSCAN': master_config['MODULES_WAITSCAN'], 	\
			'MODULES_NET': master_config['MODULES_NET'], 		\
			'MODULES_ISCSI': master_config['MODULES_ISCSI'], 	\
			'MODULES_FIREWIRE': master_config['MODULES_FIREWIRE'], 	\
			'MODULES_PCMCIA': master_config['MODULES_PCMCIA'], 	\
			'MODULES_USB': master_config['MODULES_USB'], 		\
			'MODULES_FS': master_config['MODULES_FS'] }
	return modules_config
