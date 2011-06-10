import os
import sys
from stdout import green, turquoise, white, red, yellow
from utils.process import *
from utils.misc import *

class zlib:

    def __init__(self, temp, verbose):
        self.temp = temp
        self.verbose = verbose

    def build(self):
        """
        Append host zlib libraries to the initramfs

        @return: bool
        """
        logging.debug('>>> entering initramfs.append.bin_zlib')
        process('mkdir -p %s' % self.temp['work']+'/initramfs-bin-zlib-temp/lib', self.verbose)

        print(green(' * ') + '... ' + '/lib/libz.so.1')
        process('cp /lib/libz.so.1      %s' % self.temp['work']+'/initramfs-bin-zlib-temp/lib', self.verbose)

        os.chdir(self.temp['work']+'/initramfs-bin-zlib-temp')
        return os.system('find . -print | cpio --quiet -o -H newc --append -F %s/initramfs-cpio' % self.temp['cache'])
