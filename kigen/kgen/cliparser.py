import sys
import os
import getopt
from stdout import white, green, turquoise, yellow, red
from credits import author, productname, version, description, contributor

# parse command line parameters
def parse():
    cli = {}
    verbose = { 'std': '', 	\
                'set': False}

    try:
        opts, args = getopt.getopt(sys.argv[1:], "idhn", [ \
                                "config=",                  \
                                "help",                     \
                                "info",                     \
                                "version",                  \
                                "nocolor",                  \
                                "credits",                  \
                                "conf=",                    \
                                "dotconfig=",               \
                                "bbconf=",                  \
                                "rename=",                \
                                "mrproper",                 \
                                "clean",                    \
                                "menuconfig",               \
                                "allyesconfig",             \
                                "nomodinstall",             \
                                "fakeroot=",                \
                                "allnoconfig",              \
                                "nooldconfig",              \
                                "oldconfig",                \
                                "logfile=",	                \
                                "noboot",	                \
                                "nosaveconfig",             \
                                "nohostbin",                \
                                "debug"])
    except getopt.GetoptError, err:
        print str(err) # "option -a not recognized"
        print_usage()
        sys.exit(2)

    # this has to be taken care before quiet is initialized
    # hence the extra loop, catch --logfile before all
    cli['logfile'] = '/var/log/kgen.log'
    for o, a in opts:
        if o in ("--logfile"):
            cli['logfile'] = a
    # default
    cli['config']       = '/etc/kigen.conf'
    cli['dotconfig']    = ''
    cli['rename']		= ''
    cli['info']         = False
    cli['mrproper']     = False
    cli['menuconfig']   = False
    cli['clean']        = False
    cli['allyesconfig'] = False
    cli['allnoconfig']  = False
    cli['oldconfig']    = True
    cli['nomodinstall']	= False
    cli['fakeroot']		= ''
    cli['nocache']		= False
    cli['noboot']		= False
#	quiet				= '2>&1 | tee -a ' + logfile # verbose
#	quiet               = '>>' + logfile + ' 2>&1' # quiet + logfile
    verbose['std']		= '>>' + cli['logfile'] + ' 2>&1'
    cli['color']		= True
    cli['nosaveconfig'] = False

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
#			quiet = '>>' + logfile + ' 2>&1' # logfile
#			quiet = '2>&1 | tee -a ' + logfile # verbose
            verbose['std'] = '2>&1 | tee -a ' + cli['logfile']
            verbose['set'] = True
        elif o in ("-k", "--dotconfig"):
            cli['dotconfig'] = a
            cli['oldconfig'] = True # make sure .config is ok
        elif o in ("--rename"):
            cli['rename'] = a
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
        elif o in ("-n", "--nocolor"):
            cli['color'] = False
        elif o in ("--nosaveconfig"):
            cli['nosaveconfig'] = True
        elif o in ("--config="):
            cli['config'] = a
        elif o in ("--clean"):
            cli['clean'] = True
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

def print_usage(ex=False):
    print
    print white('  a GNU/Linux kernel generator')
    print
    print white('Usage')+':'
    print '      ' + turquoise(os.path.basename(sys.argv[0])) + green(' <options>')
    print
    print green('Options') + ':'
    print '  -h, --help             This'
    print '  --config=/file         Custom master config file'
    print '  -n, --nocolor          Do not colorize output'
    print '  -d, --debug            Show more output'
    print '  --logfile=/file        Log to file, default to /var/log/kgen.log'
    print '  --version              Version'
    print '  --credits              Credits and license'
    print
    print '  --dotconfig=/file      Custom kernel config file (full path)'
    print '  --rename=mykernel      Custom kernel file name'
    print '  --nooldconfig          Will not ask for new kernel/initramfs options'
    print '  --mrproper             Clean precompiled objects and remove config file'
    print '  --clean                Clean precompiled objects only'
    print '  --oldconfig            Will ask for new kernel/initramfs options'
    print '  --menuconfig           Interactive kernel options menu'
    print '  --nomodinstall         Do not install modules'
    print '  --nosaveconfig         Do not save kernel config in /etc/kernels'
    print '  --fakeroot=/dir        Append modules to /dir/lib/modules'
    print '  --noboot               Do not copy kernel to /boot'
