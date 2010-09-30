import sys
import os
from getopt import getopt, GetoptError
from stdout import white, green, turquoise, yellow, red
from credits import author, productname, version, description, contributor
 
from default import *
from utils.misc import *

from usage import *

# WARN don't import logging here

def cli_parser(master_conf, modules_conf, kernel_conf, initramfs_conf):

    target = 'none'

    cli = { 'config':       '/etc/kigen.conf',  \
            'nocache':      '',                 \
            'oldconfig':    True,               \
            'kerneldir':    kerneldir,          \
            'arch':         identify_arch()}

    # parse kigen config file
    kigen_conf = cli['config']
    if os.path.isfile(kigen_conf):
        master_conf_temp = parse_config_file(kigen_conf)
        master_conf.update(master_conf_temp)
    else:
        print 'error: missing ' + red(kigen_conf)
        sys.exit(2)

    # set default kernel sources
    if 'kernel-sources' in master_conf:
        # if set grab value from config file
        cli['kerneldir'] = master_conf['kernel-sources']

    cli['KV'] = get_kernel_version(cli['kerneldir'])

    if not os.path.isdir(cli['kerneldir']):
        print red('error') + ': ' + cli['kerneldir'] + ' does not exist.'
        sys.exit(2)
    if cli['KV'] is 'none':
        print red('error') + ': ' + cli['kerneldir']+'/Makefile not found'
        sys.exit(2)

    verbose = { 'std':      '',     \
                'set':      False,  \
                'logfile':  '/var/log/kigen.log'}

    if len(sys.argv) < 2:
        print_usage()
        sys.exit(2)

    cliopts = sys.argv

    # prevent multiple targets from running
    if 'k' in cliopts and 'i' in cliopts:
        print red('error: ') + 'kigen cannot run multiple targets at once'
        print_usage()
        sys.exit(2)
    elif 'initramfs' in cliopts and 'kernel' in cliopts:
        print red('error: ') + 'kigen cannot run multiple targets at once'
        print_usage()
        sys.exit(2)
    elif 'k' in cliopts and 'initramfs' in cliopts:
        print red('error: ') + 'kigen cannot run multiple targets at once'
        print_usage()
        sys.exit(2)
    elif 'i' in cliopts and 'kernel' in cliopts:
        print red('error: ') + 'kigen cannot run multiple targets at once'
        print_usage()
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
        try:
            opts, args = getopt(cliopts[1:], "idhn", [  \
                                    "config=",                  \
                                    "help",                     \
                                    "info",                     \
                                    "version",                  \
#                                    "nocolor",                  \
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
                                    "fixdotconfig",             \
                                    "getdotconfig=",            \
                                    "debug"])
        except GetoptError, err:
            print str(err) # "option -a not recognized"
            print_usage()
            sys.exit(2)

        # this has to be taken care before quiet is initialized
        # hence the extra loop, catch --logfile before all
        cli['logfile'] = '/var/log/kigen.log'
        for o, a in opts:
            if o in ("--logfile"):
                cli['logfile'] = a
        # default
        cli['config']       = '/etc/kigen.conf'
        cli['dotconfig']    = ''
        cli['rename']       = '/boot/kernel-kigen-'+cli['arch']+'-'+cli['KV']
        cli['initramfs']    = ''
        cli['info']         = False
        cli['mrproper']     = False
        cli['menuconfig']   = False
        cli['clean']        = False
        cli['allyesconfig'] = False
        cli['allnoconfig']  = False
        cli['oldconfig']    = True
        cli['nomodinstall'] = False
        cli['fakeroot']     = '/'
        cli['nocache']      = False
        cli['noboot']       = False
#       quiet               = '2>&1 | tee -a ' + logfile # verbose
#       quiet               = '>>' + logfile + ' 2>&1' # quiet + logfile
        verbose['std']      = '>>' + cli['logfile'] + ' 2>&1'
        cli['color']        = True
        cli['nosaveconfig'] = False
        cli['fixdotconfig'] = False
        cli['getdotconfig'] = ''

        # target options
        for o, a in opts:
            if o in ("-h", "--help"):
                print_usage_kernel(cli)
                sys.exit(0)
            elif o in ("--credits"):
                print_credits()
                sys.exit(0)
            elif o in ("--version"):
                print_version()
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
                if os.path.isdir(a):
                    cli['fakeroot'] = a
                else:
                    print "%s is not a directory" % a
                    sys.exit(2)
            elif o in ("--noboot"):
                cli['noboot'] = True
