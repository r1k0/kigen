import sys
import os
from getopt import getopt, GetoptError
import stdout
import credits
import default
import utils.misc
import usage
import etcparser

# WARN don't import logging here as it's not already declared in kigen

def cli_parser():

    target = ''

    cli = { 'nocache':      '',                 \
            'oldconfig':    True,               \
            # typically kernel sources are found here
            'kerneldir':    '/usr/src/linux',   \
            'arch':         utils.misc.identify_arch()}

    verbose = { 'std':      '',     \
                'set':      False,  \
                'logfile':  '/var/log/kigen.log'}

    master_conf     = {}
    kernel_conf     = {}
    modules_conf    = {}
    initramfs_conf  = {}
    version_conf    = {}
    url_conf        = {}

    # copy command line arguments
    cliopts = sys.argv

    # parse /etc/kigen/master.conf
    master_conf = etcparser.etc_parser_master()

    # if not enough parameters exit with usage
    if len(sys.argv) < 2:
        usage.print_usage()
        sys.exit(2)

    # set default kernel sources
    if 'kernel-sources' in master_conf:
        # if set grab value from config file
        cli['kerneldir'] = master_conf['kernel-sources']
    # else: exit

    cli['KV'], cli['KNAME'] = utils.misc.get_kernel_version(cli['kerneldir'])

    # exit if kernel dir doesn't exist
    if not os.path.isdir(cli['kerneldir']):
        print(stdout.red('error') + ': ' + cli['kerneldir'] + ' does not exist.')
        sys.exit(2)
    # exit if kernel version is not found
    if cli['KV'] is 'none':
        print(stdout.red('error') + ': ' + cli['kerneldir']+'/Makefile not found')
        sys.exit(2)

    # prevent multiple targets from running
    if ('k' in cliopts and 'i' in cliopts)               or \
        ('initramfs' in cliopts and 'kernel' in cliopts) or \
        ('k' in cliopts and 'initramfs' in cliopts)      or \
        ('i' in cliopts and 'kernel' in cliopts)         or \
        ('t' in cliopts and 'kernel' in cliopts)         or \
        ('t' in cliopts and 'initramfs' in cliopts)      or \
        ('tool' in cliopts and 'kernel' in cliopts)      or \
        ('tool' in cliopts and 'initramfs' in cliopts)   or \
        ('tool' in cliopts and 'i' in cliopts)           or \
        ('tool' in cliopts and 'k' in cliopts)           or \
        ('t' in cliopts and 'i' in cliopts)              or \
        ('t' in cliopts and 'k' in cliopts):
        print(stdout.red('error') + ': kigen cannot run multiple targets at once.')
        sys.exit(2)

    # === parsing for the kernel target ===
    if 'kernel' in sys.argv or 'k' in sys.argv:
        # we found the kernel target
        # parse accordingly
        if 'kernel' in sys.argv:
            target = 'kernel'
            cliopts.remove('kernel')
        if 'k' in sys.argv:
            target = 'k'
            cliopts.remove('k')

        # parse 
        kernel_conf = etcparser.etc_parser_kernel()

        try:
            # parse command line
            opts, args = getopt(cliopts[1:], "dhn", [  \
                                    "help",                     \
#                                    "info",                     \
                                    "version",                  \
                                    "credits",                  \
                                    "conf=",                    \
                                    "dotconfig=",               \
                                    "bbconf=",                  \
                                    "rename=",                  \
                                    "initramfs=",               \
                                    "mrproper",                 \
                                    "clean",                    \
                                    "menuconfig",               \
                                    "allyesconfig",             \
                                    "nomodules",                \
                                    "nomodinstall",             \
                                    "fakeroot=",                \
                                    "allnoconfig",              \
                                    "nooldconfig",              \
                                    "oldconfig",                \
                                    "logfile=",                 \
                                    "noboot",                   \
                                    "nosaveconfig",             \
                                    "hostbin",                  \
                                    "fixdotconfig=",             \
                                    "getdotconfig=",            \
                                    "debug"])
        except GetoptError as err:
            print(str(err)) # "option -a not recognized"
            usage.print_usage()
            sys.exit(2)

        # this has to be taken care before quiet is initialized
        # hence the extra loop, catch --logfile before all
        cli['logfile'] = '/var/log/kigen.log'
        if master_conf['logfile'] != '':
            cli['logfile'] = master_conf['logfile']
        for o, a in opts:
            if o in ("--logfile"):
                cli['logfile'] = a

        # default
        cli['dotconfig']    = master_conf['kernel-sources']+'/.config'
        if kernel_conf['dotconfig'] != '':
            cli['dotconfig'] = kernel_conf['dotconfig']

        cli['rename']       = '/boot/kernel-kigen-'+cli['arch']+'-'+cli['KV']
        if kernel_conf['rename'] != '':
            cli['rename'] = kernel_conf['rename']

        cli['initramfs']    = ''

        cli['info']         = False

        cli['mrproper']     = False
        if kernel_conf['mrproper'] == 'True':
            cli['mrproper'] = True

        cli['menuconfig']   = False
        if kernel_conf['menuconfig'] == 'True':
            cli['menuconfig'] = True

        cli['clean']        = False
        if kernel_conf['clean'] == 'True':
            cli['clean'] = True

        cli['allyesconfig'] = False

        cli['allnoconfig']  = False

        cli['oldconfig']    = False
        if kernel_conf['nooldconfig'] == 'False':
            cli['oldconfig'] = True

        cli['nomodinstall'] = False
        if kernel_conf['nomodinstall'] == 'True':
            cli['nomodinstall'] = True

        cli['nomodules'] = False
        if kernel_conf['nomodules'] == 'True':
            cli['nomodules'] = True
            # No module support implies not installing modules
            cli['nomodinstall'] = True 

        cli['fakeroot']     = '/'
        if kernel_conf['fakeroot'] != '':
            cli['fakeroot'] = kernel_conf['fakeroot']

        cli['nocache']      = False

        cli['noboot']       = False
        if kernel_conf['noboot'] == 'True':
            cli['noboot'] = True

