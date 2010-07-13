import os
import sys
from stdout import white, green, turquoise, red, yellow
import utils

class kernel:

    def __init__(self, kerneldir, master_config, arch, KV, cli, verbose):

        self.kerneldir      = kerneldir
        self.master_config  = master_config
        self.arch           = arch
        self.KV             = KV
        self.verbose        = verbose
        self.dotconfig      = cli['dotconfig']
        self.mrproper       = cli['mrproper']
        self.allnoconfig    = cli['allnoconfig']
        self.menuconfig     = cli['menuconfig']
        self.oldconfig      = cli['oldconfig']
        self.quiet          = verbose['std']
        self.nomodinstall   = cli['nomodinstall']
        self.fakeroot       = cli['fakeroot']
        self.nosaveconfig   = cli['nosaveconfig']
        self.clean          = cli['clean']
        self.initramfs      = cli['initramfs']

    def build(self):
        """
        Build kernel
        """
        ret = zero = int('0')
        if self.dotconfig:
            # backup the previous .config if found
            if os.path.isfile(self.kerneldir + '/.config'):
                from time import time
                self.copy_config(self.kerneldir + '/.config', self.kerneldir + '/.config.' + str(time()))

            # copy the custom .config
            self.copy_config(self.dotconfig, self.kerneldir + '/.config')
    
        if self.mrproper is True:
            ret = make_mrproper()
            if ret is not zero: self.fail('mrproper')
        if self.clean is True:
            ret = make_clean()
            if ret is not zero: self.fail('clean')

# TODO
# check for --initramfs cli here
        if self.initramfs is not '':
            # check for CONFIG_INITRAMFS_SOURCE="cli['initramfs']" in .config
#            print green(' * ') + turquoise('kernel.append_config ') + 'CONFIG_INITRAMFS_SOURCE="'+self.initramfs+'"'
#            file(self.kerneldir + '/.config', 'a').writelines('CONFIG_INITRAMFS_SOURCE="%s"\n' % self.initramfs)
            file(self.kerneldir + '/.config', 'a').writelines('CONFIG_INITRAMFS_SOURCE="/usr/src/initramfs"\n')
            # TODO
            # copy self.initramfs to kerneldir+'/usr/initramfs_data.cpio' and gzip -d the file
            utils.sprocessor('cp %s %s/usr/initramfs_data.cpio.gz' % (self.initramfs, self.kerneldir), self.verbose)
            # gzip -d
            utils.sprocessor('gzip -d %s/usr/initramfs_data.cpio.gz' % self.kerneldir, self.verbose)
            # then extract cpio
