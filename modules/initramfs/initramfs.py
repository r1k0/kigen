import os
import sys
import logging
import commands
from stdout import *
from utils.shell import *
from utils.misc import *
from append import append

class initramfs:

    def __init__(self,              \
                kernel_dir_opt,     \
                arch,               \
                KV,                 \
                libdir,             \
                master_conf,        \
                modules_conf,       \
                initramfs_conf,     \
                version_conf,       \
                cli,                \
                temp,               \
                bootupdateset,      \
                bootupdateinitrd,   \
                verbose):
        """
        init class variables
        """
        self.kernel_dir_opt     = kernel_dir_opt
        self.arch               = arch
        self.KV                 = KV
        self.libdir             = libdir
        self.master_conf        = master_conf
        self.modules_conf       = modules_conf
        self.initramfs_conf     = initramfs_conf
        self.version_conf       = version_conf
        self.linuxrc            = cli['linuxrc'] # list
        self.defconfig          = cli['defconfig']
        self.oldconfig          = cli['oldconfig']
        self.menuconfig         = cli['menuconfig']
#        self.mrproper           = cli['mrproper']
        self.nocache            = cli['nocache']
#        self.firmware           = cli['firmware']
        self.verbosestd         = verbose['std']
        self.verboseset         = verbose['set']
        self.verbose            = verbose
        self.temproot           = temp['root']
        self.tempcache          = temp['cache']
        self.temp               = temp
        self.dotconfig          = cli['dotconfig']
        self.nocache            = cli['nocache']
#        self.firmware           = cli['firmware']
        self.cli                = cli
        self.bootupdateset      = bootupdateset
        self.bootupdateinitrd   = bootupdateinitrd
        self.splash             = cli['splash']
        self.sres               = cli['sres']
        self.sinitrd            = cli['sinitrd']
#        self.selinux            = cli['selinux']
        self.hostbin            = cli['hostbin']
        self.pluginroot         = cli['plugin'] # string
        self.rootpasswd         = cli['rootpasswd']
        self.dbdebugflag        = cli['debugflag']

    def build(self):
        """
        Initramfs build sequence
    
        @return: bool
        """
        zero = int('0')
        import shutil
        cpv = ''
        if self.verboseset is True: cpv = '-v'
    
        # for the sake of knowing where we are
        os.chdir(self.temproot)

        # create object
        aobj = append(self.temp,                \
                        self.KV,                \
                        self.linuxrc,           \
                        self.kernel_dir_opt,    \
                        self.arch,              \
                        self.master_conf,       \
                        self.modules_conf,      \
                        self.initramfs_conf,    \
                        self.version_conf,      \
                        self.libdir,            \
                        self.defconfig,         \
                        self.oldconfig,         \
                        self.menuconfig,        \
#                        self.mrproper,          \
                        self.verbose,           \
                        self.dotconfig,         \
                        self.master_conf['busybox-progs'],  \
                        self.bootupdateset,     \
                        self.bootupdateinitrd,  \
                        self.splash,            \
                        self.sres,              \
                        self.sinitrd,           \
#                        self.firmware,          \
#                        self.selinux,           \
                        self.dbdebugflag,       \
                        self.nocache,           \
                        self.hostbin,           \
                        self.rootpasswd)

        # 1) create initial cpio and append object
        ret, output = process_pipe('echo | cpio --quiet -o -H newc -F %s/initramfs-cpio' % self.tempcache, self.verbose)
        if ret is not zero: self.fail('cpio')
        # 2) append base
        aobj.base()
        # 4) append modules
        # note that /etc/boot.conf initrd modules if set
        # overlap the ones from /etc/kigen.conf
        if aobj.modules() is not zero: self.fail('modules')
        # 3) append busybox
        os.chdir(self.temp['work'])
        if aobj.busybox() is not zero: self.fail('busybox')
        # 5) append lvm2
        if self.cli['lvm2'] is True:
            os.chdir(self.temp['work'])
            if aobj.lvm2() is not zero: self.fail('lvm2')
