import os
import sys
from stdout import green, turquoise, white, red, yellow
from utils.process import *
from utils.misc import *
from utils.listdynamiclibs import *
from utils.isstatic import *

class disklabel:

    def __init__(self, cli, temp, verbose):

        self.cli = cli
        self.temp = temp
        self.verbose = verbose

    def build(self):
        """
        Append blkid binary from the host
        
        @return: bool
        """
        logging.debug('>>> entering initramfs.append.bin_disklabel')
        blkid_sbin = '/sbin/blkid'

        process('mkdir -p %s' % self.temp['work']+'/initramfs-bin-disklabel-temp/bin', self.verbose)

        # use from host
        logging.debug('initramfs.append.bin_disklabelfrom %s' % white('host'))
        process('cp %s %s/initramfs-bin-disklabel-temp/bin' % (blkid_sbin, self.temp['work']), self.verbose)
        process('chmod +x %s/initramfs-bin-disklabel-temp/bin/blkid' % self.temp['work'], self.verbose)

        if not isstatic(blkid_sbin, self.verbose) and self.cli['dynlibs'] is True:
            blkid_libs = listdynamiclibs(blkid_sbin, self.verbose)
            process('mkdir -p %s' % self.temp['work']+'/initramfs-bin-blkid-temp/lib', self.verbose)
            print(yellow(' * ') + '... ' + yellow('warning')+': '+blkid_sbin+' is dynamically linked, copying detected libraries')
            for i in blkid_libs:
                print(green(' * ') + '... ' + i)
                process('cp %s %s' % (i, self.temp['work']+'/initramfs-bin-blkid-temp/lib'), self.verbose)
        else:
            logging.debug(blkid_sbin+' is statically linked nothing to do')

        os.chdir(self.temp['work']+'/initramfs-bin-disklabel-temp')
        return os.system('find . -print | cpio --quiet -o -H newc --append -F %s/initramfs-cpio' % self.temp['cache'])
