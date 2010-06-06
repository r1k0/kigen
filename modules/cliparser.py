import sys
import os
import getopt
from stdout import white, green, turquoise, yellow, red

__author__	    = [ 'erick "r1k0" michau - <erick@openchill.org>', \
                    '']
__version__		= "0.9"
__productname__	= os.path.basename(sys.argv[0])
__description__	= "a kernel/initramfs generator."

# parse command line parameters
def parse():
    cli = {}
    verbose = { 'std': '', 	\
                'set': False}

    try:
        topts, targs = getopt.getopt(sys.argv[1:], "ihn", [ \
                                "conf=",                    \
                                "help",                     \
                                "info",                     \
                                "version",                  \
                                "nocolor",                  \
                                "credits"])

        opts, args = getopt.getopt(sys.argv[2:], "hdin", [  \
                                "conf=",                    \
                                "kconf=",                   \
                                "bbconf=",                  \
                                "kernname=",                \
                                "mrproper",                 \
                                "kmenuconfig",              \
                                "bbmenuconfig",             \
                                "allyesconfig",             \
                                "nomodinstall",             \
                                "fakeroot=",                \
                                "allnoconfig",              \
                                "nooldconfig",              \
                                "oldconfig",                \
                                "luks",                     \
                                "lvm2",                     \
                                "dmraid",                   \
                                "iscsi",	    \
                                "logfile=",	    \
                                "evms",		    \
                                "mdadm",	    \
                                "splash",	    \
                                "stheme=",	    \
                                "sres=",	    \
                                "firmware=",	\
                                "disklabel",	\
                                "unionfs-fuse",	\
                                "aufs",		    \
                                "linuxrc=",	    \
                                "nocache",	    \
                                "noboot",	    \
                                "selinux",	    \
                                "help", 	    \
                                "nocolor",	    \
                                "info",		    \
                                "version",	    \
                                "credits",	    \
                                "nosaveconfig", \
                                "debug"])
    except getopt.GetoptError, err:
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
    cli['kconf']		= ''
    cli['kernname']		= ''
    cli['bbconf']		= ''
    cli['info']         = False
    cli['mrproper']     = False
    cli['kmenuconfig']  = False
    cli['bbmenuconfig'] = False
    cli['allyesconfig'] = False
    cli['allnoconfig']  = False
    cli['koldconfig']   = True
    cli['bboldconfig']  = False # because it produces too much output
    cli['luks']         = False
    cli['lvm2']         = False
    cli['dmraid']		= False
    cli['iscsi']		= False
    cli['evms']         = False
    cli['mdadm']		= False
    cli['splash']		= False
    cli['stheme']		= ''
    cli['sres']         = '' # 1024x768
    cli['firmware']		= ''
    cli['disklabel']	= False
    cli['unionfs']		= False
    cli['aufs']         = False
    cli['linuxrc']		= ''
    cli['nomodinstall']	= False
    cli['fakeroot']		= ''
    cli['nocache']		= False
    cli['noboot']		= False
    cli['selinux']		= False
#	quiet				= '2>&1 | tee -a ' + logfile # verbose
#	quiet               = '>>' + logfile + ' 2>&1' # quiet + logfile
    verbose['std']		= '>>' + cli['logfile'] + ' 2>&1'
    cli['color']		= True
    cli['nosaveconfig'] = False

    # single options
    for o, a in topts:
        if o in ("-h", "--help"):
            print_usage(ex=True)
            sys.exit(0)
        elif o in ("-i", "--info"):
            cli['info'] = True
        elif o in ("--version"):
            print_version()
            sys.exit(0)
        elif o in ("--credits"):
            print_credits()
            sys.exit(0)
        elif o in ("--config="):
            cli['config'] = a

    # target options
    for o, a in opts:
        if o in ("-h", "--help"):
            if sys.argv[1] == 'kernel' or sys.argv[1] == 'k':
                print_usage_kernel()
            elif sys.argv[1] == 'all' or sys.argv[1] == 'a':
                print_usage_all()
            elif sys.argv[1] == 'initramfs' or sys.argv[1] == 'i':
                print_usage_initramfs()
            else:
                print_usage()
            sys.exit(0)
        # have to declare logfile here too
        elif o in ("--logfile="):
            cli['logfile'] = a
        elif o in ("-d", "--debug"):
