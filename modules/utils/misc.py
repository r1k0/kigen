import os
import sys
import re
import subprocess

# WARN don't import logging here as it's not already declared in kigen

def failed(string):
    print(string)
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
    uname = subprocess.getoutput('uname -m | sed -e "s:i[3-6]86:x86:"') #-e "s:x86_64:amd64:" -e "s:parisc:hppa:"')

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

# FIXME broke due to python3
# http://stackoverflow.com/questions/1767513/read-first-n-lines-of-a-file-in-python
def get_kernel_version(kerneldir):
    """
    Get the kernel version number

    @arg: string
    @return: string
    """
    # best way *here* is to get KV from the sources, not the running KV
    if not os.path.isfile(kerneldir+'/Makefile'):
        return 'none'
    head = []
    nlines = 0
    for line in open(kerneldir+'/Makefile'):
        line = line.replace(' ','')
        head.append(line.rstrip())
        nlines += 1
        if nlines >= 5:
            break
    head = dict(item.split("=") for item in head )

    return head['VERSION']+"."+head['PATCHLEVEL']+"."+head['SUBLEVEL']+head['EXTRAVERSION'], head['NAME']

# DEPRECATED: I don't see a case where get_kernel_version() would break
# and we have the kernel nickname aka 'Flesh-Eating Bats with Fangs' for 2.6.37
#def get_kernel_utsrelease(kerneldir):
#    """
#    Get the kernel release number
#    
#    @arg: string
#    @return: string
#    """
#    
#    source = kerneldir + '/include/config/kernel.release'
#
#    if os.path.isfile(source):
#        utsrelease = os.popen('cat '+source).read().strip()
#        return utsrelease
#    else:
#        return get_kernel_version(kerneldir)

def is_static(binary_path):
    """
    Check if binary is statis or not

    @arg: string
    @return: bool
    """

    return os.system('LANG="C" LC_ALL="C" objdump -T $1 2>&1 | grep "not a dynamic object" >/dev/null')

def get_distdir(temp):
    """
    Get portage DISTDIR env var content
    will create /var/tmp/kigen/distfiles on non portage systems
    
    @arg: none
    @return: string
    """
    if os.path.isfile('/usr/bin/portageq'):
        distfiles = os.popen('portageq distdir').read().strip()
        if not os.path.isdir(distfiles):
            os.mkdir(distfiles)
    else:
        # non Portage system
        distfiles = temp['distfiles']

    return distfiles
    

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

def get_config_modules_list(modules_conf):
    """
    Get configuration module list

    @arg: dict
    @return: list
    """
    modules_config = modules_conf['MODULES_ATARAID']   \
            +' '+modules_conf['MODULES_DMRAID']    \
            +' '+modules_conf['MODULES_EVMS']  \
            +' '+modules_conf['MODULES_LVM']   \
            +' '+modules_conf['MODULES_MDADM']     \
            +' '+modules_conf['MODULES_PATA']  \
            +' '+modules_conf['MODULES_SATA']  \
            +' '+modules_conf['MODULES_SCSI']  \
            +' '+modules_conf['MODULES_WAITSCAN']  \
            +' '+modules_conf['MODULES_NET']   \
            +' '+modules_conf['MODULES_ISCSI']     \
            +' '+modules_conf['MODULES_FIREWIRE']  \
            +' '+modules_conf['MODULES_PCMCIA']    \
            +' '+modules_conf['MODULES_USB']   \
            +' '+modules_conf['MODULES_FS']   \
            +' '+modules_conf['MODULES_CRYPT']   \
            +' '+modules_conf['MODULES_MISC']   \
            +' '+modules_conf['MODULES_VIDEO']  

    return modules_config

def get_config_modules_dict(master_conf):
    """
    Get configuration module dictionary

    @arg: dict
    @return: dict
    """
    modules_config = { 'MODULES_ATARAID': master_conf['MODULES_ATARAID'], \
            'MODULES_DMRAID': master_conf['MODULES_DMRAID'],  \
            'MODULES_EVMS': master_conf['MODULES_EVMS'],      \
            'MODULES_LVM': master_conf['MODULES_LVM'],        \
            'MODULES_MDADM': master_conf['MODULES_MDADM'],    \
            'MODULES_PATA': master_conf['MODULES_PATA'],      \
            'MODULES_SATA': master_conf['MODULES_SATA'],      \
            'MODULES_SCSI': master_conf['MODULES_SCSI'],      \
            'MODULES_WAITSCAN': master_conf['MODULES_WAITSCAN'],  \
            'MODULES_NET': master_conf['MODULES_NET'],        \
            'MODULES_ISCSI': master_conf['MODULES_ISCSI'],    \
            'MODULES_FIREWIRE': master_conf['MODULES_FIREWIRE'],  \
            'MODULES_PCMCIA': master_conf['MODULES_PCMCIA'],  \
            'MODULES_USB': master_conf['MODULES_USB'],        \
            'MODULES_FS': master_conf['MODULES_FS'],        \
            'MODULES_CRYPT': master_conf['MODULES_CRYPT'],	\
            'MODULES_MISC': master_conf['MODULES_MISC'],	\
            'MODULES_VIDEO': master_conf['MODULES_VIDEO'] }

    return modules_config
