import os
import sys
import logging
import subprocess
from stdout                 import *
from utils.process          import *
from utils.misc             import *
from utils.isstatic         import isstatic
from .append                import append

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
                url_conf,           \
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
        self.url_conf           = url_conf
        self.linuxrc            = cli['linuxrc'] # list
        self.defconfig          = cli['defconfig']
        self.oldconfig          = cli['oldconfig']
        self.menuconfig         = cli['menuconfig']
        self.nocache            = cli['nocache']
#        self.firmware           = cli['firmware']
        self.verbosestd         = verbose['std']
        self.verboseset         = verbose['set']
        self.verbose            = verbose
        self.temproot           = temp['root']
        self.tempcache          = temp['cache']
        self.temp               = temp
        self.dotconfig          = cli['dotconfig']
        self.cli                = cli
        self.bootupdateset      = bootupdateset
        self.bootupdateinitrd   = bootupdateinitrd
        self.splash             = cli['splash']
        self.sres               = cli['sres']
        self.sinitrd            = cli['sinitrd']
        self.selinux            = cli['selinux']
        self.hostbin            = cli['hostbin']
        self.pluginroot         = cli['plugin'] # string
        self.rootpasswd         = cli['rootpasswd']
        self.dbdebugflag        = cli['debugflag']
        self.keymaplist         = cli['keymaps']

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
                        self.url_conf,          \
                        self.libdir,            \
                        self.defconfig,         \
                        self.oldconfig,         \
                        self.menuconfig,        \
                        self.verbose,           \
                        self.dotconfig,         \
                        self.master_conf['busybox-progs'],  \
                        self.bootupdateset,     \
                        self.bootupdateinitrd,  \
                        self.splash,            \
                        self.sres,              \
                        self.sinitrd,           \
#                        self.firmware,          \
                        self.selinux,           \
                        self.dbdebugflag,       \
                        self.keymaplist,        \
                        self.nocache,           \
                        self.hostbin,           \
                        self.rootpasswd)

        # 1) create initial cpio and append object
        logging.debug('>>> creating empty initramfs')
        ret, output = process_pipe('echo -n | cpio --quiet -o -H newc -F %s/initramfs-cpio' % self.tempcache, self.verbose)
        if ret is not zero: self.fail('cpio')

        # 2) append base
        print(green(' * ') + turquoise('initramfs.append.base Gentoo linuxrc'+ white(' 3.4.30') + ' patched'))
        aobj.base()

        # 3) append modules
        # note that /etc/boot.conf initrd modules if set
        # overlap the ones from /etc/kigen.conf
        if self.cli['nomodules'] is not True:
            print(green(' * ') + turquoise('initramfs.append.modules ') + self.KV)
            if aobj.modules() is not zero: self.fail('modules')

        # 4) append busybox
        if self.cli['bin-busybox'] is True:
            print(green(' * ') + turquoise('initramfs.append.host.busybox ') + '/bin/busybox')
            os.chdir(self.temp['work'])
            if os.path.isfile('/bin/busybox'):
                from .bin.busybox import busybox
                bin_bb = busybox(self.cli, self.master_conf['busybox-progs'], self.libdir, self.temp, self.verbose)
                bin_bb.build()
                if not isstatic('/bin/busybox', self.verbose) and self.cli['dynlibs'] is False:
                    self.fail_msg('/bin/busybox is not statically linked. Merge sys-app/busybox with USE=static or use --dynlibs')
            else:
                self.fail_msg('sys-app/busybox must be merged')            
        else:
            print(green(' * ') + turquoise('initramfs.append.source.busybox ') + self.version_conf['busybox-version'])
            os.chdir(self.temp['work'])
            if aobj.source_busybox() is not zero: self.fail('busybox')

        # 5) append lvm2
        if self.cli['bin-lvm2'] is True:
            print(green(' * ') + turquoise('initramfs.append.host.lvm2 ')+'/sbin/lvm.static')
            os.chdir(self.temp['work'])
            if os.path.isfile('/sbin/lvm.static'):
                if isstatic('/sbin/lvm.static', self.verbose):
                    from .bin.lvm2 import lvm2
                    bin_lvm2 = lvm2(self.cli, self.temp, self.verbose)
                    bin_lvm2.build()
                    if not isstatic('/sbin/lvm.static', self.verbose) and self.cli['dynlibs'] is False:
                        self.fail_msg('/sbin/lvm.static is not statically linked. Merge sys-fs/lvm2 with USE=static or use --dynlibs')
                else:
                    self.fail_msg('/sbin/lvm.static is not statically linked. Merge sys-fs/lvm2 with USE=static')
            else:
                self.fail_msg('sys-fs/lvm2 must be merged')
        elif self.cli['source-lvm2'] is True:
            print(green(' * ') + turquoise('initramfs.append.source.lvm2 ') + self.version_conf['lvm2-version'])
            os.chdir(self.temp['work'])
            if aobj.source_lvm2() is not zero: self.fail('source.lvm2')

        # 6) append dmraid
        if self.cli['bin-dmraid'] is True:
            print(green(' * ') + turquoise('initramfs.append.host.dmraid ')+'/usr/sbin/dmraid')
            os.chdir(self.temp['work'])
            if os.path.isfile('/usr/sbin/dmraid'):
                from .bin.dmraid import dmraid
                bin_dmraid = dmraid(self.cli, self.temp, self.verbose)
                bin_dmraid.build()
                if not isstatic('/usr/sbin/dmraid', self.verbose) and self.cli['dynlibs'] is False:
                    self.fail_msg('/usr/sbin/dmraid is not statically linked. Merge sys-fs/dmraid with USE=static or use --dynlibs')
            else:
                self.fail_msg('sys-fs/dmraid must be merged')
        elif self.cli['source-dmraid'] is True:
            print(green(' * ') + turquoise('initramfs.append.source.dmraid ') + self.version_conf['dmraid-version'])
            os.chdir(self.temp['work'])
            if aobj.source_dmraid() is not zero: self.fail('source.dmraid')