#       quiet               = '2>&1 | tee -a ' + logfile # verbose
#       quiet               = '>>' + logfile + ' 2>&1' # quiet + logfile

        verbose['std']      = '>>' + cli['logfile'] + ' 2>&1'
        verbose['set']      = False

        if master_conf['debug'] == 'True':
            verbose['set'] = True
            verbose['std'] = '2>&1 | tee -a ' + cli['logfile']
            verbose['logfile'] = cli['logfile']

        cli['color']        = True

        cli['nosaveconfig'] = False

        if kernel_conf['nosaveconfig'] == 'True':
            cli['nosaveconfig'] = True

        cli['fixdotconfig'] = ''
        if kernel_conf['fixdotconfig'] != '':
            cli['fixdotconfig'] = kernel_conf['fixdotconfig']
            
        cli['getdotconfig'] = ''

        # target options
        for o, a in opts:
            if o in ("-h", "--help"):
                usage.print_usage_kernel(cli, master_conf, kernel_conf)
                sys.exit(0)
            elif o in ("--credits"):
                usage.print_credits()
                sys.exit(0)
            elif o in ("--version"):
                usage.print_version()
                sys.exit(0)
            # have to declare logfile here too
            elif o in ("--logfile="):
                cli['logfile'] = a
                verbose['logfile'] = cli['logfile']
            elif o in ("-d", "--debug"):
#               quiet = '>>' + logfile + ' 2>&1' # logfile
#               quiet = '2>&1 | tee -a ' + logfile # verbose
                verbose['std'] = '2>&1 | tee -a ' + cli['logfile']
                verbose['set'] = True
                verbose['logfile'] = cli['logfile']
            elif o in ("-k", "--dotconfig"):
                cli['dotconfig'] = a
                cli['oldconfig'] = True # make sure .config is ok
            elif o in ("--rename"):
                cli['rename'] = a
            elif o in ("--initramfs"):
                cli['initramfs'] = a
            elif o in ("--mrproper"):
                cli['mrproper'] = True
            elif o in ("--menuconfig"):
                cli['menuconfig'] = True
            elif o in ("--nooldconfig"):
                cli['oldconfig'] = False
            elif o in ("--oldconfig"):
                cli['oldconfig'] = True
            elif o in ("--nomodinstall"):
                cli['nomodinstall'] = True
            elif o in ("--nomodules"):
                cli['nomodules'] = True
            elif o in ("--fakeroot"):
