import sys
import os
from getopt import getopt, GetoptError
from stdout import white, green, turquoise, yellow, red
from credits import author, productname, version, description, contributor
 
from config import master_config, temp, kerneldir
from utils.misc import *

# WARN don't import logging here

def parse():

    target = 'none'

    cli = { 'config':       '/etc/kigen.conf',  \
            'nocache':      '',                 \
            'oldconfig':    True,               \
            'kerneldir':    kerneldir,          \
            'arch':         identify_arch()}

    # parse kigen config file
    kigen_conf = cli['config']
    if os.path.isfile(kigen_conf):
        master_config_temp = parse_config_file(kigen_conf)
        master_config.update(master_config_temp)
    else:
        print 'error: missing ' + red(kigen_conf)
        sys.exit(2)

    # set default kernel sources
    if 'kernel-sources' in master_config:
        # if set grab value from config file
        cli['kerneldir'] = master_config['kernel-sources']

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

    return master_config, target, cli, verbose

def print_version():
    print green('%s' % version)

def print_credits():
    print 'Copyright 2010 r1k0'
    print 'Portions copyright 2003-2005 Gentoo Foundation (default linuxrc)'
    print 'Distributed under the terms of the GNU General Public License v2'
    print 
    print 'Alphabetical list of authors:'
    print
    for i in author:
        print green(i)
    print 'Alphabetical list of contributors:'
    print
    for i in contributor:
        print green(i)

def print_usage():
    print
    print '  a '+white('Portage')+' kernel|initramfs generator'
    print
    print 'Usage'+':'
    print '      '+white(sys.argv[0])+' <'+green('options')+'|'+turquoise('target')+'>'+' ['+turquoise('parameters')+']'
    print
    print green('Options') + ':'
    print '  --help, -h                 This and examples'
    print '  --nocolor, -n              Do not colorize output'
    print '  --version                  Version'
    print '  --credits                  Credits and license'
    print
    print turquoise('Targets')+':'
    print '  kernel, k                  Build kernel/modules'
    print '  initramfs, i               Build initramfs'
    print
    print turquoise('Parameters')+':'
    print ' '+os.path.basename(sys.argv[0])+' kernel'+'                --help, -h'
    print ' '+os.path.basename(sys.argv[0])+' initramfs'+'             --help, -h'

def print_examples():
    print
    print white('Examples')+':'
    print ' '+os.path.basename(sys.argv[0])+' kernel'
    print ' '+os.path.basename(sys.argv[0])+' --clean --menuconfig k'
    print ' '+os.path.basename(sys.argv[0])+' k --initramfs=/myinitramfsfile'
    print ' '+os.path.basename(sys.argv[0])+' i --splash=sabayon'
    print ' '+os.path.basename(sys.argv[0])+' --disklabel --lvm2 --splash=sabayon --luks -d -n initramfs'
    print ' '+os.path.basename(sys.argv[0])+' i --luks --lvm2 --disklabel --splash=sabayon --glibc --hostbin'
    print ' '+os.path.basename(sys.argv[0])+' i --luks --lvm2 --disklabel --splash=sabayon --dropbear --glibc --zlib --libncurses --rootpasswd=mypasswd --ttyecho --nocache --oldconfig'
    print ' '+os.path.basename(sys.argv[0])+' --extract=/file i --to=/dir'
    print ' '+os.path.basename(sys.argv[0])+' initramfs --compress=/dir --into=/file'


def print_usage_kernel(cli):
    print 'Parameter:\t\t     Default value:\t\tDescription:'
    print
    print '  --config=/file             "'+cli['config']+'"\t\tCustom master config file'
    print '  --dotconfig=/file          "'+cli['kerneldir']+'/.config'+'"\tCustom kernel .config file'
    print '  --rename=/file             "'+cli['rename']+'"'
    print '\t\t\t\t\t\t\tCustom kernel file name'

    print '  --initramfs=/file          "'+cli['initramfs']+'"\t\t\t\tEmbed initramfs into the kernel'

    print yellow('   --fixdotconfig           '),
    print cli['fixdotconfig'],
    print yellow('\t\t\t Check and auto fix the kernel config file (experimental)')

    print '  --clean                   ',
    print cli['clean'],
    print '\t\t\tClean precompiled objects only'

    print '  --mrproper                ',
    print cli['mrproper'],
    print '\t\t\tClean precompiled objects and remove config file'

    print '  --oldconfig               ',
    print cli['oldconfig'],
    print '\t\t\tAsk for new kernel options if any'

    print '  --menuconfig              ',
    print cli['menuconfig'],
    print '\t\t\tInteractive kernel options menu'

    print '  --fakeroot=/dir            "'+cli['fakeroot']+'"\t\t\tAppend modules to /dir/lib/modules'

    print '  --nooldconfig             ',
    print not cli['oldconfig'],
    print '\t\t\tDo not ask for new kernel/initramfs options'

    print '  --nomodinstall            ',
    print cli['nomodinstall'],
    print '\t\t\tDo not install modules'

    print '  --nosaveconfig            ',
    print cli['nosaveconfig'],
    print '\t\t\tDo not save kernel config in /etc/kernels'

    print '  --noboot                  ',
    print cli['noboot'],
    print '\t\t\tDo not copy kernel to /boot'

    print '  --logfile=/file            "'+cli['logfile']+'"\tLog to file'
    print '  --debug, -d                False\t\t\tDebug verbose'
    print
    print '  --getdotconfig=/vmlinux    "'+cli['getdotconfig']+'"\t\t\t\tExtract .config from compiled binary kernel (if IKCONFIG has been set)'

