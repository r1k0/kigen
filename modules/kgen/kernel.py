import os
import sys
from stdout import white, green, turquoise, red, yellow
import utils

# NOTE: if we add functions as methods
# we get TypeError: 'bool' object is not callable
# hence no methods

class kernel:

    def __init__(self, kerneldir, master_config, arch, KV, cli, verbose):

        self.kerneldir      = kerneldir
        self.master_config  = master_config
        self.arch           = arch
        self.KV             = KV
        self.verbose        = verbose
        self.dotconfig      = cli['dotconfig']
        self.mrproper       = cli['mrproper']
        self.allyesconfig   = cli['allyesconfig']
        self.allnoconfig    = cli['allnoconfig']
        self.menuconfig     = cli['menuconfig']
        self.oldconfig      = cli['oldconfig']
        self.quiet          = verbose['std']
        self.nomodinstall   = cli['nomodinstall']
        self.fakeroot       = cli['fakeroot']
        self.nosaveconfig   = cli['nosaveconfig']
        self.clean          = cli['clean']

    def build(self):
        """
        Build kernel
        """
        ret = zero = int('0')
        if self.dotconfig:
            # backup the previous .config found
            if os.path.isfile(self.kerneldir + '/.config'):
                from time import time
                copy_dotconfig(self.kerneldir + '/.config', self.kerneldir + '/.config.' + str(time()), self.quiet)
            # copy the custom .config
            copy_dotconfig(self.dotconfig, self.kerneldir + '/.config', self.quiet)
    
        if self.mrproper is True:
            ret = mrproper(self.kerneldir, self.KV, self.master_config, self.arch, self.quiet)
            if ret is not zero: self.fail('mrproper')
        if self.clean is True:
            ret = clean(self.kerneldir, self.KV, self.master_config, self.arch, self.quiet)
            if ret is not zero: self.fail('clean')
#        if self.allyesconfig is True:
#            ret = allyesconfig(self.kerneldir, self.KV, self.master_config, self.arch, self.quiet)
#            if ret is not zero: self.fail('allyesconfig')
#        elif self.allnoconfig is True:
#            ret = allnoconfig(self.kerneldir, self.KV, self.master_config, self.arch, self.quiet)
#            if ret is not zero: self.fail('allnoconfig')
        if self.oldconfig is True:
            ret = oldconfig(self.kerneldir, self.KV, self.master_config, self.arch, self.quiet)
            if ret is not zero: self.fail('oldconfig')
        if self.menuconfig is True or self.dotconfig is not '':
            ret = menuconfig(self.kerneldir, self.KV, self.master_config, self.arch, self.quiet)
            if ret is not zero: self.fail('menuconfig')
    
        # check for kernel .config
        if os.path.isfile(self.kerneldir+'/.config') is not True:
            raise error.fail(self.kerneldir+'/.config'+' does not exist.')
    
        # prepare
        ret = prepare(self.kerneldir, self.KV, self.master_config, self.arch, self.quiet)
        if ret is not zero: self.fail('prepare')
    
        # bzImage
        ret = bzImage(self.kerneldir, self.KV, self.master_config, self.arch, self.quiet)
        if ret is not zero: self.fail('bzImage')
    
        # modules
        # if --allnoconfig is passed, then modules are disabled
        if self.allnoconfig is not True:
            ret = modules(self.kerneldir, self.KV, self.master_config, self.arch, self.quiet)
            if ret is not zero: self.fail('modules')
            if self.nomodinstall is False:
                # modules_install
                ret = modules_install(self.kerneldir, self.KV, self.master_config, self.arch, self.quiet, self.fakeroot)
                if ret is not zero: self.fail('modules_install')
        # save kernel config
        if self.nosaveconfig is False:
            if os.path.isdir('/etc/kernels/'):
                utils.sprocessor('cp %s %s' % (self.kerneldir+'/.config', '/etc/kernels/dotconfig-kigen-'+self.arch+'-'+self.KV), self.verbose)
            else:
                utils.sprocessor('mkdir /etc/kernels', self.verbose)
                utils.sprocessor('cp %s %s' % (self.kerneldir+'/.config', '/etc/kernels/dotconfig-kigen-'+self.arch+'-'+self.KV), self.verbose)
            print green(' * saved ') + '/etc/kernels/dotconfig-kigen-'+self.arch+'-'+self.KV

    def fail(self, step):
        """
        @arg step   string

        @return     exit
        """
        print red('error')+': kernel.'+step+'() failed'
        sys.exit(2)

def copy_dotconfig(kernel_config, kerneldir, quiet):
    """
    Copy kernel .config file to kerneldir 
    (/usr/src/linux by default)

    @arg: string
    @arg: string
    @return: none
    """
    cpv = ''
    if quiet is '': cpv = '-v'
    print green(' * ') + turquoise('kernel.copy_config')
    if os.path.isfile(kernel_config):
        return os.system('cp %s %s %s' % (cpv, kernel_config, kerneldir))
    else:
        print red('ERR: ') + kernel_config + " doesn't exist."
        sys.exit(2)

