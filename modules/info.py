import os
import sys
from stdout import green, turquoise, white, yellow, red

def show(kernel_dir_opt, master_config, arch, libdir, KV, corebootset, corebootinitrd):
    """
    Show /etc/funkernel.conf information in a formatted way
    
    @arg: string
    @arg: dict
    @arg: string
    @arg: string
    @arg: string
    @return: none
    """
    flavor = 'unknown'
    gentoorelease  = '/etc/gentoo-release'
    sabayonrelease = '/etc/sabayon-release'
#   funtoorelease  = '/etc/funtoo-release'
    debianversion  = '/etc/debian_version'
    archrelease    = '/etc/arch-release'

    # funtoo overwrites /etc/gentoo-release we catch it anyway
    if os.path.isfile(gentoorelease):
        f = open(gentoorelease)
        flavor = f.readline()
        f.close()
        if os.path.isfile(sabayonrelease):
            f = open(sabayonrelease)
            flavor = f.readline()
            f.close()
    elif os.path.isfile(debianversion):
        f = open(debianversion)
        flavor = f.readline()
        f.close()
    elif os.path.isfile(archrelease):
        f = open(archrelease)
        flavor = f.readline()
        f.close()
        flavor = 'Arch Linux' # /etc/arch-release is empty
# Funtoo needs update in baselayout to have 
# its own /etc/funtoo-release
#    elif os.path.isfile(funtoorelease):
#        f = open(funtoorelease)
#        flavor = f.readline()
#        f.close()

    flavor = flavor.strip()

    print green('OS flavor:             ') + white(flavor)
    print green('Architecture:          ') + white(arch)
    print green('Kernel source:         ') + white(master_config['kernel-sources'])+'-'+white(KV)
    print green('Funkernel root:        ') + white(libdir)
    print
    
    print green('Versions')
    print '  Busybox:             ' + white(master_config['busybox-version'])
    print '  e2fsprogs:           ' + white(master_config['e2fsprogs-version'])
    print '  LVM2:                ' + white(master_config['lvm_ver'])
    print '  device-mapper:       ' + white(master_config['dm_ver'])
    print '  iSCSI:               ' + white(master_config['iscsi_ver'])
    print '  DMRAID:              ' + white(master_config['dmraid_ver'])
    print '  Unionfs-fuse:        ' + white(master_config['unionfs_fuse_ver'])
    print '  FUSE:                ' + white(master_config['fuse_ver'])
    print '  aufs:                ' + white(master_config['aufs_ver'])
    print '  LUKS:                ' + white(master_config['luks-version'])
    print
    print green('Busybox settings')
    print '  UTILS_MAKE:          ' + white(master_config['UTILS_MAKE'])
    print '  UTILS_CC:            ' + white(master_config['UTILS_CC'])
    print '  UTILS_AS:            ' + white(master_config['UTILS_AS'])
    print '  UTILS_LD:            ' + white(master_config['UTILS_LD'])
    print
    print green('Busybox features')
    for i in master_config['busybox-progs'].split():
        print '  /bin/' + white(i) +' -> busybox'
#    print white('  %s' % master_config['busybox-progs'])
    print
    print green('Kernel settings')
    print '  DEFAULT_KERNEL_MAKE: ' + white(master_config['DEFAULT_KERNEL_MAKE'])
    print '  DEFAULT_KERNEL_CC:   ' + white(master_config['DEFAULT_KERNEL_CC'])
    print '  DEFAULT_KERNEL_AS:   ' + white(master_config['DEFAULT_KERNEL_AS'])
    print '  DEFAULT_KERNEL_LD:   ' + white(master_config['DEFAULT_KERNEL_LD'])
    print
    print green('Other source settings')
    print '  DEFAULT_MAKEOPTS:    ' + white(master_config['DEFAULT_MAKEOPTS'])
    print '  DEFAULT_UTILS_MAKE:  ' + white(master_config['DEFAULT_UTILS_MAKE'])
    print '  DEFAULT_UTILS_CC:    ' + white(master_config['DEFAULT_UTILS_CC'])
    print '  DEFAULT_UTILS_AS:    ' + white(master_config['DEFAULT_UTILS_AS'])
    print '  DEFAULT_UTILS_LD:    ' + white(master_config['DEFAULT_UTILS_LD'])
    print

    if corebootset is True:
        print green('/etc/boot.conf initrd settings')
        print '  load-modules:    ' + white(corebootinitrd['load-modules'])
        print
    else:
        print yellow('/etc/boot.conf initrd section is not set!')
        print

    print green('Modules settings')
    print '  MODULES_ATARAID:     ' + white(master_config['MODULES_ATARAID'])
    print '  MODULES_DMRAID:      ' + white(master_config['MODULES_DMRAID'])
    print '  MODULES_EVMS:        ' + white(master_config['MODULES_EVMS'])
    print '  MODULES_LVM:         ' + white(master_config['MODULES_LVM'])
    print '  MODULES_MDADM:       ' + white(master_config['MODULES_MDADM'])
    print '  MODULES_PATA:        ' + white(master_config['MODULES_PATA'])
    print '  MODULES_SATA:        ' + white(master_config['MODULES_SATA'])
    print '  MODULES_SCSI:        ' + white(master_config['MODULES_SCSI'])
    print '  MODULES_WAITSCAN:    ' + white(master_config['MODULES_WAITSCAN'])
    print '  MODULES_NET:         ' + white(master_config['MODULES_NET'])
    print '  MODULES_ISCSI:       ' + white(master_config['MODULES_ISCSI'])
    print '  MODULES_FIREWIRE:    ' + white(master_config['MODULES_FIREWIRE'])
    print '  MODULES_PCMCIA:      ' + white(master_config['MODULES_PCMCIA'])
    print '  MODULES_USB:         ' + white(master_config['MODULES_USB'])
    print '  MODULES_FS:          ' + white(master_config['MODULES_FS'])