#                if os.path.isdir(a):
                 cli['fakeroot'] = a
#                else:
#                    print "%s is not a directory" % a
#                    sys.exit(2)
            elif o in ("--noboot"):
                cli['noboot'] = True
            elif o in ("--nosaveconfig"):
                cli['nosaveconfig'] = True
            elif o in ("--clean"):
                cli['clean'] = True
            elif o in ("--fixdotconfig"):
                cli['fixdotconfig'] = a
            elif o in ("--getdotconfig"):
                cli['getdotconfig'] = a
            else:
                assert False, "uncaught option"

    # === parsing for the initramfs target ===
    elif 'initramfs' in sys.argv or 'i' in sys.argv:
        # we found the initramfs target
        # parse accordingly
        if 'initramfs' in sys.argv:
            target = 'initramfs'
            cliopts.remove('initramfs')
        if 'i' in sys.argv:
            target = 'i'
            cliopts.remove('i')

        # parse /etc/kigen/initramfs/modules.conf and 
        # /etc/kigen/initramfs/initramfs.conf
        initramfs_conf, modules_conf, version_conf, url_conf = etcparser.etc_parser_initramfs()

        try:
            # parse command line
            opts, args = getopt(cliopts[1:], "hdn", [  \
                                    "dotconfig=",   \
                                    "mrproper",     \
                                    "menuconfig",   \
                                    "allyesconfig", \
                                    "nooldconfig",  \
                                    "defconfig",    \
                                    "oldconfig",    \
#                                    "luks",         \
                                    "bin-luks",     \
                                    "source-luks",  \
#                                    "lvm2",         \
                                    "source-lvm2",  \
                                    "bin-lvm2",     \
#                                    "dmraid",       \
                                    "bin-dmraid",   \
                                    "source-dmraid",\
                                    "iscsi",        \
                                    "logfile=",     \
#                                    "evms",         \
                                    "bin-evms",     \
                                    "mdadm",        \
                                    "splash=",      \
                                    "sres=",        \
                                    "sinitrd=",     \
                                    "firmware=",    \
#                                    "disklabel",    \
                                    "bin-disklabel",\
                                    "source-disklabel",\
                                    "unionfs-fuse", \
                                    "aufs",         \
#                                    "dropbear",     \
                                    "bin-dropbear", \
                                    "source-dropbear",\
                                    "linuxrc=",     \
                                    "nocache",      \
                                    "nomodules",    \
                                    "noboot",       \
                                    "selinux",      \
                                    "help",         \
#                                    "info",         \
                                    "version",      \
                                    "credits",      \
                                    "nosaveconfig", \
                                    "hostbin",      \
                                    "glibc",        \
#                                    "bin-glibc",    \
                                    "libncurses",   \
                                    "bin-libncurses",\
#                                    "zlib",         \
                                    "bin-zlib",     \
                                    "rename=",      \
                                    "plugin=",      \
                                    "rootpasswd=",  \
                                    "extract=",     \
                                    "to=",          \
                                    "compress=",    \
                                    "into=",        \
                                    "keymaps=",     \
#                                    "ttyecho",      \
                                    "source-ttyecho",\
#                                    "strace",       \
                                    "bin-strace",   \
                                    "source-strace",\
#                                    "screen",       \
                                    "bin-screen",   \
                                    "source-screen", \
                                    "debugflag",    \
                                    "bin-all",      \
                                    "source-all",   \
                                    "bin-busybox",  \
                                    "dynlibs", \
                                    "debug"])
        except GetoptError as err:
            print(str(err)) # "option -a not recognized"
            usage.print_usage()
            sys.exit(2)
    
        # this has to be taken care before quiet is initialized
        # hence the extra loop, catch --logfile before all
        cli['logfile'] = '/var/log/kigen.log'
        if master_conf['logfile'] != '':
            cli['logfile'] = master_conf['logfile']
        for o, a in opts:
            if o in ("--logfile"):
                cli['logfile'] = a

        cli['oldconfig'] = False # too much verbose
        if initramfs_conf['oldconfig'] == 'True':
            cli['oldconfig'] = True

        # default
        cli['dotconfig'] = ''
        if initramfs_conf['dotconfig'] != '':
            cli['dotconfig'] = initramfs_conf['dotconfig']
            cli['oldconfig'] = True # make sure .config is ok

