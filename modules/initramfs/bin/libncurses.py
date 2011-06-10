import os
import sys
from stdout import green, turquoise, white, red, yellow
from utils.process import *
from utils.misc import *

class libncurses:

    def __init__(self, temp, verbose):
        self.temp = temp
        self.verbose = verbose

    def build(self):
        """
        Append host libncurses libraries to the initramfs

        @return: bool
        """
        logging.debug('>>> entering initramfs.append.bin_libncurses')
        process('mkdir -p %s' % self.temp['work']+'/initramfs-bin-libncurses-temp/lib', self.verbose)

        print(green(' * ') + '... ' + '/lib/libncurses.so.5')
        process('cp /lib/libncurses.so.5     %s' % self.temp['work']+'/initramfs-bin-libncurses-temp/lib', self.verbose)

        os.chdir(self.temp['work']+'/initramfs-bin-libncurses-temp')
        return os.system('find . -print | cpio --quiet -o -H newc --append -F %s/initramfs-cpio' % self.temp['cache'])
