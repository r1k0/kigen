import os
import sys
from stdout import green, turquoise, white, red, yellow
import utils

class splash:

    def __init__(self,  \
                master_config,  \
                theme,          \
                sres,           \
                sinitrd,        \
                temp,           \
                verbose):
        """
        init class variable
        """

        self.master_config  = master_config
        self.theme          = theme
        self.sres           = sres
        self.sinitrd        = sinitrd
        self.temp           = temp
        self.verbose        = verbose
        self.splashtmp      = self.temp['work']+'/initramfs-splash-temp/'

    def build(self):
        """
        splash build sequence

        @return     bool
        """
        utils.sprocessor('mkdir -p ' + self.splashtmp + '/dev', self.verbose)
        utils.sprocessor('mkdir -p ' + self.splashtmp + '/etc', self.verbose)
        utils.sprocessor('mkdir -p ' + self.splashtmp + '/root', self.verbose)
        utils.sprocessor('mkdir -p ' + self.splashtmp + '/sbin', self.verbose)

# create /lib or /lib64 depends on system host or why not just both?
# create /lib/splash/proc /lib/splash/sys
# create /dev/console /dev/tty0 /dev/null nods
# create /dev/fb /dev/misc /dev/vc dir
# copy initrd.splash to $/etc
# create /etc/splash
# copy theme dir from /etc/splash/theme to $/etc/splash according to sres too

# compile fbcondecor_helper and copy it to /sbin 
#  libpng jpeg zlib freetype
#  mimic splashutils ebuild
# make a symlink from /sbin/fbcondecor_helper to /sbin/splash_helper


    def fail(self, step):
        """
        @arg step   string

        @return     exit
        """
        print red('error')+': initramfs.splash.'+step+'() failed'
        sys.exit(2)