#            elif o in ("-n", "--nocolor"):
#                cli['color'] = False
            elif o in ("--nosaveconfig"):
                cli['nosaveconfig'] = True
            elif o in ("--config="):
                cli['config'] = a
            elif o in ("--clean"):
                cli['clean'] = True
            elif o in ("--fixdotconfig"):
                cli['fixdotconfig'] = True
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
        try:
            opts, args = getopt(cliopts[1:], "hdin", [  \
                                    "config=",      \
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
#                                    "nocolor",      \
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
        except GetoptError, err:
            print str(err) # "option -a not recognized"
            print_usage()
            sys.exit(2)
    
        # this has to be taken care before quiet is initialized
        # hence the extra loop, catch --logfile before all
        cli['logfile'] = '/var/log/kigen.log'
        for o, a in opts:
            if o in ("--logfile"):
                cli['logfile'] = a
        # default
        cli['config']       = '/etc/kigen.conf'
        cli['dotconfig']    = ''
        cli['info']         = False
        cli['mrproper']     = False
        cli['menuconfig']   = False
        cli['defconfig']    = False
        cli['oldconfig']    = False # too much verbose
        cli['luks']         = False
        cli['lvm2']         = False
        cli['dmraid']       = False
        cli['iscsi']        = False
        cli['evms']         = False
        cli['mdadm']        = False
        cli['splash']       = ''
        cli['sres']         = '' # 1024x768
        cli['sinitrd']      = '' # a custom initrd.splash file
        cli['firmware']     = ''
        cli['disklabel']    = False
        cli['unionfs']      = False
        cli['aufs']         = False
        cli['linuxrc']      = ''
        cli['dropbear']     = False
        cli['nocache']      = False
        cli['noboot']       = False
        cli['selinux']      = False
#       quiet               = '2>&1 | tee -a ' + logfile # verbose
#       quiet               = '>>' + logfile + ' 2>&1' # quiet + logfile
        verbose['std']      = '>>' + cli['logfile'] + ' 2>&1'
        cli['color']        = True
        cli['nosaveconfig'] = False
        cli['hostbin']      = False
        cli['glibc']        = False
        cli['libncurses']   = False
        cli['zlib']         = False
        cli['rename']       = '/boot/initramfs-kigen-'+cli['arch']+'-'+cli['KV']
        cli['plugin']       = ''
        cli['rootpasswd']   = ''
        cli['extract']      = ''
        cli['to']           = '/var/tmp/kigen/extracted-initramfs'
        cli['compress']     = ''
        cli['into']         = '/var/tmp/kigen/compressed-initramfs/initramfs_data.cpio.gz'
        cli['ttyecho']      = False
        cli['keymaps']      = False
        cli['strace']       = False
        cli['screen']       = False
        cli['debugflag']    = False
    
        # target options
        for o, a in opts:
            if o in ("-h", "--help"):
                print_usage_initramfs(cli)
                sys.exit(0)
            elif o in ("--credits"):
                print_credits()
                sys.exit(0)
            elif o in ("--version"):
                print_version()
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
                    print "%s is not a directory" % a
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
#            elif o in ("-n", "--nocolor"):
#                cli['color'] = False
            elif o in ("--config="):
                cli['config'] = a
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
        except GetoptError, err:
            print str(err) # "option -a not recognized"
            print_usage()
            sys.exit(2)

        # single options
        for o, a in opts:
            if o in ("-h", "--help"):
                print_usage()
                print_examples()
                sys.exit(0)
            elif o in ("--version"):
                print_version()
                sys.exit(0)
            elif o in ("--credits"):
                print_credits()
                sys.exit(0)
            else:
                assert False, "uncaught option"

    return master_conf, target, cli, verbose
