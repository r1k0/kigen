# default temp directory
temp_root = '/var/tmp/kigen'

# default kernel directory
kerneldir = '/usr/src/linux'

# default temp directory structure
temp = {'root' :        temp_root,              \
        'work' :        temp_root + '/work',    \
        'cache':        temp_root + '/cache',   \
        'distfiles':    temp_root + '/distfiles'}

# default values
master_conf = {
        'busybox-version':      '',             \
        'dm_ver':               '',             \
        'dmraid_ver':           '',             \
        'e2fsprogs-version':    '',             \
        'luks-version':         '',             \
        'fuse_ver':             '',             \
        'iscsi_ver':            '',             \
        'kernel-source':        '/usr/src/linux', \
        'lvm2-version':         '',             \
        'aufs_ver':             '',             \
        'unionfs_fuse_ver':     '',             \
        'DEFAULT_KERNEL_AS':    'as',           \
        'DEFAULT_KERNEL_CC':    'gcc',          \
        'DEFAULT_KERNEL_LD':    'ld',           \
        'DEFAULT_KERNEL_MAKE':  'make',         \
        'DEFAULT_MAKEOPTS':     '-j2',          \
        'DEFAULT_UTILS_AS':     'as',           \
        'DEFAULT_UTILS_CC':     'gcc',          \
        'DEFAULT_UTILS_LD':     'ld',           \
        'DEFAULT_UTILS_MAKE':   'make',         \
        'MODULES_ATARAID':      '',             \
        'MODULES_DMRAID':       '',             \
        'MODULES_EVMS':         '',             \
        'MODULES_FIREWIRE':     '',             \
        'MODULES_FS' :          '',             \
        'MODULES_ISCSI':        '',             \
        'MODULES_LVM':          '',             \
        'MODULES_MDADM':        '',             \
        'MODULES_NET':          '',             \
        'MODULES_PATA':         '',             \
        'MODULES_PCMCIA':       '',             \
        'MODULES_SATA':         '',             \
        'MODULES_SCSI':         '',             \
        'MODULES_USB':          '',             \
        'MODULES_WAITSCAN':     '',             \
        'UTILS_AS':             'as',           \
        'UTILS_CC':             'gcc',          \
        'UTILS_MAKE':           'make',         \
        'UTILS_LD':             'ld'}

modules_conf = {}

default_conf = {}
