import os
import sys
import error
import kmake

class kernel:

    def __init__(self, kerneldir, master_config, arch, KV, cli, verbose):
        self.kerneldir      = kerneldir
        self.master_config  = master_config
        self.arch           = arch
        self.KV             = KV
        self.verbose        = verbose
        self.kconf          = cli['kconf']
        self.mrproper       = cli['mrproper']
        self.allyesconfig   = cli['allyesconfig']
        self.allnoconfig    = cli['allnoconfig']
        self.menuconfig     = cli['kmenuconfig']
        self.oldconfig      = cli['koldconfig']
        self.quiet          = verbose['std']

    def build(self):
        """
        Build kernel
        """
        ret = zero = int('0')
        if self.kconf:
            # backup the previous .config found
            if os.path.isfile(self.kerneldir + '/.config'):
                from time import time
                kmake.copy_dotconfig(self.kerneldir + '/.config', self.kerneldir + '/.config.' + str(time()), self.quiet)
            # copy the custom .config
            kmake.copy_dotconfig(self.kconf, self.kerneldir + '/.config', self.quiet)
    
        if self.mrproper is True:
            ret = kmake.mrproper(self.kerneldir, self.KV, self.master_config, self.arch, self.quiet)
            if ret is not zero:
                raise error.fail('kernel.mrproper()')
        if self.allyesconfig is True:
            ret = kmake.allyesconfig(self.kerneldir, self.KV, self.master_config, self.arch, self.quiet)
            if ret is not zero:
                raise error.fail('kernel.allyesconfig()')
        elif self.allnoconfig is True:
            ret = kmake.allnoconfig(self.kerneldir, self.KV, self.master_config, self.arch, self.quiet)
            if ret is not zero:
                raise error.fail('kernel.allnoconfig()')
        if self.menuconfig is True or self.kconf is not '':
            ret = kmake.menuconfig(self.kerneldir, self.KV, self.master_config, self.arch, self.quiet)
            if ret is not zero:
                raise error.fail('kernel.menuconfig()')
        if self.oldconfig is True:
            ret = kmake.oldconfig(self.kerneldir, self.KV, self.master_config, self.arch, self.quiet)
            if ret is not zero:
                raise error.fail('kernel.oldconfig()')
    
        # check for kernel .config
        if os.path.isfile(self.kerneldir+'/.config') is not True:
            raise error.fail(self.kerneldir+'/.config'+' does not exist.')
    
        # prepare
        ret = kmake.prepare(self.kerneldir, self.KV, self.master_config, self.arch, self.quiet)
        if ret is not zero:
            raise error.fail('kernel.prepare()')
    
        # bzImage
        ret = kmake.bzImage(self.kerneldir, self.KV, self.master_config, self.arch, self.quiet)
        if ret is not zero:
            raise error.fail('kernel.bzImage()')
    
        # modules
        # if --allnoconfig is passed, then modules are disabled
        if self.allnoconfig is not True:
            ret = kmake.modules(self.kerneldir, self.KV, self.master_config, self.arch, self.quiet)
            if ret is not zero:
                raise error.fail('kernel.modules()')
            if self.nomodinstall is False:
                # modules_install
                ret = kmake.modules_install(self.kerneldir, self.KV, self.master_config, self.arch, self.quiet, self.fakeroot)
                if ret is not zero:
                    raise error.fail('kernel.modules_install()')
    
