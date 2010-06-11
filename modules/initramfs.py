import os
import sys
from stdout import white, green, turquoise
from append import append
import error
import warning
import utils
import logging
import commands

class initramfs:

    def __init__(self,              \
                kernel_dir_opt,     \
                arch,               \
                KV,                 \
                libdir,             \
                master_config,      \
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
        self.master_config      = master_config # TODO replace 
        self.linuxrc            = cli['linuxrc']
        self.oldconfig          = cli['bboldconfig']
        self.menuconfig         = cli['bbmenuconfig']
        self.allyesconfig       = cli['allyesconfig']
        self.mrproper           = cli['mrproper']
        self.bbconf             = cli['bbconf']
        self.nocache            = cli['nocache']
        self.firmware           = cli['firmware']
        self.verbosestd         = verbose['std']
        self.verboseset         = verbose['set']
        self.verbose            = verbose # TODO replace 
        self.temproot           = temp['root']
        self.tempcache          = temp['cache']
        self.temp               = temp # TODO replace 
        self.bbconf             = cli['bbconf']
        self.nocache            = cli['nocache']
        self.firmware           = cli['firmware']
        self.cli                = cli # TODO replace
        self.bootupdateset      = bootupdateset
        self.bootupdateinitrd   = bootupdateinitrd
        self.stheme             = cli['stheme']
        self.sres               = cli['sres']
        self.selinux            = cli['selinux']
        self.nohostbin          = cli['nohostbin']

    def build(self):
        """
        Initramfs build sequence
    
        @return: bool
        """
        ret = zero = int('0')
        import shutil
        cpv = ''
        if self.verboseset is True: cpv = '-v'
    
        # for the sake of knowing where we are
        os.chdir(self.temproot)

        # 1) create initial cpio and append object
        ret, output = utils.spprocessor('echo | cpio --quiet -o -H newc -F %s/initramfs-cpio' % self.tempcache, self.verbose)
        if ret is not zero:
            raise error.fail('initial cpio creation failed')
        aobject = append(self.temp,         \
                        self.KV,            \
                        self.linuxrc,       \
                        self.kernel_dir_opt,\
                        self.arch,          \
                        self.master_config, \
                        self.libdir,        \
                        self.oldconfig,     \
                        self.menuconfig,    \
                        self.allyesconfig,  \
                        self.mrproper,      \
                        self.verbose,       \
                        self.bbconf,        \
                        self.master_config['busybox-progs'],  \
                        self.bootupdateset,   \
                        self.bootupdateinitrd,\
                        self.stheme,        \
                        self.sres,          \
                        self.firmware,      \
                        self.selinux,       \
                        self.nocache,       \
                        self.nohostbin)
        # 2) append base
        aobject.base()
        if ret is not zero:
            raise error.fail('initramfs.append.baselayout()')
        # 3) append busybox
        os.chdir(self.temp['work'])
        ret = aobject.busybox()
        if ret is not zero:
            raise error.fail('initramfs.append.busybox()')
        # 4) append modules
        # note that /etc/boot.conf initrd modules overlap the ones from /etc/funkernel.conf
        ret = aobject.modules()
        if ret is not zero:
            raise error.fail('initramfs.append_modules()')

        # 4) append lvm2
        if self.cli['lvm2'] is True:
            os.chdir(self.temp['work'])
            ret = aobject.lvm2()
            if ret is not zero:
                raise error.fail('initramfs.append_lvm2()')
        # 5) append dmraid
        if self.cli['dmraid'] is True:
            os.chdir(self.temp['work'])
            ret = aobject.dmraid()
            if ret is not zero:
                raise error.fail('initramfs.append_dmraid()')
        # 6) append iscsi
        if self.cli['iscsi'] is True:
            os.chdir(self.temp['work'])
            ret = aobject.iscsi()
            if ret is not zero:
                raise error.fail('initramfs.append_iscsi()')
        # 7) append evms
        if self.cli['evms'] is True:
            os.chdir(self.temp['work'])
            ret = aobject.evms()
            if ret is not zero: 
                raise error.fail('initramfs.append_evms()')
        # 8) append mdadm
        if self.cli['mdadm'] is True:
            os.chdir(self.temp['work'])
            ret = aobjectmdadm()
            if ret is not zero: 
                raise error.fail('initramfs.append_mdadm()')
        # 9) append luks
        if self.cli['luks'] is True:
            os.chdir(self.temp['work'])
            ret = aobject.luks()
            if ret is not zero: 
                raise error.fail('initramfs.append.luks()')
#        # 10) append multipath
#        # TODO
        # 12) append blkid
        if self.cli['disklabel'] is True:
            os.chdir(self.temp['work'])
            ret = aobject.e2fsprogs()
            if ret is not zero: 
                raise error.fail('initramfs.append.e2fsprogs()')
        # 13) append ssh
        if self.cli['ssh'] is True:
            os.chdir(self.temp['work'])
            ret = aobject.ssh()
            if ret is not zero:
                raise error.fail('initramfs.append_ssh()')
        # 13) append unionfs_fuse
        if self.cli['unionfs'] is True:
            os.chdir(self.temp['work'])
            ret = aobject.unionfs_fuse()
            if ret is not zero: 
                raise error.fail('initramfs.append_unionfs-fuse()')
        # 14) append aufs
        if self.cli['aufs'] is True:
            os.chdir(self.temp['work'])
            ret = aobject.aufs()
            if ret is not zero:
                raise error.fail('initramfs.append_aufs()')
        # 15) append splash
        if self.cli['splash'] is True:
            os.chdir(self.temp['work'])
            ret = aobject.splash()
            if ret is not zero:
                raise error.fail('initramfs.append.splash()')
#        # 16) append firmware
#        if os.path.isdir(self.firmware):
#            os.chdir(self.temp['work'])
#            ret = aobject.firmware()
#            if ret is not zero: 
#                raise error.fail('initramfs.append_firmware()')
    
        # 17) append overlay
        # TODO
    
        # compress initramfs-cpio
        print green(' * ') + turquoise('initramfs.compress')
        utils.sprocessor('gzip -f -9 %s/initramfs-cpio' % self.temp['cache'], self.verbose)
        if ret is not zero: 
            raise error.fail('utils.copy.initramfs() compression pre copy')
    
        return ret
 