def print_usage_initramfs(cli):
    # passing cli is supposed to grab default from parse()
    print 'Parameter:\t\t     Default value:\t     Description:'
    print
    print '  --config=/file             "'+cli['config']+'"       Custom master config file'
#    print '  --dotconfig=/file          "'+cli['dotconfig']+'"                      Custom busybox config file'
    print '  --dotconfig=/file          "'+temp['work'] + '/busybox-' + master_config['busybox-version']+'/.config"'
    print '\t\t\t\t\t\t     Custom busybox config file'
    print '  --rename=/file             "'+cli['rename']+'"'
    print '\t\t\t\t\t\t     Custom initramfs file name'

    print '  --defconfig               ',
    print cli['defconfig'], # bool
    print '\t\t     Set .config to largest generic options'

    print '  --oldconfig               ',
    print cli['oldconfig'], # bool
    print '\t\t     Ask for new busybox options if any'

    print '  --menuconfig              ',
    print cli['menuconfig'], # bool
    print '\t\t     Interactive busybox options menu'

    print '  --linuxrc=/linuxrc[,/file] "'+cli['linuxrc']+'"                      Include custom linuxrc (files copied over to etc)'
    print '  --splash=<theme>           "'+cli['splash']+'"                      Include splash support (splashutils must be merged)'
    print '   --sres=YxZ[,YxZ]          "'+cli['sres']+'"                       Splash resolution, all if not set'
#   print '   --sinitrd=/file           ""                       Splash custom initrd.splash (host if found)'

    print '  --disklabel               ',
    print cli['disklabel'], # bool
    print '\t\t     Include support for UUID/LABEL'

    print '  --luks                    ',
    print cli['luks'], # bool 
    print '\t\t     Include LUKS support (host binary if found)'

    print '  --lvm2                    ',
    print cli['lvm2'], # bool
    print '\t\t     Include LVM2 support (host binary if found)'

#   print '  --evms                     False                   Include evms support (evms must be merged)'
#   print '  --dmraid                   False                   Include dmraid support'
#   print '   --selinux                 False                    Include selinux support in --dmraid'
#   print '  --iscsi                    False                   Include iscsi support'
#   print '  --mdadm                    False                   Include mdadm support (mdadm must be merged)'
    print '  --dropbear                ',
    print cli['dropbear'], # bool
    print '\t\t     Include dropbear tools and daemon (host binaries if found)'

    print '   --glibc                  ',
    print cli['glibc'], # bool
    print '\t\t      Include host GNU C libraries (required for dns,dropbear)'

    print '   --libncurses             ',
    print cli['libncurses'], # bool
    print '\t\t      Include host libncurses (required for dropbear)'

    print '   --zlib                   ',
    print cli['zlib'], # bool
    print '\t\t      Include host zlib (required for dropbear)'

    print '   --rootpasswd=<passwd>     "'+cli['rootpasswd']+'"                       Create and set root password (required for dropbear)'
#   print '  --unionfs-fuse             False                   Include unionfs-fuse support'
#   print '  --aufs                     False                   Include aufs support'
#   print '  --firmware=/dir            ""                      Include custom firmware support'

    print '  --keymaps                 ',
    print cli['keymaps'], # bool
    print '\t\t     Include all keymaps'

    print '  --ttyecho                 ',
    print cli['ttyecho'], # bool
    print '\t\t     Include the handy ttyecho.c tool'

    print '  --plugin=/dir[,/dir]       "'+cli['plugin']+'"                      Include list of user generated custom roots'

    print '  --nocache                 ',
    print cli['nocache'],
    print '\t\t     Do not use cached data'

    print '  --hostbin                 ',
    print cli['hostbin'],
    print '\t\t     Use host binaries over sources when possible'

    print '  --noboot                  ',
    print cli['noboot'],
    print '\t\t     Do not copy initramfs to /boot'

    print '  --logfile=/file            "'+cli['logfile']+'"    Log to file'
    print '  --debug, -d                False                   Debug verbose'
    print
    print '  --extract=/file            "'+cli['extract']+'"                      Extract initramfs file'
    print '   --to=/dir                 "'+cli['to']+'"'
    print '\t\t\t\t\t\t      Custom extracting directory'
    print '  --compress=/dir            "'+cli['compress']+'"                      Compress directory into initramfs'
    print '   --into=/file              "'+cli['into']+'"'
    print '\t\t\t\t\t\t      Custom initramfs file'