#        # 7) append iscsi
#        if self.cli['iscsi'] is True:
#            os.chdir(self.temp['work'])
#            if aobj.iscsi() is not zero: self.fail('iscsi')

#        # 8) append evms
#        if self.cli['bin-evms'] is True:
#            print(green(' * ') + turquoise('initramfs.append.host.evms'))
#            os.chdir(self.temp['work'])
#            if os.path.isfile('/usr/sbin/evms'):
#                from .bin.evms import evms
#                bin_evms = evms(self.temp, self.verbose)
#                bin_evms.build()
##                if not isstatic('/sbin/evms', self.verbose) and self.cli['dynlibs'] is False:
##                    self.fail_msg('/sbin/evms is not statically linked. Merge sys-fs/evms with USE=static or use --dynlibs')
#            else:
#                self.fail_msg('sys-fs/evms must be merged')

#        # 9) append mdadm
#        if self.cli['mdadm'] is True:
#            os.chdir(self.temp['work'])
#            if aobj.mdadm() is not zero: self.fail('mdadm')

        # 10) append luks
        if self.cli['bin-luks'] is True:
            print(green(' * ') + turquoise('initramfs.append.host.luks ') +'/sbin/cryptsetup')
            os.chdir(self.temp['work'])
            if os.path.isfile('/sbin/cryptsetup'):
                from .bin.luks import luks
                bin_luks = luks(self.cli, self.temp, self.verbose)
                bin_luks.build()
                if not isstatic('/sbin/cryptsetup', self.verbose) and self.cli['dynlibs'] is False:
                    self.fail_msg('/sbin/cryptsetup is not statically linked. Merge sys-fs/cryptsetup with USE=static or use --dynlibs')
            else:
                self.fail_msg('sys-fs/cryptsetup must be merged')
        elif self.cli['source-luks'] is True:
            print(green(' * ') + turquoise('initramfs.append.source.luks ') + self.version_conf['luks-version'])
            os.chdir(self.temp['work'])
            if aobj.source_luks() is not zero: self.fail('source.luks')

        # 11) append multipath
        # TODO

        # 12) append blkid
        if self.cli['bin-disklabel'] is True:
            print(green(' * ') + turquoise('initramfs.append.host.disklabel ')+ '/sbin/blkid')
            os.chdir(self.temp['work'])
            if os.path.isfile('/sbin/blkid'):
                from .bin.disklabel import disklabel
                bin_disklabel = disklabel(self.cli, self.temp, self.verbose)
                bin_disklabel.build()
                if not isstatic('/sbin/blkid', self.verbose) and self.cli['dynlibs'] is False:
                    self.fail_msg('/sbin/blkid is not statically linked. Merge sys-fs/e2fsprogs with USE=static or use --dynlibs')
            else:
                self.fail_msg('sys-fs/e2fsprogs must be merged')
        elif self.cli['source-disklabel']:
            print(green(' * ') + turquoise('initramfs.append.source.disklabel ') + self.version_conf['e2fsprogs-version'])
            os.chdir(self.temp['work'])
            if aobj.source_disklabel() is not zero: self.fail('source.disklabel')
 
        # 13) append dropbear
        if self.cli['bin-dropbear'] is True:
            print(green(' * ') + turquoise('initramfs.append.host.dropbear'))
            os.chdir(self.temp['work'])
            if os.path.isfile('/usr/sbin/dropbear'):
                from .bin.dropbear import dropbear
                bin_dropbear = dropbear(self.cli, self.libdir, self.temp, self.verbose)
                bin_dropbear.build()
                if not isstatic('/usr/sbin/dropbear', self.verbose) and self.cli['dynlibs'] is False:
                    self.fail_msg('/usr/sbin/dropbear is not statically linked. Merge net-misc/dropbear with USE=static or use --dynlibs')
            else:
                self.fail_msg('net-misc/dropbear must be merged')
        elif self.cli['source-dropbear'] is True:
            print(green(' * ') + turquoise('initramfs.append.source.dropbear ') + self.version_conf['dropbear-version'])
            if aobj.source_dropbear() is not zero: self.fail('source.dropbear')

        # 14) append strace
        if self.cli['bin-strace'] is True:
            print(green(' * ') + turquoise('initramfs.append.host.strace ')+'/usr/bin/strace')
            os.chdir(self.temp['work'])
            if os.path.isfile('/usr/bin/strace'):
                from .bin.strace import strace
                bin_strace = strace(self.cli, self.temp, self.verbose)
                bin_strace.build()
                if not isstatic('/usr/bin/strace', self.verbose) and self.cli['dynlibs'] is False:
                    self.fail_msg('/usr/bin/strace is not statically linked. Merge app-misc/strace with USE=static or use --dynlibs')
            else:
                self.fail_msg('dev-util/strace must be merged')
        elif self.cli['source-strace'] is True:
            print(green(' * ') + turquoise('initramfs.append.source.strace ') + self.version_conf['strace-version'])
            os.chdir(self.temp['work'])
            if aobj.source_strace() is not zero: self.fail('source.strace')

        # 15) append screen
        if self.cli['bin-screen'] is True:
            print(green(' * ') + turquoise('initramfs.append.host.screen ')+ '/usr/bin/screen')
            os.chdir(self.temp['work'])
            if os.path.isfile('/usr/bin/screen'):
                from .bin.screen import screen
                bin_screen = screen(self.cli, self.temp, self.verbose)
                bin_screen.build()
                if not isstatic('/usr/bin/screen', self.verbose) and self.cli['dynlibs'] is False:
                    self.fail_msg('/usr/bin/screen is not statically linked. Merge app-misc/screen with USE=static or use --dynlibs')
            else:
                self.fail_msg('app-misc/screen must be merge')
        elif self.cli['source-screen'] is True:
            print(green(' * ') + turquoise('initramfs.append.source.screen ') + self.version_conf['screen-version'])
            os.chdir(self.temp['work'])
            if aobj.source_screen() is not zero: self.fail('source.screen')

