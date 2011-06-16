import os
import sys
from stdout import green, turquoise, white, red, yellow
from utils.process import *
from utils.misc import *
from utils.listdynamiclibs import *
from utils.isstatic import *

class strace:

    def __init__(self, cli, temp, verbose):

        self.cli = cli
        self.temp = temp
        self.verbose = verbose

    def build(self):
        """
        Append strace host binary to the initramfs
        for debugging purposes
        
        @return: bool
        """
        logging.debug('>>> entering initramfs.append.bin.strace')
        strace_bin = '/usr/bin/strace'

        process('mkdir -p %s' % self.temp['work']+'/initramfs-bin-strace-temp/bin', self.verbose)

        # use from host
        logging.debug('initramfs.append.bin_strace from ' + white('host'))
        process('cp %s %s/initramfs-bin-strace-temp/bin' % (strace_bin, self.temp['work']), self.verbose)
        process('chmod +x %s/initramfs-bin-strace-temp/bin/strace' % self.temp['work'], self.verbose)

        if not isstatic(strace_bin, self.verbose) and self.cli['dynlibs'] is True:
            strace_libs = listdynamiclibs(strace_bin, self.verbose)
            process('mkdir -p %s' % self.temp['work']+'/initramfs-bin-strace-temp/lib', self.verbose)
            print(yellow(' * ') + '... ' + yellow('warning')+': '+strace_bin+' is dynamically linked, copying detected libraries')
            for i in strace_libs:
                print(green(' * ') + '... ' + i)
                process('cp %s %s' % (i, self.temp['work']+'/initramfs-bin-strace-temp/lib'), self.verbose)
        else:
            logging.debug(strace_bin+' is statically linked nothing to do')

        os.chdir(self.temp['work']+'/initramfs-bin-strace-temp')
        return os.system('find . -print | cpio --quiet -o -H newc --append -F %s/initramfs-cpio' % self.temp['cache'])