#        cli['info'] = False
#        cli['mrproper'] = False
#        if initramfs_conf['mrproper'] == 'True':
#            cli['mrproper'] = True

        cli['menuconfig'] = False
        if initramfs_conf['menuconfig'] == 'True':
            cli['menuconfig'] = True

        cli['defconfig'] = False
        if initramfs_conf['defconfig'] == 'True':
            cli['defconfig'] = True

        cli['bin-luks'] = False
        if initramfs_conf['bin-luks'] == 'True':
            cli['bin-luks'] = True
            cli['source-luks'] = False

        cli['source-luks'] = False
        if initramfs_conf['source-luks'] == 'True':
            cli['source-luks'] = True
            cli['bin-luks'] = False

        cli['bin-busybox'] = False
        if initramfs_conf['bin-busybox'] == 'True':
            cli['bin-busybox'] = True

        cli['source-lvm2'] = False
        if initramfs_conf['source-lvm2'] == 'True':
            cli['source-lvm2'] = True

        cli['bin-lvm2'] = False
        if initramfs_conf['bin-lvm2'] == 'True':
            cli['bin-lvm2'] = True

        cli['bin-dmraid'] = False
        if initramfs_conf['bin-dmraid'] == 'True':
            cli['bin-dmraid'] = True
        cli['source-dmraid'] = False
        if initramfs_conf['source-dmraid'] == 'True':
            cli['source-dmraid'] = True

#        cli['iscsi'] = False
#        if initramfs_conf['iscsi'] == 'True':
#            cli['iscsi'] = True

        cli['bin-evms'] = False
        if initramfs_conf['bin-evms'] == 'True':
            cli['bin-evms'] = True

#        cli['mdadm'] = False
#        if initramfs_conf['mdadm'] == 'True':
#            cli['mdadm'] = True

        cli['splash'] = ''
        if initramfs_conf['splash'] != '':
            cli['splash'] = initramfs_conf['splash']

        cli['sres'] = '' # 1024x768
        if initramfs_conf['sres'] != '':
            cli['sres'] = initramfs_conf['sres']

        cli['sinitrd'] = '' # a custom initrd.splash file

#        cli['firmware'] = ''

        cli['bin-disklabel'] = False
        if initramfs_conf['bin-disklabel'] == 'True':
            cli['bin-disklabel'] = True

        cli['source-disklabel'] = False
        if initramfs_conf['source-disklabel'] == 'True':
            cli['source-disklabel'] = True

#        cli['unionfs'] = False
#        if initramfs_conf['unionfs'] == 'True':
#           cli['unionfs'] = True

#        cli['aufs'] = False

        cli['linuxrc'] = ''
        if initramfs_conf['linuxrc'] != '':
            cli['linuxrc'] = initramfs_conf['linuxrc']

        cli['bin-dropbear'] = False
        if initramfs_conf['bin-dropbear'] == 'True':
            cli['bin-dropbear'] = True

        cli['source-dropbear'] = False
        if initramfs_conf['source-dropbear'] == 'True':
            cli['source-dropbear'] = True

        cli['nomodules'] = False
        if initramfs_conf['nomodules'] == 'True':
            cli['nomodules'] = True

        cli['nocache'] = False
        if initramfs_conf['nocache'] == 'True':
            cli['nocache'] = True

        cli['noboot'] = False
        if initramfs_conf['noboot'] == 'True':
            cli['noboot'] = True

        cli['selinux']      = False
#       quiet               = '2>&1 | tee -a ' + logfile # verbose
#       quiet               = '>>' + logfile + ' 2>&1' # quiet + logfile
        verbose['std']      = '>>' + cli['logfile'] + ' 2>&1'
        cli['color']        = True
        cli['nosaveconfig'] = False