#			quiet = '>>' + logfile + ' 2>&1' # logfile
#			quiet = '2>&1 | tee -a ' + logfile # verbose
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
        elif o in ("-k", "--kconf"):
            cli['kconf'] = a
            cli['koldconfig'] = True # make sure .config is ok
        elif o in ("--kernname"):
            cli['kernname'] = a
        elif o in ("-b", "--bbconf"):
            cli['bbconf'] = a
            cli['bboldconfig'] = True # make sure .config is ok
        elif o in ("--iscsi"):
            cli['iscsi'] = True
        elif o in ("--evms"):
            cli['evms'] = True
        elif o in ("--mdadm"):
            cli['mdadm'] = True
        elif o in ("--mrproper"):
            cli['mrproper'] = True
        elif o in ("--bbmenuconfig"):
            cli['bbmenuconfig'] = True
        elif o in ("--kmenuconfig"):
#			if allyesconfig is True 	\
#			or koldconfig is True 		\
#			or bboldconfig is True		\
#			or allnoconfig is True:
#				print "--menuconfig --allyesconfig --allnoconfig --oldconfig are exclusive."
#				print "Choose only one."
#				sys.exit(2)
            cli['kmenuconfig'] = True
#		elif o in ("--allyesconfig"):
#			if menuconfig is True 		\
#			or koldconfig is True 		\
#			or bboldconfig is True		\
#			or allnoconfig is True:
#				print "--allyesconfig --allnoconfig --menuconfig --oldconfig are exclusive."
#				print "Choose only one."
#				sys.exit(2)
#			allyesconfig = True
#		elif o in ("--allnoconfig"):
#			if menuconfig is True 		\
#			or koldconfig is True 		\
#			or bboldconfig is True		\
#			or allyesconfig is True:
#				print "--allyesconfig --allnoconfig --menuconfig --oldconfig are exclusive."
#				print "Choose only one."
#				sys.exit(2)
#			allnoconfig = 'yes'
        elif o in ("--nooldconfig"):
#			if allyesconfig is True 	\
#			or menuconfig is True		\
#			or allnoconfig is True:
#				print "--oldconfig --menuconfig --allyesconfig --allnoconfig are exclusive."
#				print "Choose only one."
#				sys.exit(2)
            cli['koldconfig'] = False
            cli['bboldconfig'] = False
        elif o in ("--oldconfig"):
            cli['koldconfig'] = True
            cli['bboldconfig'] = True
        elif o in ("--splash"):
            cli['splash'] = True
        elif o in ("--firmware"):
            if os.path.isdir(a):
                cli['firmware'] = a
            else:
                print "%s is not a directory" % a
                sys.exit(2)
        elif o in ("--nomodinstall"):
            cli['nomodinstall'] = True
        elif o in ("--fakeroot"):
            if os.path.isdir(a):
                cli['fakeroot'] = a
            else:
                print "%s is not a directory" % a
                sys.exit(2)
        elif o in ("--unionfs-fuse"):
            cli['unionfs'] = True
        elif o in ("--aufs"):
            cli['aufs'] = True
        elif o in ("--linuxrc"):
            cli['linuxrc'] = a
        elif o in ("--stheme"):
            cli['stheme'] = a
        elif o in ("--sres"):
            cli['sres'] = a
        elif o in ("--nocache"):
            cli['nocache'] = True
        elif o in ("--noboot"):
            cli['noboot'] = True
        elif o in ("--selinux"):
            cli['selinux'] = True
        elif o in ("-n", "--nocolor"):
            cli['color'] = False
        elif o in ("--nosaveconfig"):
            cli['nosaveconfig'] = True
        elif o in ("--config="):
            cli['config'] = a
        else:
            assert False, "uncaught option"

    return cli, verbose

def print_version():
    print "%s" % (__version__)

def print_credits():
    print 'Copyright 2010 r1k0'
    print 'Portions copyright 2003-2005 Gentoo Foundation (default linuxrc)'
    print 'Distributed under the terms of the GNU General Public License v2'
    print 
    print 'Alphabetical list of authors:'
    print
    for i in __author__:
        print i

def print_usage(ex=False):
    print
    print white('  a GNU/Linux kernel|initramfs generator')
    print
    print white('Usage')+":"
    print "  " + turquoise(os.path.basename(sys.argv[0])) + green(' <target|options>') + yellow(' [parameters]')
    print
    print green("Options") + ":"
