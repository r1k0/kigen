# These default variables are vital for kigen to work
# default temp directory
temp_root = '/var/tmp/kigen'

# default kernel directory
kerneldir = '/usr/src/linux'

# default temp directory structure
temp = {'root'      : temp_root,              \
        'work'      : temp_root + '/work',    \
        'cache'     : temp_root + '/cache',   \
        'distfiles' : temp_root + '/distfiles'}

# These default variables are just for convenience
# when the option is not found in /etc/kigen config files
# it will fall back to these values
# default values
master_conf = {
        'busybox-version'       : '',             \
        'dm_ver'                : '',             \
        'dmraid_ver'            : '',             \
        'e2fsprogs-version'     : '',             \
        'luks-version'          : '',             \
        'fuse_ver'              : '',             \
        'iscsi_ver'             : '',             \
        'kernel-source'         : '/usr/src/linux',\
        'lvm2-version'          : '',             \
        'aufs_ver'              : '',             \
        'unionfs_fuse_ver'      : '',             \
        'DEFAULT_KERNEL_AS'     : 'as',           \
        'DEFAULT_KERNEL_CC'     : 'gcc',          \
        'DEFAULT_KERNEL_LD'     : 'ld',           \
        'DEFAULT_KERNEL_MAKE'   : 'make',         \
        'DEFAULT_MAKEOPTS'      : '-j2',          \
        'DEFAULT_UTILS_AS'      : 'as',           \
        'DEFAULT_UTILS_CC'      : 'gcc',          \
        'DEFAULT_UTILS_LD'      : 'ld',           \
        'DEFAULT_UTILS_MAKE'    : 'make',         \
        'UTILS_AS'              : 'as',           \
        'UTILS_CC'              : 'gcc',          \
        'UTILS_MAKE'            : 'make',         \
        'UTILS_LD'              : 'ld'}

# default kernel values
kernel_conf = {
         'dotconfig'   : '',    \
         'initramfs'   : '',    \
         'fixdotconfig': '',    \
         'clean'       : '',    \
         'mrproper'    : '',    \
         'menuconfig'  : '',    \
         'fakeroot'    : '',    \
         'nooldconfig' : '',    \
         'nomodinstall': '',    \
         'nomodules'   : '',    \
         'nosaveconfig': '',    \
         'noboot'      : '',    \
         'rename'      : ''}

# default modules values
modules_conf = {
        'MODULES_ATARAID'   : '',   \
        'MODULES_DMRAID'    : '',   \
        'MODULES_EVMS'      : '',   \
        'MODULES_FIREWIRE'  : '',   \
        'MODULES_FS'        : '',   \
        'MODULES_ISCSI'     : '',   \
        'MODULES_LVM'       : '',   \
        'MODULES_MDADM'     : '',   \
        'MODULES_NET'       : '',   \
        'MODULES_PATA'      : '',   \
        'MODULES_PCMCIA'    : '',   \
        'MODULES_SATA'      : '',   \
        'MODULES_SCSI'      : '',   \
        'MODULES_USB'       : '',   \
        'MODULES_WAITSCAN'  : '',   \
        'MODULES_CRYPT'     : '',   \
        'MODULES_MISC'      : '',   \
        'MODULES_VIDEO'     : ''}

# default initramfs values
initramfs_conf = {
        'rename'        : '',   \
        'keymaps'       : 'all',\
#        'evms'          : 'False',   \
        'bin-evms'      : 'False',   \
#        'lvm2'          : 'False',   \
        'bin-lvm2'      : 'False',   \
        'source-lvm2'   : 'False',   \
#        'selinux'       : '',   \
#        'screen'        : 'False',   \
        'bin-screen'    : 'False',   \
        'source-screen' : 'False',   \
        'rootpasswd'    : '',   \
        'defconfig'     : 'False',   \
#        'disklabel'     : '',   \
        'bin-disklabel' : 'False',   \
        'source-disklabel': 'False', \
#        'strace'        : '',   \
        'bin-strace'    : 'False',  \
        'source-strace' : 'False',  \
        'noboot'        : '',   \
        'debugflag'     : '',   \
        'sres'          : '',   \
        'menuconfig'    : '',   \
#        'dmraid'        : 'False',  \
        'bin-dmraid'    : 'False',  \
        'source-dmraid' : 'False',  \
        'nocache'       : '',   \
        'plugin'        : '',   \
        'linuxrc'       : '',   \
#        'glibc'         : 'False',  \
        'bin-glibc'     : 'False',  \
#        'zlib'          : 'False',  \
        'bin-zlib'      : 'False',  \
#        'libncurses'    : 'False',  \
        'bin-libncurses': 'False',  \
        'dotconfig'     : '',   \
        'dropbear'      : 'False',  \
        'bin-dropbear'  : 'False',  \
        'source-dropbear':'False',  \
        'hostbin'       : '',   \
        'splash'        : '',   \
        'oldconfig'     : '',   \
#        'ttyecho'       : 'False',  \
        'source-ttyecho': 'False',  \
#        'luks'          : 'False',  \
        'bin-luks'      : 'False',  \
        'source-luks'   : 'False',  \
        'bin-all'       : 'False',  \
        'source-all'    : 'False',  \
        'nomodules'     : 'False',  \
        'bin-busybox'   : 'False',  \
        'dynlibs'  : 'False'}

# default version values
version_conf = {
        'strace-version'    : '4.5.20',         \
        'luks-version'      : '1.1.3',          \
        'screen-version'    : '4.0.3',          \
        'dropbear-version'  : '0.53',           \
        'busybox-version'   : '1.18.4',         \
        'dmraid-version'    : '1.0.0.rc16-3',   \
        'lvm2-version'      : '2.02.85',        \
        'e2fsprogs-version' : '1.41.14'}

# default url values
url_conf = {
        'device_mapper' : 'http://ftp.snt.utwente.nl/pub/os/linux/gentoo/distfiles',        \
        'fuse'          : 'http://sourceforge.net/projects/fuse/files/fuse-2.X',            \
        'iscsi'         : 'http://www.open-iscsi.org/bits',                                 \
        'unionfs_fuse'  : 'http://podgorny.cz/unionfs-fuse/releases',                       \
        'busybox'       : 'http://www.busybox.net/downloads',                               \
        'dmraid'        : 'http://people.redhat.com/~heinzm/sw/dmraid/src',                 \
        'dropbear'      : 'http://matt.ucc.asn.au/dropbear/releases',                       \
        'e2fsprogs'     : 'http://downloads.sourceforge.net/project/e2fsprogs/e2fsprogs',   \
        'luks'          : 'http://gentoo.osuosl.org/distfiles',                             \
        'lvm2'          : 'ftp://sourceware.org/pub/lvm2',                                  \
        'strace'        : 'http://downloads.sourceforge.net/project/strace/strace',         \
        'screen'        : 'http://ftp.gnu.org/gnu/screen'}