#        if initramfs_conf['nosaveconfig'] == 'True':
#            cli['nosaveconfig'] = True
        cli['hostbin']      = False
        if initramfs_conf['hostbin'] == 'True':
            cli['hostbin'] = True

        cli['bin-glibc'] = False
        if initramfs_conf['bin-glibc'] == 'True':
            cli['bin-glibc'] = True

        cli['bin-libncurses'] = False
        if initramfs_conf['bin-libncurses'] == 'True':
            cli['bin-libncurses'] = True

        cli['bin-zlib'] = False
        if initramfs_conf['bin-zlib'] == 'True':
            cli['bin-zlib'] = True

        cli['rename'] = '/boot/initramfs-kigen-'+cli['arch']+'-'+cli['KV']
        if initramfs_conf['rename'] != '':
            cli['rename'] = initramfs_conf['rename']

        cli['plugin'] = ''
        if initramfs_conf['plugin'] != '':
            cli['plugin'] = initramfs_conf['plugin']

        cli['rootpasswd']  = ''
        if initramfs_conf['rootpasswd'] != '':
            cli['rootpasswd'] = initramfs_conf['rootpasswd']

        cli['source-ttyecho'] = False
        if initramfs_conf['source-ttyecho'] == 'True':
            cli['source-ttyecho'] = True

        cli['keymaps'] = 'all'
        if initramfs_conf['keymaps'] != '':
            cli['keymaps'] = initramfs_conf['keymaps']

        cli['bin-strace'] = False
        if initramfs_conf['bin-strace'] == 'True':
            cli['bin-strace'] = True

        cli['source-strace'] = False
        if initramfs_conf['source-strace'] == 'True':
            cli['source-strace'] =True

        cli['bin-screen'] = False
        if initramfs_conf['bin-screen'] == 'True':
            cli['bin-screen'] = True

        cli['source-screen'] = False
        if initramfs_conf['source-screen'] == 'True':
            cli['source-screen'] = True

        cli['dynlibs'] = False
        if initramfs_conf['dynlibs'] == 'True':
            cli['dynlibs'] = True

        cli['debugflag'] = False
        if initramfs_conf['debugflag'] == 'True':
            cli['debugflag']= True

        cli['bin-all'] = False
        if initramfs_conf['bin-all'] == 'True':
            cli['bin-busybox'] = True
            cli['bin-luks'] = True
            cli['bin-lvm2'] = True
            cli['bin-screen'] = True
            cli['bin-disklabel'] = True
            cli['bin-strace'] = True
            cli['bin-evms'] = True
            cli['bin-glibc'] = True
            cli['bin-libncurses'] = True
            cli['bin-zlib'] = True
            cli['bin-dmraid'] = True
            cli['bin-dropbear'] = True

        cli['source-all'] = False
        if initramfs_conf['source-all'] == 'True':
            cli['source-luks'] = True
            cli['source-lvm2'] = True
            cli['source-screen'] = True
            cli['source-disklabel'] = True
            cli['source-ttyecho'] = True
            cli['source-strace'] = True
            cli['source-dmraid'] = True
            cli['source-dropbear'] = True

        # tools
        cli['extract']      = ''
        cli['to']           = '/var/tmp/kigen/extracted-initramfs'
        cli['compress']     = ''
        cli['into']         = '/var/tmp/kigen/compressed-initramfs/initramfs_data.cpio.gz'

        verbose['set'] = False
        if master_conf['debug'] == 'True':
            verbose['set'] = True
            verbose['std'] = '2>&1 | tee -a ' + cli['logfile']
            verbose['logfile'] = cli['logfile']
    
        # target options
        for o, a in opts:
            if o in ("-h", "--help"):
                usage.print_usage_initramfs(cli, master_conf, initramfs_conf, modules_conf)
                sys.exit(0)
            elif o in ("--credits"):
                usage.print_credits()
                sys.exit(0)
            elif o in ("--version"):
                usage.print_version()
                sys.exit(0)
            # have to declare logfile here too
            elif o in ("--logfile="):
                cli['logfile'] = a
                verbose['logfile'] = cli['logfile']
            elif o in ("-d", "--debug"):
#               quiet = '>>' + logfile + ' 2>&1' # logfile
#               quiet = '2>&1 | tee -a ' + logfile # verbose
                verbose['std'] = '2>&1 | tee -a ' + cli['logfile']
                verbose['set'] = True
                verbose['logfile'] = cli['logfile']
            elif o in ("--disklabel"):
                cli['disklabel'] = True
            elif o in ("--bin-disklabel"):
                cli['bin-disklabel'] = True
                cli['source-disklabel'] = False
            elif o in ("--source-disklabel"):
                cli['bin-disklabel'] = False
                cli['source-disklabel'] = True
            elif o in ("--luks"):
                cli['luks'] = True