# kernel building functions
def build_command(master_config, arch, target, quiet):
    """
    Kernel Makefile bash build command
    
    @arg: dict
    @arg: string
    @arg: string
    @arg: string
    @return: string
    """
    command = '%s %s CC="%s" LD="%s" AS="%s" ARCH="%s" %s %s' % (master_config['DEFAULT_KERNEL_MAKE'], \
                master_config['DEFAULT_MAKEOPTS'],      \
                master_config['DEFAULT_KERNEL_CC'],     \
                master_config['DEFAULT_KERNEL_LD'],     \
                master_config['DEFAULT_KERNEL_AS'],     \
                arch,                                   \
                target,                                 \
                quiet)
    return command

def mrproper(kerneldir, KV, master_config, arch, quiet):
    """
    Kernel command interface for mrproper
    
    @arg: string
    @arg: dict
    @arg: string
    @arg: string
    @return: bool
    """
    print green(' * ') + turquoise('kernel.mrproper ') + KV
    utils.chgdir(kerneldir)
    command = build_command(master_config, arch, 'mrproper', quiet)
    if quiet is '':
        print command
    return os.system(command)

def clean(kerneldir, KV, master_config, arch, quiet):
    """
    Kernel command interface for clean
    
    @arg: string
    @arg: dict
    @arg: string
    @arg: string
    @return: bool
    """
    print green(' * ') + turquoise('kernel.clean ') + KV
    utils.chgdir(kerneldir)
    command = build_command(master_config, arch, 'clean', quiet)
    if quiet is '':
        print command
    return os.system(command)

# TODO: should we add a sort of yes '' | make oldconfig?
def oldconfig(kerneldir, KV, master_config, arch, quiet):
    """
    Kernel command interface for oldconfig
    
    @arg: string
    @arg: dict
    @arg: string
    @arg: string
    @return: bool
    """
    print green(' * ') + turquoise('kernel.oldconfig ') + KV
    utils.chgdir(kerneldir)
    command = build_command(master_config, arch, 'oldconfig', '')
    if quiet is '':
        print command
    return os.system(command)

def allyesconfig(kerneldir, KV, master_config, arch, quiet):
    """
    Kernel command interface for allyesconfig
    
    @arg: string
    @arg: dict
    @arg: string
    @arg: string
    @return: bool
    """
    print green(' * ') + turquoise('kernel.allyesconfig ') + KV
    utils.chgdir(kerneldir)
    command = build_command(master_config, arch, 'allyesconfig', quiet)
    if quiet is '':
        print command
    return os.system(command)

def allnoconfig(kerneldir, KV, master_config, arch, quiet):
    """
    Kernel command interface for allnoconfig
    
    @arg: string
    @arg: dict
    @arg: string
    @arg: string
    @return: bool
    """
    print green(' * ') + turquoise('kernel.allnoconfig ') + KV
    utils.chgdir(kerneldir)
    command = build_command(master_config, arch, 'allnoconfig', quiet)
    if quiet is '':
        print command
    return os.system(command)

def menuconfig(kerneldir, KV, master_config, arch, quiet):
    """
    Kernel command interface for menuconfig
    
    @arg: string
    @arg: dict
    @arg: string
    @arg: string
    @return: bool
    """
    print green(' * ') + turquoise('kernel.menuconfig ') + KV
    utils.chgdir(kerneldir)
    command = build_command(master_config, arch, 'menuconfig', '')
    return os.system(command)

def prepare(kerneldir, KV, master_config, arch, quiet):
    """
    Kernel command interface for prepare
    
    @arg: string
    @arg: dict
    @arg: string
    @arg: string
    @return: bool
    """
    print green(' * ') + turquoise('kernel.prepare ') + KV
    utils.chgdir(kerneldir)
    command = build_command(master_config, arch, 'prepare', quiet)
    if quiet is '':
        print command
    return os.system(command)

def bzImage(kerneldir, KV, master_config, arch, quiet):
    """
    Kernel command interface for bzImage
    
    @arg: string
    @arg: dict
    @arg: string
    @arg: string
    @return: bool
    """
    print green(' * ') + turquoise('kernel.bzImage ') + KV
    utils.chgdir(kerneldir)
    command = build_command(master_config, arch, 'bzImage', quiet)
    if quiet is '':
        print command
    return os.system(command)

def modules(kerneldir, KV, master_config, arch, quiet):
    """
    Kernel command interface for modules
    
    @arg: string
    @arg: dict
    @arg: string
    @arg: string
    @return: bool
    """
    print green(' * ') + turquoise('kernel.modules ') + KV
    utils.chgdir(kerneldir)
    command = build_command(master_config, arch, 'modules', quiet)
    if quiet is '':
        print command
    return os.system(command)

def modules_install(kerneldir, KV, master_config, arch, quiet, fakeroot):
    """
    Kernel command interface for modules_install 
    
    @arg: string
    @arg: dict
    @arg: string
    @arg: string
    @return: bool
    """
    print green(' * ') + turquoise('kernel.modules_install ') + fakeroot + '/lib/modules/' + KV
    utils.chgdir(kerneldir)
    
    if fakeroot is not '':
        # export INSTALL_MOD_PATH 
        os.environ['INSTALL_MOD_PATH'] = fakeroot

    command = build_command(master_config, arch, 'modules_install', quiet)
    if quiet is '':
        print command
    return os.system(command)

