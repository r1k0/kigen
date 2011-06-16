import os
import sys
from stdout import green, turquoise, white, red, yellow
from utils.process import *
from utils.misc import *

class evms:

    def __init__(self, temp, verbose):

        self.temp = temp
        self.verbose = verbose

    def build(self):
        """
        Append evms libraries to the initramfs
    
        @return: bool
        """
        logging.debug('>>> entering initramfs.append.bin.evms')
        if os.path.isfile('/sbin/evms'):
            print(green(' * ')+'...'+' feeding' + ' from '+white('host'))

            process('mkdir -p ' + self.temp['work']+'/initramfs-bin-evms-temp/lib/evms', self.verbose)
            process('mkdir -p ' + self.temp['work']+'/initramfs-bin-evms-temp/etc', self.verbose)
            process('mkdir -p ' + self.temp['work']+'/initramfs-bin-evms-temp/bin', self.verbose)
            process('mkdir -p ' + self.temp['work']+'/initramfs-bin-evms-temp/sbin', self.verbose)

# FIXME compare this list to the one from 'ldd /sbin/evms'
            process_star('cp -a /lib/ld-*           %s/initramfs-bin-evms-temp/lib' % self.temp['work'], self.verbose)
            process_star('cp -a /lib/libgcc_s*      %s/initramfs-bin-evms-temp/lib' % self.temp['work'], self.verbose)
            process_star('cp -a /lib/libc.*         %s/initramfs-bin-evms-temp/lib' % self.temp['work'], self.verbose)
            process_star('cp -a /lib/libc-*         %s/initramfs-bin-evms-temp/lib' % self.temp['work'], self.verbose)
            process_star('cp -a /lib/libdl.*        %s/initramfs-bin-evms-temp/lib' % self.temp['work'], self.verbose)
            process_star('cp -a /lib/libdl-*        %s/initramfs-bin-evms-temp/lib' % self.temp['work'], self.verbose)
            process_star('cp -a /lib/libpthread*    %s/initramfs-bin-evms-temp/lib' % self.temp['work'], self.verbose)
            process_star('cp -a /lib/libuuid*so*    %s/initramfs-bin-evms-temp/lib' % self.temp['work'], self.verbose)
            process_star('cp -a /lib/libevms*so*    %s/initramfs-bin-evms-temp/lib' % self.temp['work'], self.verbose)
            process('cp -a /lib/evms                %s/initramfs-bin-evms-temp/lib' % self.temp['work'], self.verbose)
            process_star('cp -a /lib/evms/*         %s/initramfs-bin-evms-temp/lib/evms' % self.temp['work'], self.verbose)
            process('cp -a /etc/evms.conf           %s/initramfs-bin-evms-temp/etc' % self.temp['work'], self.verbose)

# FIXME isstatic('/sbin/evms_activate')?
            process('cp /sbin/evms_activate         %s/initramfs-bin-evms-temp/sbin' % self.temp['work'], self.verbose)
            process_star('rm %s/initramfs-bin-evms-temp/lib/evms/*/swap*.so' % self.temp['work'], self.verbose)
        else:
            self.fail('sys-fs/evms must be merged')

        os.chdir(self.temp['work']+'/initramfs-bin-evms-temp')
        return os.system('find . -print | cpio --quiet -o -H newc --append -F %s/initramfs-cpio' % self.temp['cache'])
