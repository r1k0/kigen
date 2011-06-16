import os
import sys
from stdout import green, turquoise, white, red, yellow
from utils.process import *
from utils.misc import *
from utils.listdynamiclibs import *
from utils.isstatic import *

class dropbear:

    def __init__(self, cli, libdir, temp, verbose):

        self.cli = cli
        self.libdir = libdir
        self.temp   = temp
        self.verbose= verbose

    def build(self):
        """
        Append dropbear support to the initramfs
    
        @return: bool
        """
        logging.debug('>>> entering initramfs.append.bin.dropbear')
        for i in ['bin', 'sbin', 'dev', 'usr/bin', 'usr/sbin', 'lib', 'etc', 'var/log', 'var/run', 'root']:
            process('mkdir -p %s/%s' % (self.temp['work']+'/initramfs-bin-dropbear-temp/', i), self.verbose)

        dropbear_sbin       = '/usr/sbin/dropbear'

        dbscp_bin           = '/usr/bin/dbscp'  # FIXME assumes host version is patched w/ scp->dbscp because of openssh.
                                                # FIXME compilation of dropbear sources are not patched hence
                                                # FIXME if --dropbear --hostbin
                                                # FIXME then /usr/bin/scp
                                                # FIXME else /usr/bin/dbscp
        dbclient_bin        = '/usr/bin/dbclient'
        dropbearkey_bin     = '/usr/bin/dropbearkey'
        dropbearconvert_bin = '/usr/bin/dropbearconvert'

        process('cp %s %s/initramfs-bin-dropbear-temp/bin'                  % (dbscp_bin, self.temp['work']), self.verbose)
        process('cp %s %s/initramfs-bin-dropbear-temp/bin'                  % (dbclient_bin, self.temp['work']), self.verbose)
        process('cp %s %s/initramfs-bin-dropbear-temp/bin'                  % (dropbearkey_bin, self.temp['work']), self.verbose)
        process('cp %s %s/initramfs-bin-dropbear-temp/bin'                  % (dropbearconvert_bin, self.temp['work']), self.verbose)
        process('cp %s %s/initramfs-bin-dropbear-temp/sbin'                 % (dropbear_sbin, self.temp['work']), self.verbose)
        process('chmod +x %s/initramfs-bin-dropbear-temp/bin/dbscp'         % self.temp['work'], self.verbose)
        process('chmod +x %s/initramfs-bin-dropbear-temp/bin/dbclient'      % self.temp['work'], self.verbose)
        process('chmod +x %s/initramfs-bin-dropbear-temp/bin/dropbearkey'   % self.temp['work'], self.verbose)
        process('chmod +x %s/initramfs-bin-dropbear-temp/bin/dropbearconvert' % self.temp['work'], self.verbose)
        process('chmod +x %s/initramfs-bin-dropbear-temp/sbin/dropbear'     % self.temp['work'], self.verbose)

# FIXME check if dropbearkey dropbearconvert dbclient dbscp static too? NO ldd says they all use the same as /usr/sbin/dropbear
        if not isstatic(dropbear_sbin, self.verbose) and self.cli['dynlibs'] is True:
            dropbear_libs = listdynamiclibs(dropbear_sbin, self.verbose)
            process('mkdir -p %s' % self.temp['work']+'/initramfs-bin-dropbear-temp/lib', self.verbose)
            print(yellow(' * ') + '... ' + yellow('warning')+': '+dropbear_sbin+' is dynamically linked, copying detected libraries')
            for i in dropbear_libs:
                print(green(' * ') + '... ' + i)
                process('cp %s %s' % (i, self.temp['work']+'/initramfs-bin-dropbear-temp/lib'), self.verbose)
        else:
            logging.debug('dropbear is static nothing to do')

        process('cp /etc/localtime %s'          % self.temp['work']+'/initramfs-bin-dropbear-temp/etc', self.verbose)
        process('cp /etc/nsswitch.conf %s'      % self.temp['work']+'/initramfs-bin-dropbear-temp/etc', self.verbose)
        process('cp /etc/hosts %s'              % self.temp['work']+'/initramfs-bin-dropbear-temp/etc', self.verbose)
        process('touch %s'                      % self.temp['work']+'/initramfs-bin-dropbear-temp/var/log/lastlog', self.verbose)
        process('touch %s'                      % self.temp['work']+'/initramfs-bin-dropbear-temp/var/log/wtmp', self.verbose)
        process('touch %s'                      % self.temp['work']+'/initramfs-bin-dropbear-temp/var/run/utmp', self.verbose)

        # ship the boot* scripts too
        process('cp %s/scripts/boot-luks-lvm.sh %s' % (self.libdir, self.temp['work']+'/initramfs-bin-dropbear-temp/root'), self.verbose)
        process('chmod +x %s' % self.temp['work']+'/initramfs-bin-dropbear-temp/root/boot-luks-lvm.sh', self.verbose)
        process('cp %s/scripts/boot-luks.sh %s' % (self.libdir, self.temp['work']+'/initramfs-bin-dropbear-temp/root'), self.verbose)
        process('chmod +x %s' % self.temp['work']+'/initramfs-bin-dropbear-temp/root/boot-luks.sh', self.verbose)

        os.chdir(self.temp['work']+'/initramfs-bin-dropbear-temp/dev')
        process('mknod urandom c 1 9', self.verbose)
        process('mknod ptmx c 5 2', self.verbose)
        process('mknod tty c 5 0', self.verbose)
        process('chmod 0666 urandom', self.verbose)
        process('chmod 0666 ptmx', self.verbose)
        process('chmod 0666 tty', self.verbose)

        os.chdir(self.temp['work']+'/initramfs-bin-dropbear-temp')
        return os.system('find . -print | cpio --quiet -o -H newc --append -F %s/initramfs-cpio' % self.temp['cache'])