#        # 16) append unionfs_fuse
#        if self.cli['unionfs'] is True:
#            os.chdir(self.temp['work'])
#            if aobj.unionfs_fuse() is not zero: self.fail('unionfs-fuse')

#        # 17) append aufs
#        if self.cli['aufs'] is True:
#            os.chdir(self.temp['work'])
#            if aobj.aufs() is not zero: self.fail('aufs')

        # 18) append ttyecho
        if self.cli['source-ttyecho'] is True:
            print(green(' * ') + turquoise('initramfs.append.source.ttyecho'))
            os.chdir(self.temp['work'])
            if aobj.source_ttyecho() is not zero: self.fail('source.ttyecho')

#        # 20) append firmware
#        if os.path.isdir(self.firmware):
#            os.chdir(self.temp['work'])
#            if aobj.firmware() is not zero: self.fail('firmware')

        # TODO # 22bis) append overlay

        # 21) append glibc
        if self.cli['bin-glibc'] is True:
            print(green(' * ') + turquoise('initramfs.append.host.glibc'))
            from .bin.glibc import glibc
            bin_glibc = glibc(self.temp, self.verbose)
            bin_glibc.build()

        # 21bis) append libncurses
        if self.cli['bin-libncurses'] is True:
            print(green(' * ') + turquoise('initramfs.append.host.libncurses'))
            from .bin.libncurses import libncurses
            bin_libncurses = libncurses(self.temp, self.verbose)
            bin_libncurses.build()

        # 21terce) append zlib
        if self.cli['bin-zlib'] is True:
            print(green(' * ') + turquoise('initramfs.append.host.zlib'))
            from .bin.zlib import zlib
            bin_zlib = zlib(self.temp, self.verbose)
            bin_zlib.build()

        # 22) append splash
        if (self.cli['splash'] is not '') or (self.initramfs_conf['splash'] != ''):
            os.chdir(self.temp['work'])
            if aobj.splash() is not zero: self.fail('splash')

        # 23) append rootpasswd
        if self.cli['rootpasswd'] is not '':
            print(green(' * ') + turquoise('initramfs.append.rootpasswd'))
            os.chdir(self.temp['work'])
            if aobj.set_rootpasswd() is not zero: self.fail('rootpasswd')

        # 24) append keymaps
        if self.cli['keymaps'] is not '':
            os.chdir(self.temp['work'])
            if aobj.keymaps() is not zero: self.fail('keymaps')

        # last) append user plugin
        if self.pluginroot is not '':
            pluginlist = self.pluginroot.split(',')
            for j in pluginlist:
                if j is not '': # this check else it copies from / :(
                    os.chdir(self.temp['work'])
                    if aobj.plugin(j) is not zero: self.fail('plugin')

        # compress initramfs-cpio
        print(green(' * ') + turquoise('initramfs.compress'))
        logging.debug('>>> compressing final initramfs-cpio')
        if process('gzip -f -9 %s/initramfs-cpio' % self.temp['cache'], self.verbose) is not zero: self.fail('compress')
    
    def fail(self, step):
        """
        @arg step   string

        @return     exit
        """
        print(red('error')+': initramfs.append.'+step+'() failed')
        sys.exit(2)
 
    def fail_msg(self, msg):
        """
        @arg step   string

        @return     exit
        """
        print(red('error')+': ' + msg)
        sys.exit(2)
