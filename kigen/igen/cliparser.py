import sys
import os
import getopt
from stdout import white, green, turquoise, yellow, red
from credits import author, productname, version, description, contributor

# parse command line parameters
def parse():
    cli = {}
    verbose = { 'std': '',  \
                'set': False}

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hdin", [  \
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
                                "splash=",       \
#                                "stheme=",      \
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
                                "nocolor",      \
                                "info",         \
                                "version",      \
                                "credits",      \
                                "nosaveconfig", \
                                "nohostbin",    \
                                "glibc",        \
                                "rename=",      \
                                "plugin=",      \
                                "debug"])
    except getopt.GetoptError, err:
        print str(err) # "option -a not recognized"
        print_usage()
        sys.exit(2)

    # this has to be taken care before quiet is initialized
    # hence the extra loop, catch --logfile before all
    cli['logfile'] = '/var/log/igen.log'
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
#    cli['splash']       = False
#    cli['stheme']       = ''
    cli['sres']         = '' # 1024x768
    cli['sinitrd']      = '' # a custom initrd.splash file
    cli['firmware']     = ''
    cli['disklabel']    = False
    cli['unionfs']      = False
    cli['aufs']         = False
    cli['linuxrc']      = ''
    cli['dropbear']          = False
    cli['nocache']      = False
    cli['noboot']       = False
    cli['selinux']      = False
#   quiet               = '2>&1 | tee -a ' + logfile # verbose
#   quiet               = '>>' + logfile + ' 2>&1' # quiet + logfile
    verbose['std']      = '>>' + cli['logfile'] + ' 2>&1'
    cli['color']        = True
    cli['nosaveconfig'] = False
    cli['nohostbin']    = False
    cli['glibc']        = False
    cli['rename']       = ''
    cli['plugin']       = ''

    # target options
    for o, a in opts:
        if o in ("-h", "--help"):
            print_usage()
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
        elif o in ("-d", "--debug"):
#           quiet = '>>' + logfile + ' 2>&1' # logfile
#           quiet = '2>&1 | tee -a ' + logfile # verbose
            verbose['std'] = '2>&1 | tee -a ' + cli['logfile']
            verbose['set'] = True
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
#       elif o in ("--allyesconfig"):
#           if menuconfig is True       \
#           or koldconfig is True       \
#           or bboldconfig is True      \
#           or allnoconfig is True:
#               print "--allyesconfig --allnoconfig --menuconfig --oldconfig are exclusive."
#               print "Choose only one."
#               sys.exit(2)
#           allyesconfig = True
#       elif o in ("--allnoconfig"):
#           if menuconfig is True       \
#           or koldconfig is True       \
#           or bboldconfig is True      \
#           or allyesconfig is True:
#               print "--allyesconfig --allnoconfig --menuconfig --oldconfig are exclusive."
#               print "Choose only one."
#               sys.exit(2)
#           allnoconfig = 'yes'
        elif o in ("--nooldconfig"):
#           if allyesconfig is True     \
#           or menuconfig is True       \
#           or allnoconfig is True:
#               print "--oldconfig --menuconfig --allyesconfig --allnoconfig are exclusive."
#               print "Choose only one."
#               sys.exit(2)
            cli['oldconfig'] = False
        elif o in ("--oldconfig"):
            cli['oldconfig'] = True
        elif o in ("--splash"):
#            cli['splash'] = True
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
#        elif o in ("--stheme"):
#            cli['stheme'] = a
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
        elif o in ("-n", "--nocolor"):
            cli['color'] = False
        elif o in ("--config="):
            cli['config'] = a
        elif o in ("--dropbear"):
            cli['dropbear'] = True
        elif o in ("--nohostbin"):
            cli['nohostbin'] = True
        elif o in ("--glibc"):
            cli['glibc'] = True
        elif o in ("--rename"):
            cli['rename'] = a
        elif o in ("--plugin"):
            cli['plugin'] = a # a is a list
        else:
            assert False, "uncaught option"

    return cli, verbose

def print_version():
    print '%s' % (version)

def print_credits():
    print 'Copyright 2010 r1k0'
    print 'Portions copyright 2003-2005 Gentoo Foundation (default linuxrc)'
    print 'Distributed under the terms of the GNU General Public License v2'
    print 
    print 'Alphabetical list of authors:'
    print
    for i in author:
        print i
    print 'Alphabetical list of contributors:'
    print
    for i in contributor:
        print i

def print_usage():
    print
    print white('  a GNU/Linux initramfs generator')
    print
    print white('Usage')+':'
    print '      ' + turquoise(os.path.basename(sys.argv[0])) + green(' <options>') 
    print
    print green('Options') + ':'
    print '  -h, --help             This'
    print '  --config=/file         Custom master config file'
    print '  -n, --nocolor          Do not colorize output'
    print '  -d, --debug            Show more output'
    print '  --logfile=/file        Log to file, default to /var/log/igen.log'
    print '  --version              Version'
    print '  --credits              Credits and license'
    print
    print '  --dotconfig=/file      Custom busybox config file'
    print '  --rename=myinitramfs   Custom initramfs file name'
    print '  --menuconfig           Interactive initramfs options menu'
    print '  --linuxrc=/file        Custom linuxrc /init'
    print '  --disklabel            Include support for disklabel and UUID'
    print '  --luks                 Include LUKS support (host binary if found)'
    print '  --lvm2                 Include LVM2 support (host binary if found)'
#    print yellow('  --evms                 Include evms support (evms must be merged)')
#    print yellow('  --dmraid               Include dmraid support')
#    print yellow('   --selinux              Include selinux support in --dmraid')
#    print yellow('  --iscsi                Include iscsi support')
#    print yellow('  --mdadm                Include mdadm support (mdadm must be merged)')
    print '  --glibc                Include host GNU C libraries (required for dns)'
#    print yellow('  --dropbear             Include dropbear tools and daemon (host binaries if found)')
    print '  --splash=<theme>       Include splash support (media-gfx/splashutils must be merged)'
    print '   --sres=YxZ[,YxZ]       Splash resolution, all if not set'
#    print yellow('   --sinitrd=/file        Splash custom initrd.splash (host if found)')
#    print yellow('  --unionfs-fuse         Include unionfs-fuse support')
#    print red('  --aufs                 Include aufs support')
#    print yellow('  --firmware=/dir        Include custom firmware support')
    print '  --plugin=/dir[,/dir]   Include list of user generated custom roots'
    print '  --nocache              Do not use cached data'
    print '  --nohostbin            Do not use host binaries but compile from sources'
    print '  --noboot               Do not copy initramfs to /boot'