# FIXME trigger --keymap=all?
            elif o in ("--bin-luks"):
                cli['bin-luks'] = True
                cli['source-luks'] = False
            elif o in ("--source-luks"):
                cli['source-luks'] = True
                cli['bin-luks'] = False
            elif o in ("--lvm2"):
                cli['lvm2'] = True
            elif o in ("--source-lvm2"):
                cli['source-lvm2'] = True
                cli['bin-lvm2'] = False
            elif o in ("--bin-lvm2"):
                cli['bin-lvm2'] = True
                cli['source-lvm2'] = False
            elif o in ("--bin-dmraid"):
                cli['bin-dmraid'] = True
            elif o in ("--source-dmraid"):
                cli['source-dmraid'] = True
            elif o in ("--dotconfig"):
                cli['dotconfig'] = a
                cli['oldconfig'] = True # make sure .config is ok
            elif o in ("--iscsi"):
                cli['iscsi'] = True
            elif o in ("--bin-evms"):
                cli['bin-evms'] = True
            elif o in ("--mdadm"):
                cli['mdadm'] = True
            elif o in ("--mrproper"):
                cli['mrproper'] = True
            elif o in ("--menuconfig"):
                cli['menuconfig'] = True
            elif o in ("--nooldconfig"):
                cli['oldconfig'] = False
            elif o in ("--oldconfig"):
                cli['oldconfig'] = True
            elif o in ("--defconfig"):
                cli['defconfig'] = True
            elif o in ("--splash"):
                cli['splash'] = a
            elif o in ("--firmware"):
                if os.path.isdir(a):
                    cli['firmware'] = a
                else:
                    print(("%s is not a directory" % a))
                    sys.exit(2)
            elif o in ("--unionfs-fuse"):
                cli['unionfs'] = True
            elif o in ("--aufs"):
                cli['aufs'] = True
            elif o in ("--linuxrc"):
                cli['linuxrc'] = a
            elif o in ("--sres"):
                cli['sres'] = a
            elif o in ("--sinitrd"):
                cli['sinitrd'] = a
            elif o in ("--nocache"):
                cli['nocache'] = True
            elif o in ("--noboot"):
                cli['noboot'] = True
            elif o in ("--selinux"):
                cli['selinux'] = True
            elif o in ("--bin-dropbear"):
                cli['bin-dropbear'] = True
                cli['bin-glibc'] = True         # dropbear needs glibc
                cli['bin-libncurses'] = True    # dropbear needs libncurses
                cli['bin-zlib'] = True          # dropbear needs zlib
            elif o in ("--source-dropbear"):
                cli['source-dropbear'] = True
                cli['bin-glibc'] = True         # dropbear needs glibc
                cli['bin-libncurses'] = True    # dropbear needs libncurses
                cli['bin-zlib'] = True          # dropbear needs zlib
            elif o in ("--hostbin"):
                cli['hostbin'] = True
            elif o in ("--bin-glibc"):
                cli['bin-glibc'] = True
            elif o in ("--bin-libncurses"):
                cli['bin-libncurses'] = True
            elif o in ("--bin-zlib"):
                cli['bin-zlib'] = True
            elif o in ("--rename="):
                cli['rename'] = a
            elif o in ("--plugin"):
                cli['plugin'] = a # a is a list
            elif o in ("--rootpasswd="):
                cli['rootpasswd'] = a
            elif o in ("--extract"):
                cli['extract'] = a
            elif o in ("--to"):
                cli['to'] = a
            elif o in ("--compress"):
                cli['compress'] = a
            elif o in ("--into"):
                cli['into'] = a
            elif o in ("--ttyecho"):
                cli['ttyecho'] = True
            elif o in("--source-ttyecho"):
                cli['source-ttyecho'] = True
            elif o in ("--keymaps"):
                cli['keymaps'] = a
            elif o in ("--strace"):
                cli['strace'] = True
            elif o in ("--bin-strace"):
                cli['bin-strace'] = True
                cli['source-strace'] = False
            elif o in ("--source-strace"):
                cli['source-strace'] = True
                cli['bin-strace'] = False
            elif o in ("--screen"):
                cli['screen'] = True
                cli['bin-glibc'] = True         # screen needs glibc
                cli['bin-libncurses'] = True    # screen needs libncurses
            elif o in ("--bin-screen"):
                cli['bin-screen'] = True
                cli['bin-glibc'] = True         # screen needs glibc
                cli['bin-libncurses'] = True    # screen needs libncurses
            elif o in ("--source-screen"):
                cli['source-screen'] = True
                cli['bin-glibc'] = True         # screen needs glibc
                cli['bin-libncurses'] = True    # screen needs libncurses
            elif o in ("--debugflag"):
                cli['debugflag'] = True
            elif o in ("--nomodules"):
                cli['nomodules'] = True
            elif o in ("--bin-all"):
                cli['bin-busybox']      = True
                cli['bin-luks']         = True
                cli['bin-lvm2']         = True
                cli['bin-screen']       = True
                cli['bin-disklabel']    = True
                cli['bin-strace']       = True
                cli['bin-evms']         = True
                cli['bin-glibc']        = True
                cli['bin-libncurses']   = True
                cli['bin-zlib']         = True
                cli['bin-dmraid']       = True
                cli['bin-dropbear']     = True
            elif o in ("--source-all"):
                cli['source-luks']      = True
                cli['source-lvm2']      = True
                cli['source-disklabel'] = True
                cli['source-screen']    = True
                cli['source-ttyecho']   = True
                cli['source-strace']    = True
                cli['source-dmraid']    = True
                cli['source-dropbear']  = True
            elif o in ("--bin-busybox"):
                cli['bin-busybox'] = True
            elif o in ("--dynlibs"):
                cli['dynlibs'] = True

            else:
                assert False, "uncaught option"

    # === parsing for the tool target ===
    elif 'tool' in sys.argv or 't' in sys.argv:
        # we found the tool target
        # parse accordingly
        if 'tool' in sys.argv:
            target = 'tool'
            cliopts.remove('tool')
        if 't' in sys.argv:
            target = 't'
            cliopts.remove('t')

        # parse all /etc/kigen/ config files
        kernel_conf = etcparser.etc_parser_kernel()
        initramfs_conf, modules_conf, version_conf, url_conf = etcparser.etc_parser_initramfs()

        try:
            # parse command line
            opts, args = getopt(cliopts[1:], "hn", [  \
                                    "extract=",         \
                                    "to=",              \
                                    "compress=",        \
                                    "into=",            \
                                    "getdotconfig="])
        except GetoptError as err:
            print(str(err)) # "option -a not recognized"
            usage.print_usage()
            sys.exit(2)

        cli['getdotconfig'] = ''
        cli['extract']      = ''
        cli['to']           = '/var/tmp/kigen/extracted-initramfs'
        cli['compress']     = ''
        cli['into']         = '/var/tmp/kigen/compressed-initramfs/initramfs_data.cpio.gz'

        for o, a in opts:
            if o in ("-h", "--help"):
                usage.print_usage_tool(cli)
                sys.exit(0)
            elif o in ("--getdotconfig"):
                cli['getdotconfig'] = a
            elif o in ("--extract"):
                cli['extract'] = a
            elif o in ("--to"):
                cli['to'] = a
            elif o in ("--compress"):
                cli['compress'] = a
            elif o in ("--into"):
                cli['into'] = a

            else:
                assert False, "uncaught option"

        if not opts:
            usage.print_usage_tool(cli)
            sys.exit(0)
    # === parsing for NO target ===
    else:
        try:
            opts, args = getopt(cliopts[1:], "hn", [\
                                "help",             \
                                "version",          \
                                "credits"])
        except GetoptError as err:
            print(str(err)) # "option -a not recognized"
            usage.print_usage()
            sys.exit(2)

        # single options
        for o, a in opts:
            if o in ("-h", "--help"):
                usage.print_usage()
                usage.print_examples()
                sys.exit(0)
            elif o in ("--version"):
                usage.print_version()
                sys.exit(0)
            elif o in ("--credits"):
                usage.print_credits()
                sys.exit(0)
            else:
                assert False, "uncaught option"

    if target == '':
        print(stdout.red('error') + ': target not known.')
        sys.exit(2)

    return  master_conf,    \
            kernel_conf,    \
            modules_conf,   \
            initramfs_conf, \
            version_conf,   \
            url_conf,       \
            target,         \
            cli,            \
            verbose
