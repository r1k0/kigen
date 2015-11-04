import os
import sys
from stdout import green, turquoise, white, red, yellow
from utils.process import *
from utils.misc import *
from utils.listdynamiclibs import *
from utils.isstatic import *

class plymouth:

    def __init__(self, cli, temp, verbose):

        self.cli = cli
        self.temp = temp
        self.verbose = verbose

    def build(self):
        """
        Append plymouth binary from host to the initramfs
        
        @return: bool
        """
        logging.debug('>>> entering initramfs.append.bin_plymouth')
        plymouth_bin = '/usr/bin/plymouth'

        process('mkdir -p %s' % self.temp['work']+'/initramfs-bin-plymouth-temp/bin', self.verbose)

         # use from host
        logging.debug('initramfs.append.bin_plymouth from %s' % white('host'))
        process('cp %s %s/initramfs-bin-plymouth-temp/bin' % (plymouth_bin, self.temp['work']), self.verbose)
        process('chmod +rx %s/initramfs-bin-plymouth-temp/bin/plymouth' % self.temp['work'], self.verbose)

        if not isstatic(plymouth_bin, self.verbose) and self.cli['dynlibs'] is True:
            plymouth_libs = listdynamiclibs(plymouth_bin, self.verbose)
            process('mkdir -p %s' % self.temp['work']+'/initramfs-bin-plymouth-temp/lib', self.verbose)
            print(yellow(' * ') + '... ' + yellow('warning')+': '+plymouth_bin+' is dynamically linked, copying detected libraries')
            for i in plymouth_libs:
                print(green(' * ') + '... ' + i)
                process('cp %s %s' % (i, self.temp['work']+'/initramfs-bin-plymouth-temp/lib'), self.verbose)

        os.chdir(self.temp['work']+'/initramfs-bin-plymouth-temp')
        return os.system('find . -print | cpio --quiet -o -H newc --append -F %s/initramfs-cpio' % self.temp['cache'])