# create /usr/src/initramfs/
            os.system('mkdir -p /usr/src/initramfs')
            os.system('cp %s/usr/initramfs_data.cpio /usr/src/initramfs/ ' % self.kerneldir)
            self.chgdir('/usr/src/initramfs/')
            os.system('cpio -id < initramfs_data.cpio')

        if self.oldconfig is True:
            ret = self.make_oldconfig()
            if ret is not zero: self.fail('oldconfig')
        if self.menuconfig is True:
            ret = self.make_menuconfig()
            if ret is not zero: self.fail('menuconfig')
    
        # check for kernel .config (gotta be sure)
        if os.path.isfile(self.kerneldir+'/.config') is not True: self.fail(self.kerneldir+'/.config'+' does not exist.')

        # prepare
        ret = self.make_prepare()
        if ret is not zero: self.fail('prepare')
    
        # bzImage
        ret = self.make_bzImage()
        if ret is not zero: self.fail('bzImage')
    
        # modules
        # if --allnoconfig is passed, then modules are disabled
        if self.allnoconfig is not True:
            ret = self.make_modules()
            if ret is not zero: self.fail('modules')
            if self.nomodinstall is False:
                # modules_install
                ret = self.make_modules_install()
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

    def chgdir(self, dir):
        """
        Change to directory
    
        @arg: string
        @return: none
        """
        if not os.path.isdir(dir):
            print red('error') + ': ' + 'cannot change dir to ' + dir
            sys.exit(2)
        if not os.getcwd() == dir:
            os.chdir(dir)

    def copy_config(self, source, dest): #, self.dotconfig, self.kerneldir + '/.config', self.quiet):
        """
        Copy kernel .config file to kerneldir 
        (/usr/src/linux by default)
    
        @arg: string
        @arg: string
        @return: none
        """
        cpv = ''
        if self.quiet is '': cpv = '-v'
        print green(' * ') + turquoise('kernel.copy_config') + ' ' + source + ' -> ' + dest
        if os.path.isfile(source):
            return os.system('cp %s %s %s' % (cpv, source, dest))
        else:
            print red('error: ') + source + " doesn't exist."
            sys.exit(2)

    # kernel building functions
    def build_command(self, target, verbose): #master_config, arch, target, quiet):
        """
        Kernel Makefile bash build command
        
        @arg: dict
        @arg: string
        @arg: string
        @arg: string
        @return: string
        """
        command = '%s %s CC="%s" LD="%s" AS="%s" ARCH="%s" %s %s' % (self.master_config['DEFAULT_KERNEL_MAKE'], \
                    self.master_config['DEFAULT_MAKEOPTS'],     \
                    self.master_config['DEFAULT_KERNEL_CC'],    \
                    self.master_config['DEFAULT_KERNEL_LD'],    \
                    self.master_config['DEFAULT_KERNEL_AS'],    \
                    self.arch,                                  \
                    target,                                     \
                    verbose)

        return command

    def make_mrproper(self): #kerneldir, KV, master_config, arch, quiet):
        """
        Kernel command interface for mrproper
        
        @return: bool
        """
        print green(' * ') + turquoise('kernel.mrproper ') + self.KV
        self.chgdir(self.kerneldir)
        command = self.build_command('mrproper', self.quiet)
        if self.quiet is '':
            print command

        return os.system(command)
    
    def make_clean(self): #kerneldir, KV, master_config, arch, quiet):
        """
        Kernel command interface for clean
        
        @return: bool
        """
        print green(' * ') + turquoise('kernel.clean ') + self.KV
        self.chgdir(self.kerneldir)
        command = self.build_command('clean', self.quiet)
        if self.quiet is '':
            print command

        return os.system(command)
    
    # TODO: should we add a sort of yes '' | make oldconfig?
    def make_oldconfig(self): #kerneldir, KV, master_config, arch, quiet):
        """
        Kernel command interface for oldconfig
        
        @return: bool
        """
        print green(' * ') + turquoise('kernel.oldconfig ') + self.KV
        self.chgdir(self.kerneldir)
        command = self.build_command('oldconfig', '')
        if self.quiet is '':
            print command

        return os.system(command)
    
    def make_menuconfig(self):
        """
        Kernel command interface for menuconfig
        
        @return: bool
        """
        print green(' * ') + turquoise('kernel.menuconfig ') + self.KV
        self.chgdir(self.kerneldir)
        command = self.build_command('menuconfig', '')

        return os.system(command)
    
    def make_prepare(self):
        """
        Kernel command interface for prepare
        
        @return: bool
        """
        print green(' * ') + turquoise('kernel.prepare ') + self.KV
        self.chgdir(self.kerneldir)
        command = self.build_command('prepare', self.quiet)
        if self.quiet is '':
            print command

        return os.system(command)
    
    def make_bzImage(self):
        """
        Kernel command interface for bzImage
        
        @return: bool
        """
        print green(' * ') + turquoise('kernel.bzImage ') + self.KV
        self.chgdir(self.kerneldir)
        command = self.build_command('bzImage', self.quiet)
        if self.quiet is '':
            print command

        return os.system(command)
    
    def make_modules(self):
        """
        Kernel command interface for modules
        
        @return: bool
        """
        print green(' * ') + turquoise('kernel.modules ') + self.KV
        self.chgdir(self.kerneldir)
        command = self.build_command('modules', self.quiet)
        if self.quiet is '':
            print command

        return os.system(command)
    
    def make_modules_install(self):
        """
        Kernel command interface for modules_install 
        
        @return: bool
        """
        print green(' * ') + turquoise('kernel.modules_install ') + self.fakeroot + '/lib/modules/' + self.KV
        self.chgdir(self.kerneldir)
        
        if self.fakeroot is not '':
            # export INSTALL_MOD_PATH 
            os.environ['INSTALL_MOD_PATH'] = self.fakeroot
    
        command = self.build_command('modules_install', self.quiet)
        if self.quiet is '':
            print command

        return os.system(command)
