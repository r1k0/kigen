import sys
import os
from getopt import getopt, GetoptError
from stdout import white, green, turquoise, yellow, red
from credits import author, productname, version, description, contributor
 
from config import master_config, temp

# WARN don't import logging here

def parse():

    target = 'none'

    cli = { 'config':       '/etc/kigen.conf',  \
            'nocache':      '',                 \
            'oldconfig':    True}
    
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
                                    "nohostbin",                \
                                    "fixdotconfig",             \
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
        cli['rename']       = ''
        cli['initramfs']    = ''
        cli['info']         = False
        cli['mrproper']     = False
        cli['menuconfig']   = False
        cli['clean']        = False
        cli['allyesconfig'] = False
        cli['allnoconfig']  = False
        cli['oldconfig']    = True
        cli['nomodinstall'] = False
        cli['fakeroot']     = ''
        cli['nocache']      = False
        cli['noboot']       = False
#       quiet               = '2>&1 | tee -a ' + logfile # verbose
#       quiet               = '>>' + logfile + ' 2>&1' # quiet + logfile
        verbose['std']      = '>>' + cli['logfile'] + ' 2>&1'
        cli['color']        = True
        cli['nosaveconfig'] = False
        cli['fixdotconfig'] = False

        # target options
        for o, a in opts:
            if o in ("-h", "--help"):
                print_usage_kernel()
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
            else:
                assert False, "uncaught option"

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
                                    "nohostbin",    \
                                    "glibc",        \
                                    "libncurses",   \
                                    "zlib",         \
                                    "rename=",      \
                                    "plugin=",      \
                                    "rootpasswd=",  \
                                    "extract=",     \
                                    "to=",          \
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
        cli['oldconfig']    = False # because it produces too much output
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
        cli['nohostbin']    = False
        cli['glibc']        = False
        cli['libncurses']   = False
        cli['zlib']         = False
        cli['rename']       = ''
        cli['plugin']       = ''
        cli['rootpasswd']   = ''
        cli['extract']      = ''
        cli['to']           = '/var/tmp/kigen/extracted-initramfs'
        cli['compress']     = ''
        cli['into']         = '/var/tmp/kigen/compressed-initramfs/initramfs_data.cpio.gz'
    
        # target options
        for o, a in opts:
            if o in ("-h", "--help"):
                print_usage_initramfs()
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
            elif o in ("--nohostbin"):
                cli['nohostbin'] = True
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

    return target, cli, verbose

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
    print '  -h, --help                 This and examples'
    print '  -n, --nocolor              Do not colorize output'
    print '  --version                  Version'
    print '  --credits                  Credits and license'
    print
    print turquoise('Targets')+':'
    print '  k, kernel                  Build kernel/modules'
    print '  i, initramfs               Build initramfs'
    print
    print turquoise('Parameters')+':'
    print ' '+sys.argv[0]+' kernel'+'    --help, -h'
    print ' '+sys.argv[0]+' initramfs'+' --help, -h'

def print_examples():
    print
    print white('Examples')+':'
    print ' '+os.path.basename(sys.argv[0])+' kernel'
    print ' '+os.path.basename(sys.argv[0])+' --clean --menuconfig k'
    print ' '+os.path.basename(sys.argv[0])+' k --initramfs=/myinitramfsfile'
    print ' '+os.path.basename(sys.argv[0])+' i --splash=sabayon'
    print ' '+os.path.basename(sys.argv[0])+' --disklabel --lvm2 --splash=sabayon --luks -d -n initramfs'
    print ' '+os.path.basename(sys.argv[0])+' i --luks --lvm2 --disklabel --splash=sabayon --glibc --nohostbin'
    print ' '+os.path.basename(sys.argv[0])+' i --luks --lvm2 --disklabel --splash=sabayon --dropbear --glibc --zlib --libncurses --rootpasswd=mypasswd --nohostbin --nocache'
    print ' '+os.path.basename(sys.argv[0])+' --extract=/aninitramfs i --to=/here'
    print ' '+os.path.basename(sys.argv[0])+' initramfs --compress=/initramfsdir --into=/myinitramfs'


def print_usage_kernel():
    print '  --config=/file             Custom master config file'
    print '  --dotconfig=/file          Custom kernel config file'
    print '  --rename=mykernel          Custom kernel file name'
    print '  --initramfs=/file          Embed initramfs into the kernel'
    print yellow('   --fixdotconfig             Check and auto fix the kernel config file (experimental)')
    print '  --clean                    Clean precompiled objects only'
    print '  --mrproper                 Clean precompiled objects and remove config file'
    print '  --oldconfig                Ask for new kernel/initramfs options'
    print '  --menuconfig               Interactive kernel options menu'
    print '  --fakeroot=/dir            Append modules to /dir/lib/modules'
    print '  --nooldconfig              Do not ask for new kernel/initramfs options'
    print '  --nomodinstall             Do not install modules'
    print '  --nosaveconfig             Do not save kernel config in /etc/kernels'
    print '  --noboot                   Do not copy kernel to /boot'
    print
    print '  --logfile=/file            Log to file, default to /var/log/kigen.log'
#   print '  -v, --verbose              Give more verbose'
    print '  -d, --debug                Debug verbose'

def print_usage_initramfs():
    print '  --config=/file             Custom master config file'
    print '  --dotconfig=/file          Custom busybox config file'
    print '  --rename=myinitramfs       Custom initramfs file name'
    print '  --menuconfig               Interactive initramfs options menu'
    print '  --linuxrc=/linuxrc[,/file] Include custom linuxrc (files copied over to etc)'
    print '  --splash=<theme>           Include splash support (media-gfx/splashutils must be merged)'
    print '   --sres=YxZ[,YxZ]           Splash resolution, all if not set'
#   print '   --sinitrd=/file            Splash custom initrd.splash (host if found)'
    print '  --disklabel                Include support for UUID/LABEL'
    print '  --luks                     Include LUKS support (host binary if found)'
    print '  --lvm2                     Include LVM2 support (host binary if found)'
#   print '  --evms                    Include evms support (evms must be merged)'
#   print '  --dmraid                  Include dmraid support'
#   print '   --selinux                 Include selinux support in --dmraid'
#   print '  --iscsi                   Include iscsi support'
#   print '  --mdadm                   Include mdadm support (mdadm must be merged)'
    print '  --dropbear                 Include dropbear tools and daemon (host binaries if found)'
    print '   --glibc                    Include host GNU C libraries (required for dns,dropbear)'
    print '   --libncurses               Include host libncurses (required for dropbear)'
    print '   --zlib                     Include host zlib (required for dropbear)'
    print '   --rootpasswd=passwd        Create and set root password (required for dropbear)'
#   print '  --unionfs-fuse            Include unionfs-fuse support'
#   print '  --aufs                    Include aufs support'
#   print '  --firmware=/dir           Include custom firmware support'
    print '  --plugin=/dir[,/dir]       Include list of user generated custom roots'
    print '  --nocache                  Do not use cached data'
    print '  --nohostbin                Do not use host binaries but compile from sources'
    print '  --noboot                   Do not copy initramfs to /boot'
    print 'Tools:'
    print '  --extract=/file            Extract initramfs file'
    print '   --to=/dir                  Custom extracting directory'
    print '  --compress=/dir            Compress directory into initramfs'
    print '   --into=/file               Custom initramfs file'
    print
    print '  --logfile=/file            Log to file, default to /var/log/kigen.log'
#   print '  -v, --verbose              Give more verbose'
    print '  -d, --debug                Debug verbose'

