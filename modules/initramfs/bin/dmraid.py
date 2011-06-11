import os
import sys
from stdout import green, turquoise, white, red, yellow
from utils.process import *
from utils.misc import *

class dmraid:

    def __init__(self, temp, verbose):
        self.temp = temp
        self.verbose = verbose

    def build(self):
        """
        Append dmraid to initramfs from the host
    
        @return: bool
        """
        logging.debug('>>> entering initramfs.append.bin.dmraid')

        dmraid_bin = '/usr/sbin/dmraid'

        process('mkdir -p ' + self.temp['work']+'/initramfs-bin-dmraid-temp/bin', self.verbose)

        # use from host
        logging.debug('initramfs.append.bin_dmraid from %s' % white('host'))
        process('cp %s %s/initramfs-bin-dmraid-temp/bin' % (dmraid_bin, self.temp['work']), self.verbose)
        process('chmod +x %s/initramfs-bin-dmraid-temp/bin/dmraid' % self.temp['work'], self.verbose)

#        if not isstatic(dmraid_bin, self.verbose):
#            dmraid_libs = listdynamiclibs(dmraid_bin, self.verbose)
#
#            process('mkdir -p %s' % self.temp['work']+'/initramfs-bin-dmraid-temp/lib', self.verbose)
#            print yellow(' * ') + '... ' + yellow('warning')+': '+dmraid_bin+' is dynamically linked, copying detected libraries'
#            for i in dmraid_libs:
#                print green(' * ') + '... ' + i
#                process('cp %s %s' % (i, self.temp['work']+'/initramfs-bin-dmraid-temp/lib'), self.verbose)
#        else:
#            logging.debug(dmraid_bin+' is statically linked nothing to do')

        # FIXME ln -sf raid456.ko raid45.ko ?
        # FIXME is it ok to have no raid456.ko? if so shouldn't we check .config for inkernel feat?
        #   or should we raise an error and make the user enabling the module manually? warning?

        os.chdir(self.temp['work']+'/initramfs-bin-dmraid-temp')
        return os.system('find . -print | cpio --quiet -o -H newc --append -F %s/initramfs-cpio' % self.temp['cache'])