#        # 6) append dmraid
#        if self.cli['dmraid'] is True:
#            os.chdir(self.temp['work'])
#            if aobj.dmraid() is not zero: self.fail('dmraid')
#        # 7) append iscsi
#        if self.cli['iscsi'] is True:
#            os.chdir(self.temp['work'])
#            if aobj.iscsi() is not zero: self.fail('iscsi')
#        # 8) append evms
#        if self.cli['evms'] is True:
#            os.chdir(self.temp['work'])
#            if aobj.evms() is not zero: self.fail('evms')
#        # 9) append mdadm
#        if self.cli['mdadm'] is True:
#            os.chdir(self.temp['work'])
#            if aobj.mdadm() is not zero: self.fail('mdadm')
        # 10) append luks
        if self.cli['luks'] is True:
            os.chdir(self.temp['work'])
            if aobj.luks() is not zero: self.fail('luks')
        # 11) append multipath
        # TODO
        # 12) append blkid
        if self.cli['disklabel'] is True:
            os.chdir(self.temp['work'])
            if aobj.e2fsprogs() is not zero: self.fail('e2fsprogs')
        # 13) append dropbear
        if self.cli['dropbear'] is True:
            os.chdir(self.temp['work'])
            if aobj.dropbear() is not zero: self.fail('dropbear')
        # append strace
        if self.cli['strace'] is True:
            os.chdir(self.temp['work'])
            if aobj.strace() is not zero: self.fail('strace')
        # append screen
        if self.cli['screen'] is True:
            os.chdir(self.temp['work'])
            if aobj.screen() is not zero: self.fail('screen')
#        # 14) append unionfs_fuse
#        if self.cli['unionfs'] is True:
#            os.chdir(self.temp['work'])
#            if aobj.unionfs_fuse() is not zero: self.fail('unionfs-fuse')
#        # 15) append aufs
#        if self.cli['aufs'] is True:
#            os.chdir(self.temp['work'])
#            if aobj.aufs() is not zero: self.fail('aufs')
        # append ttyecho
        if self.cli['ttyecho'] is True:
            os.chdir(self.temp['work'])
            if aobj.ttyecho() is not zero: self.fail('ttyecho')
        # 16) append splash
        if (self.cli['splash'] is not '') or (self.initramfs_conf['splash'] != ''):
            os.chdir(self.temp['work'])
            if aobj.splash() is not zero: self.fail('splash')
        # append rootpasswd
        if self.cli['rootpasswd'] is not '':
            os.chdir(self.temp['work'])
            if aobj.set_rootpasswd() is not zero: self.fail('rootpasswd')
        # append keymaps
        if self.cli['keymaps'] is True:
            os.chdir(self.temp['work'])
            if aobj.keymaps() is not zero: self.fail('keympas')
#        # 17) append firmware
#        if os.path.isdir(self.firmware):
#            os.chdir(self.temp['work'])
#            if aobj.firmware() is not zero: self.fail('firmware')
        # TODO # 18) append overlay
        # 19) append glibc
        if self.cli['glibc'] is True:
            os.chdir(self.temp['work'])
            if aobj.glibc() is not zero: self.fail('glibc')
        # 19bis) append libncurses
        if self.cli['libncurses'] is True:
            os.chdir(self.temp['work'])
            if aobj.libncurses() is not zero: self.fail('libncurses')
        # 19terce) append zlib
        if self.cli['zlib'] is True:
            os.chdir(self.temp['work'])
            if aobj.zlib() is not zero: self.fail('zlib')
        # last) append user plugin
        if self.pluginroot is not '':
            pluginlist = self.pluginroot.split(',')
            for j in pluginlist:
                if j is not '': # this check else it copies from / :(
                    os.chdir(self.temp['work'])
                    if aobj.plugin(j) is not zero: self.fail('plugin')

        # compress initramfs-cpio
        print green(' * ') + turquoise('initramfs.compress')
        if process('gzip -f -9 %s/initramfs-cpio' % self.temp['cache'], self.verbose) is not zero: self.fail('compress')
    
    def fail(self, step):
        """
        @arg step   string

        @return     exit
        """
        print red('error')+': initramfs.append.'+step+'() failed'
        sys.exit(2)
 
