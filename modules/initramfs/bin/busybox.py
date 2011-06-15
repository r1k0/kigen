import os
import sys
from stdout import green, turquoise, white, red, yellow
from utils.process import *
from utils.misc import *
from utils.listdynamiclibs import *
from utils.isstatic import *

class busybox:

    def __init__(self, busyboxprogs, libdir, temp, verbose):

        self.busyboxprogs = busyboxprogs
        self.libdir = libdir
        self.temp   = temp
        self.verbose= verbose

    def build(self):
        """
        Append busybox binary from the host
        
        @return: bool
        """
        logging.debug('>>> entering initramfs.append.bin.busybox')
        bb_bin = '/bin/busybox'

        process('mkdir -p %s' % self.temp['work']+'/initramfs-bin-busybox-temp/bin', self.verbose)

        # use from host
        logging.debug('initramfs.append.bin.busybox from %s' % white('host'))
        process('cp %s %s/initramfs-bin-busybox-temp/bin' % (bb_bin, self.temp['work']), self.verbose)
        process('chmod +x %s/initramfs-bin-busybox-temp/bin/busybox' % self.temp['work'], self.verbose)

        if not isstatic(bb_bin, self.verbose):
            bb_libs = listdynamiclibs(bb_bin, self.verbose)
            process('mkdir -p %s' % self.temp['work']+'/initramfs-bin-busybox-temp/lib', self.verbose)
            print(yellow(' * ') + '... ' + yellow('warning')+': '+bb_bin+' is dynamically linked, copying detected libraries')
            for i in bb_libs:
                print(green(' * ') + '... ' + i)
                process('cp %s %s' % (i, self.temp['work']+'/initramfs-bin-busybox-temp/lib'), self.verbose)
        else:
            logging.debug(blkid_sbin+' is statically linked nothing to do')

        os.chdir(self.temp['work']+'/initramfs-bin-busybox-temp')
        process('mkdir -p %s' % self.temp['work']+'/initramfs-bin-busybox-temp/usr/share/udhcpc/', self.verbose)
        process('cp %s/defaults/udhcpc.scripts %s/initramfs-bin-busybox-temp/usr/share/udhcpc/default.script' % (self.libdir, self.temp['work']), self.verbose)
        process('chmod +x %s/initramfs-bin-busybox-temp/usr/share/udhcpc/default.script' % self.temp['work'], self.verbose)

        # TO BE REMOVED : linuxrc's bb --install -s takes care of it
        # FIXME if busybox not exist then ln the default set -> [ ash sh mount uname echo cut cat
        for i in self.busyboxprogs.split():
            process('ln -s busybox %s/initramfs-bin-busybox-temp/bin/%s' % (self.temp['work'], i), self.verbose)

        os.chdir(self.temp['work']+'/initramfs-bin-busybox-temp')
        return os.system('find . -print | cpio --quiet -o -H newc --append -F %s/initramfs-cpio' % self.temp['cache'])
