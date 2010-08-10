import os
import sys
import re
import commands

# WARN don't use colors here

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
    # FIXME x86 for 32 and 64 or x86_64?
    uname = commands.getoutput('uname -m | sed -e "s:i[3-6]86:x86:"') #-e "s:x86_64:amd64:" -e "s:parisc:hppa:"')

    return uname

def identify_flavor():
    """
    Identify OS flavor

    @arg: none
    @return: string
    """
    flavor = 'unknown'
    gentoorelease  = '/etc/gentoo-release'
    sabayonrelease = '/etc/sabayon-edition'
    funtoorelease  = '/etc/funtoo-release'

    # funtoo overwrites /etc/gentoo-release we catch it anyway
    if os.path.isfile(gentoorelease):
        f = open(gentoorelease)
        flavor = f.readline()
        f.close()
    if os.path.isfile(sabayonrelease):
        f = open(sabayonrelease)
        flavor = f.readline()
        f.close()
    # FIXME wait for Funtoo update in baselayout to have /etc/funtoo-release
    # currently Funtoo overwrites /etc/gentoo-release
    elif os.path.isfile(funtoorelease):
        f = open(funtoorelease)
        flavor = f.readline()
        f.close()

    flavor = flavor.strip()

    return flavor

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
    # best way *here* is to get KV from the sources, not the running KV
    if not os.path.isfile(kerneldir+'/Makefile'):
        return 'none'
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
        if not os.path.isdir(portdir+'/distfiles'):
            os.mkdir(portdir+'/distfiles')
    else:
        # non Portage system
        portdir = temp['root']

    return portdir

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
    modules_config = master_config['MODULES_ATARAID']   \
            +' '+master_config['MODULES_DMRAID']    \
            +' '+master_config['MODULES_EVMS']  \
            +' '+master_config['MODULES_LVM']   \
            +' '+master_config['MODULES_MDADM']     \
            +' '+master_config['MODULES_PATA']  \
            +' '+master_config['MODULES_SATA']  \
            +' '+master_config['MODULES_SCSI']  \
            +' '+master_config['MODULES_WAITSCAN']  \
            +' '+master_config['MODULES_NET']   \
            +' '+master_config['MODULES_ISCSI']     \
            +' '+master_config['MODULES_FIREWIRE']  \
            +' '+master_config['MODULES_PCMCIA']    \
            +' '+master_config['MODULES_USB']   \
            +' '+master_config['MODULES_FS']

    return modules_config

def get_config_modules_dict(master_config):
    """
    Get configuration module dictionary

    @arg: dict
    @return: dict
    """
    modules_config = { 'MODULES_ATARAID': master_config['MODULES_ATARAID'], \
            'MODULES_DMRAID': master_config['MODULES_DMRAID'],  \
            'MODULES_EVMS': master_config['MODULES_EVMS'],      \
            'MODULES_LVM': master_config['MODULES_LVM'],        \
            'MODULES_MDADM': master_config['MODULES_MDADM'],    \
            'MODULES_PATA': master_config['MODULES_PATA'],      \
            'MODULES_SATA': master_config['MODULES_SATA'],      \
            'MODULES_SCSI': master_config['MODULES_SCSI'],      \
            'MODULES_WAITSCAN': master_config['MODULES_WAITSCAN'],  \
            'MODULES_NET': master_config['MODULES_NET'],        \
            'MODULES_ISCSI': master_config['MODULES_ISCSI'],    \
            'MODULES_FIREWIRE': master_config['MODULES_FIREWIRE'],  \
            'MODULES_PCMCIA': master_config['MODULES_PCMCIA'],  \
            'MODULES_USB': master_config['MODULES_USB'],        \
            'MODULES_FS': master_config['MODULES_FS'] }

    return modules_config
