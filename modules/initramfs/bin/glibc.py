import os
import sys
from stdout import green, turquoise, white, red, yellow
from utils.process import *
from utils.misc import *

class glibc:

    def __init__(self, temp, verbose):
        self.temp = temp
        self.verbose = verbose

    def build(self):
        """
        Append GNU C libraries from host to the initramfs

        @return: bool
        """
        logging.debug('>>> entering initramfs.append.bin_glibc')

        process('mkdir -p %s' % self.temp['work']+'/initramfs-bin-glibc-temp/etc', self.verbose)
        process('mkdir -p %s' % self.temp['work']+'/initramfs-bin-glibc-temp/lib', self.verbose)

        # for shell
        print(green(' * ') + '... ' + '/lib/libm.so.6')
        process('cp /lib/libm.so.6           %s' % self.temp['work']+'/initramfs-bin-glibc-temp/lib', self.verbose)
        # mostly for authentication
        print(green(' * ') + '... ' + '/lib/libnss_files.so.2')
        process('cp /lib/libnss_files.so.2   %s' % self.temp['work']+'/initramfs-bin-glibc-temp/lib', self.verbose)
        print(green(' * ') + '... ' + '/lib/libnss_dns.so.2')
        process('cp /lib/libnss_dns.so.2     %s' % self.temp['work']+'/initramfs-bin-glibc-temp/lib', self.verbose)
        print(green(' * ') + '... ' + '/lib/libnss_nis.so.2')
        process('cp /lib/libnss_nis.so.2     %s' % self.temp['work']+'/initramfs-bin-glibc-temp/lib', self.verbose)
        print(green(' * ') + '... ' + '/lib/libnsl.so.1')
        process('cp /lib/libnsl.so.1         %s' % self.temp['work']+'/initramfs-bin-glibc-temp/lib', self.verbose)
        # resolves dns->ip
        print(green(' * ') + '... ' + '/lib/libresolv.so.2')
        process('cp /lib/libresolv.so.2      %s' % self.temp['work']+'/initramfs-bin-glibc-temp/lib', self.verbose)
        print(green(' * ') + '... ' + '/lib/ld-linux.so.2')
        process('cp /lib/ld-linux.so.2       %s' % self.temp['work']+'/initramfs-bin-glibc-temp/lib', self.verbose)
        # this is for 64b arch
        if os.path.isfile('/lib/ld-linux-x86-64.so.2'):
            print(green(' * ') + '... ' + '/lib/ld-linux-x86-64.so.2')
            process('cp /lib/ld-linux-x86-64.so.2  %s' % self.temp['work']+'/initramfs-bin-glibc-temp/lib', self.verbose)
        print(green(' * ') + '... ' + '/lib/libc.so.6')
        process('cp /lib/libc.so.6           %s' % self.temp['work']+'/initramfs-bin-glibc-temp/lib', self.verbose)
        # for dropbear
        print(green(' * ') + '... ' + '/lib/libnss_compat.so.2')
        process('cp /lib/libnss_compat.so.2  %s' % self.temp['work']+'/initramfs-bin-glibc-temp/lib', self.verbose)
        print(green(' * ') + '... ' + '/lib/libutil.so.1')
        process('cp /lib/libutil.so.1        %s' % self.temp['work']+'/initramfs-bin-glibc-temp/lib', self.verbose)
        print(green(' * ') + '... ' + '/etc/ld.so.cache')
        process('cp /etc/ld.so.cache         %s' % self.temp['work']+'/initramfs-bin-glibc-temp/etc', self.verbose)
        print(green(' * ') + '... ' + '/lib/libcrypt.so.1')
        process('cp /lib/libcrypt.so.1       %s' % self.temp['work']+'/initramfs-bin-glibc-temp/lib', self.verbose)

        os.chdir(self.temp['work']+'/initramfs-bin-glibc-temp')
        return os.system('find . -print | cpio --quiet -o -H newc --append -F %s/initramfs-cpio' % self.temp['cache'])
