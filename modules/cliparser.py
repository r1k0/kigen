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

    target = 'none'

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

    # cli['KV'] = utils.misc.get_kernel_version(cli['kerneldir'])
    cli['KV'] = utils.misc.get_kernel_utsrelease(cli['kerneldir'])

    # exit if kernel dir doesn't exist
    if not os.path.isdir(cli['kerneldir']):
        print(stdout.red('error') + ': ' + cli['kerneldir'] + ' does not exist.')
        sys.exit(2)
    # exit if kernel version is not found
    if cli['KV'] is 'none':
        print(stdout.red('error') + ': ' + cli['kerneldir']+'/Makefile not found')
        sys.exit(2)

    # prevent multiple targets from running
    if 'k' in cliopts and 'i' in cliopts:
        print(stdout.red('error: ') + 'kigen cannot run multiple targets at once')
        usage.print_usage()
        sys.exit(2)
    elif 'initramfs' in cliopts and 'kernel' in cliopts:
        print(stdout.red('error: ') + 'kigen cannot run multiple targets at once')
        usage.print_usage()
        sys.exit(2)
    elif 'k' in cliopts and 'initramfs' in cliopts:
        print(stdout.red('error: ') + 'kigen cannot run multiple targets at once')
        usage.print_usage()
        sys.exit(2)
    elif 'i' in cliopts and 'kernel' in cliopts:
        print(stdout.red('error: ') + 'kigen cannot run multiple targets at once')
        usage.print_usage()
        sys.exit(2)

    # === parsing for the kernel target ===
    if 'kernel' in sys.argv or 'k' in sys.argv:
        # we found the kernel target
        # parse accordingly
        if 'kernel' in sys.argv:
            target = 'kernel'
            cliopts.remove('kernel')
        if 'k' in sys.argv:
            target = 'kernel'
            cliopts.remove('k')

        # parse 
        kernel_conf = etcparser.etc_parser_kernel()

        try:
            # parse command line
            opts, args = getopt(cliopts[1:], "idhn", [  \
                                    "help",                     \
                                    "info",                     \
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
            print_usage()
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
#        cli['fixdotconfig'] = False
#        if kernel_conf['fixdotconfig'] == 'True':
#            cli['fixdotconfig'] = True
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
#                cli['fixdotconfig'] = True
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
            target = 'initramfs'
            cliopts.remove('i')

        # parse /etc/kigen/initramfs/modules.conf and 
        # /etc/kigen/initramfs/initramfs.conf
        initramfs_conf, modules_conf, version_conf = etcparser.etc_parser_initramfs()

        try:
            # parse command line
            opts, args = getopt(cliopts[1:], "hdin", [  \
                                    "dotconfig=",   \
                                    "mrproper",     \
                                    "menuconfig",   \
                                    "allyesconfig", \
                                    "nooldconfig",  \
                                    "defconfig",    \
                                    "oldconfig",    \
                                    "luks",         \
                                    "lvm2",         \
                                    "dmraid",       \
                                    "iscsi",        \
                                    "logfile=",     \
                                    "evms",         \
                                    "mdadm",        \
                                    "splash=",      \
                                    "sres=",        \
                                    "sinitrd=",     \
                                    "firmware=",    \
                                    "disklabel",    \
                                    "unionfs-fuse", \
                                    "aufs",         \
                                    "dropbear",     \
                                    "linuxrc=",     \
                                    "nocache",      \
                                    "noboot",       \
                                    "selinux",      \
                                    "help",         \
                                    "info",         \
                                    "version",      \
                                    "credits",      \
                                    "nosaveconfig", \
                                    "hostbin",      \
                                    "glibc",        \
                                    "libncurses",   \
                                    "zlib",         \
                                    "rename=",      \
                                    "plugin=",      \
                                    "rootpasswd=",  \
                                    "extract=",     \
                                    "to=",          \
                                    "compress=",    \
                                    "into=",        \
                                    "keymaps",      \
                                    "ttyecho",      \
                                    "strace",       \
                                    "screen",       \
                                    "debugflag",    \
                                    "debug"])
        except GetoptError as err:
            print(str(err)) # "option -a not recognized"
            print_usage()
            sys.exit(2)
    
        # this has to be taken care before quiet is initialized
        # hence the extra loop, catch --logfile before all
        cli['logfile'] = '/var/log/kigen.log'
        if master_conf['logfile'] != '':
            cli['logfile'] = master_conf['logfile']
        for o, a in opts:
            if o in ("--logfile"):
                cli['logfile'] = a

        cli['oldconfig']    = False # too much verbose
        if initramfs_conf['oldconfig'] == 'True':
            cli['oldconfig'] = True

        # default
        cli['dotconfig']    = ''
        if initramfs_conf['dotconfig'] != '':
            cli['dotconfig'] = initramfs_conf['dotconfig']
            cli['oldconfig'] = True # make sure .config is ok

#        cli['info']         = False
#        cli['mrproper']     = False
#        if initramfs_conf['mrproper'] == 'True':
#            cli['mrproper'] = True

        cli['menuconfig']   = False
        if initramfs_conf['menuconfig'] == 'True':
            cli['menuconfig'] = True

        cli['defconfig']    = False
        if initramfs_conf['defconfig'] == 'True':
            cli['defconfig'] = True

        cli['luks']         = False
        if initramfs_conf['luks'] == 'True':
            cli['luks'] = True

        cli['lvm2']         = False
        if initramfs_conf['lvm2'] == 'True':
            cli['lvm2'] = True

        cli['dmraid']       = False
        if initramfs_conf['dmraid'] == 'True':
            cli['dmraid'] = True

#        cli['iscsi']        = False
#        if initramfs_conf['iscsi'] == 'True':
#            cli['iscsi'] = True

        cli['evms']         = False
        if initramfs_conf['evms'] == 'True':
            cli['evms'] = True

#        cli['mdadm']        = False
#        if initramfs_conf['mdadm'] == 'True':
#            cli['mdadm'] = True

        cli['splash']       = ''
        if initramfs_conf['splash'] != '':
            cli['splash'] = initramfs_conf['splash']

        cli['sres']         = '' # 1024x768
        if initramfs_conf['sres'] != '':
            cli['sres'] = initramfs_conf['sres']

        cli['sinitrd']      = '' # a custom initrd.splash file

#        cli['firmware']     = ''

        cli['disklabel']    = False
        if initramfs_conf['disklabel'] == 'True':
            cli['disklabel'] = True

#        cli['unionfs']      = False
#        if initramfs_conf['unionfs'] == 'True':
#           cli['unionfs'] = True

#        cli['aufs']         = False

        cli['linuxrc']      = ''
        if initramfs_conf['linuxrc'] != '':
            cli['linuxrc'] = initramfs_conf['linuxrc']

        cli['dropbear']     = False
        if initramfs_conf['dropbear'] == 'True':
            cli['dropbear'] = True

        cli['nocache']      = False
        if initramfs_conf['nocache'] == 'True':
            cli['nocache'] = True

        cli['noboot']       = False
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

        cli['glibc']        = False
        if initramfs_conf['glibc'] == 'True':
            cli['glibc'] = True

        cli['libncurses']   = False
        if initramfs_conf['libncurses'] == 'True':
            cli['libncurses'] = True

        cli['zlib']         = False
        if initramfs_conf['zlib'] == 'True':
            cli['zlib'] = True

        print(cli['arch'])
        print(cli['KV'])
        cli['rename']       = '/boot/initramfs-kigen-'+cli['arch']+'-'+cli['KV']
        if initramfs_conf['rename'] != '':
            cli['rename'] = initramfs_conf['rename']

        cli['plugin']       = ''
        if initramfs_conf['plugin'] != '':
            cli['plugin'] = initramfs_conf['plugin']

        cli['rootpasswd'] = ''
        if initramfs_conf['rootpasswd'] != '':
            cli['rootpasswd'] = initramfs_conf['rootpasswd']

        cli['ttyecho'] = False
        if initramfs_conf['ttyecho'] == 'True':
            cli['ttyecho'] = True

        cli['keymaps']      = False
        if initramfs_conf['keymaps'] == 'True':
            cli['keymaps'] = True

        cli['strace']       = False
        if initramfs_conf['strace'] == 'True':
            cli['strace'] = True

        cli['screen']       = False
        if initramfs_conf['screen'] == 'True':
            cli['screen'] = True

        cli['debugflag']    = False
        if initramfs_conf['debugflag'] == 'True':
            cli['debugflag'] = True

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
            elif o in ("--luks"):
                cli['luks'] = True
            elif o in ("--lvm2"):
                cli['lvm2'] = True
            elif o in ("--dmraid"):
                cli['dmraid'] = True
            elif o in ("--dotconfig"):
                cli['dotconfig'] = a
                cli['oldconfig'] = True # make sure .config is ok
            elif o in ("--iscsi"):
                cli['iscsi'] = True
            elif o in ("--evms"):
                cli['evms'] = True
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
            elif o in ("--dropbear"):
                cli['dropbear'] = True
                cli['glibc'] = True         # dropbear needs glibc
                cli['libncurses'] = True    # dropbear needs libncurses
                cli['zlib'] = True          # dropbear needs zlib
            elif o in ("--hostbin"):
                cli['hostbin'] = True
            elif o in ("--glibc"):
                cli['glibc'] = True
            elif o in ("--libncurses"):
                cli['libncurses'] = True
            elif o in ("--zlib"):
                cli['zlib'] = True
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
            elif o in ("--keymaps"):
                cli['keymaps'] = True
            elif o in ("--strace"):
                cli['strace'] = True
            elif o in ("--screen"):
                cli['screen'] = True
                cli['glibc'] = True         # screen needs glibc
                cli['libncurses'] = True    # screen needs libncurses
            elif o in ("--debugflag"):
                cli['debugflag'] = True

            else:
                assert False, "uncaught option"

    else:
        # no target found in cliopts
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

    return master_conf, kernel_conf, modules_conf, initramfs_conf, version_conf, target, cli, verbose