#    print white('  -i, --info') + "             Show " + turquoise(os.path.basename(sys.argv[0])) + " configuration"
    print '  --conf=/file           Custom master config file'
    print "  -h, --help             This and examples"
    print "  -n, --nocolor          Do not colorize output"
    print "  --version              Version"
    print "  --credits              Credits and license"
    print
    print green('Targets')+":"
    print '  k, kernel' + "              Build kernel/modules"
    print '  i, initramfs' + "           Build initramfs"
    print '  a, all' + "                 Build kernel/modules/initramfs"
#	print '  moo' + '			         Ask Larry.'
    print
    print yellow('Parameters') + " help menu:"

    print "  " + os.path.basename(sys.argv[0]) + " " + 'kernel' + "           -h, --help"
    print "  " + os.path.basename(sys.argv[0]) + " " + 'initramfs' + "        -h, --help"
    print "  " + os.path.basename(sys.argv[0]) + " " + 'all' + "              -h, --help"
    if ex is True:
        print
        print green('Examples') + ":"
        print "  " + os.path.basename(sys.argv[0]) + " initramfs --disklabel --luks --lvm2 --splash --stheme=gentoo"
        print "  " + os.path.basename(sys.argv[0]) + " kernel --kconf=/file --kmenuconfig --nomodinstall --noboot --nocolor"
        print "  " + os.path.basename(sys.argv[0]) + " all --luks --lvm2 --splash --kmenuconfig --firmware=/lib/firmware"

def print_usage_bzImage(no_extra_options=False):
    print "  --kconf=/file          Custom kernel config file (full path)"
    print "  --kernname=mykernel    Custom kernel file name"
    print "  --nooldconfig          Will not ask for new kernel/initramfs options"
    print "  --mrproper             Clean precompiled objects"
    print "  --oldconfig            Will ask for new kernel/initramfs options"
    print "  --kmenuconfig          Interactive kernel options menu"
#   print "  --allyesconfig         Say yes to all kernel/busybox options"
#   print "  --allnoconfig          Say no  to all kernel options and modules only"
    if no_extra_options is False:
        print_usage_target_common()

def print_usage_kernel(no_extra_options=False):
    print green('Kernel') + ' parameters'
    print_usage_bzImage(no_extra_options=True)
    print "  --nomodinstall         Do not install modules"
    print "  --nosaveconfig         Do not save kernel config in /etc/kernels"
    print "  --fakeroot=/dir        Append modules to /dir/lib/modules"
    if no_extra_options is False:
        print_usage_target_common()

def print_usage_initramfs():
    print green('Initramfs') + ' parameters'
    print "  --bbconf=/file         Custom busybox config file (full path)"
    print "  --bbmenuconfig         Interactive initramfs options menu"
    print "  --linuxrc=/file        Custom linuxrc /init for the initramfs"
    print "  --disklabel            Include support for disklabel and UUID"
    print "  --luks                 Include LUKS support (cryptsetup must be statically merged)"
    print "  --lvm2                 Include LVM2 support"
    print yellow("  --evms                 Include evms support (evms must be merged)")
    print yellow("  --dmraid               Include dmraid support")
    print yellow("   --selinux              Include selinux support in --dmraid")
    print yellow("  --iscsi                Include iscsi support")
    print yellow("  --mdadm                Include mdadm support (mdadm must be merged)")
    print "  --splash               Include splash support (splashutils must be merged)"
    print "   --stheme=<theme>       Splash theme, gentoo is the default"
    print "   --sres=INTxINT         Splash resolution,comma separated list of INTxINT, all if not set"
    print yellow("  --unionfs-fuse         Include unionfs-fuse support")
    print red("  --aufs                 Include aufs support")
    print yellow("  --firmware=/dir        Include custom firmware support")
    print "  --nocache              Do not use cached data"
    print_usage_target_common()

def print_usage_target_common():
    print green('Common') + ' parameters'
    print '  --conf=/file           Use a custom master config file'
    print "  --noboot               Do not copy kernel/initramfs to /boot"
    print "  --logfile=/file        Log to file, default to /var/log/kigen.log"
    print "  -n, --nocolor          Do not colorize output"
    print "  -d, --debug            Show more output"

def print_usage_all():
    print_usage_kernel(no_extra_options=True)
    print_usage_initramfs()

