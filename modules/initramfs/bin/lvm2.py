import os
import sys
from stdout import green, turquoise, white, red, yellow
from utils.process import *
from utils.misc import *
from utils.listdynamiclibs import *
from utils.isstatic import *

class lvm2:

    def __init__(self, cli, temp, verbose):

        self.cli = cli
        self.temp = temp
        self.verbose = verbose

    def build(self):
        """
        Append lvm2 static binary from host to the initramfs

        @return: bool
        """
        logging.debug('>>> entering initramfs.append.host.lvm2')
        lvm2_static_bin = '/sbin/lvm.static'
        lvm2_bin        = '/sbin/lvm'

        process('mkdir -p ' + self.temp['work']+'/initramfs-bin-lvm2-temp/etc/lvm', self.verbose)
        process('mkdir -p ' + self.temp['work']+'/initramfs-bin-lvm2-temp/bin', self.verbose)

        # copy binary from host
        logging.debug('initramfs.append.bin_lvm2')
        process('cp %s      %s/initramfs-bin-lvm2-temp/bin/lvm'         % (lvm2_static_bin, self.temp['work']), self.verbose)
        process('cp %s      %s/initramfs-bin-lvm2-temp/bin/lvm_static'  % (lvm2_static_bin, self.temp['work']), self.verbose)
        process('chmod +x   %s/initramfs-bin-lvm2-temp/bin/lvm'         % self.temp['work'], self.verbose)
        process('chmod +x   %s/initramfs-bin-lvm2-temp/bin/lvm_static'  % self.temp['work'], self.verbose)

        if not isstatic(lvm2_static_bin, self.verbose) and self.cli['dynlibs'] is True:
            lvm2_libs = listdynamiclibs(lvm2_static_bin, self.verbose)
            process('mkdir -p %s' % self.temp['work']+'/initramfs-bin-lvm2-temp/lib', self.verbose)
            print(yellow(' * ') + '... ' + yellow('warning')+': '+lvm2_bin+' is dynamically linked, copying detected libraries')
            for i in lvm2_libs:
                print (green(' * ') + '... ' + i)
                process('cp %s %s' % (i, self.temp['work']+'/initramfs-bin-lvm2-temp/lib'), self.verbose)
        else:
            logging.debug(lvm2_static_bin+' is statically linked nothing to do')

        # FIXME print something to the user about it so he knows and can tweak it before
        if os.path.isfile(lvm2_static_bin) or os.path.isfile(lvm2_bin):
            process('cp /etc/lvm/lvm.conf %s/initramfs-bin-lvm2-temp/etc/lvm/' % self.temp['work'], self.verbose)

        os.chdir(self.temp['work']+'/initramfs-bin-lvm2-temp')
        return os.system('find . -print | cpio --quiet -o -H newc --append -F %s/initramfs-cpio' % self.temp['cache'])
