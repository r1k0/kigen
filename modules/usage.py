import sys
import os
#from getopt import getopt, GetoptError
from stdout import white, green, turquoise, yellow, red
from credits import author, productname, version, description, contributor
 
from default import master_conf, temp, kerneldir
from utils.misc import *

# WARN don't import logging here

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
    print ' '+os.path.basename(sys.argv[0])+' i --splash=sabayon --disklabel --luks --lvm2 --dropbear --debugflag --rootpasswd=mypasswd --keymaps --ttyecho --strace --screen --glibc --zlib --libncurses --defconfig --nocache'
    print ' '+os.path.basename(sys.argv[0])+' --extract=/file i --to=/dir'
    print ' '+os.path.basename(sys.argv[0])+' initramfs --compress=/dir --into=/file'


def print_usage_kernel(cli):
    print 'Parameter:\t\t     Default value:\tDescription:'
    print
    print 'Config:'
    print '  --config=/dir              "'+cli['config']+'"\tCustom master config dir'
    print
    print  'Kernel:'
    print '  --dotconfig=/file          "'+cli['kerneldir']+'/.config'+'"'
    print '\t\t\t\t\t\tCustom kernel .config file'
    print '  --initramfs=/file          "'+cli['initramfs']+'"\t\t\tEmbed initramfs into the kernel'
    print yellow('   --fixdotconfig           '),
    print cli['fixdotconfig'],
    print yellow('\t\t Check and auto fix the kernel config file (experimental)')
    print '  --clean                   ',
    print cli['clean'],
    print '\t\tClean precompiled objects only'
    print '  --mrproper                ',
    print cli['mrproper'],
    print '\t\tClean precompiled objects and remove config file'
    print '  --oldconfig               ',
    print cli['oldconfig'],
    print '\t\tAsk for new kernel options if any'
    print '  --menuconfig              ',
    print cli['menuconfig'],
    print '\t\tInteractive kernel options menu'
    print '  --fakeroot=/dir            "'+cli['fakeroot']+'"\t\tAppend modules to /dir/lib/modules'
    print '  --nooldconfig             ',
    print not cli['oldconfig'],
    print '\t\tDo not ask for new kernel/initramfs options'
    print '  --nomodinstall            ',
    print cli['nomodinstall'],
    print '\t\tDo not install modules'
    print
    print 'Misc:'
    print '  --nosaveconfig            ',
    print cli['nosaveconfig'],
    print '\t\tDo not save kernel config in /etc/kernels'
    print '  --noboot                  ',
    print cli['noboot'],
    print '\t\tDo not copy kernel to /boot'
    print '  --rename=/file             "'+cli['rename']+'"'
    print '\t\t\t\t\t\tCustom kernel file name'
    print '  --logfile=/file            "'+cli['logfile']+'"Log to file'
    print '  --debug, -d                False\t\tDebug verbose'
    print
    print 'Tools:'
    print '  --getdotconfig=/vmlinux    "'+cli['getdotconfig']+'"\t\t\tExtract .config from compiled binary kernel (if IKCONFIG has been set)'

def print_usage_initramfs(cli):
    # passing cli is supposed to grab default from parse()
    print 'Parameter:\t\t     Default value:\tDescription:'
    print
    print 'Config:'
    print '  --config=/dir              "'+cli['config']+'"  Custom master config dir'
    print
    print 'Linuxrc:'
    print '  --linuxrc=/linuxrc[,/file] "'+cli['linuxrc']+'"                 Include custom linuxrc (files copied over to etc)'
    print
    print 'Busybox:'
    print '  --dotconfig=/file          "'+temp['work'] + '/busybox-' + master_config['busybox-version']+'/.config"'
    print '\t\t\t\t\t\tCustom busybox config file'
    print '  --defconfig               ',
    print cli['defconfig'], # bool
    print '\t\tSet .config to largest generic options'
    print '  --oldconfig               ',
    print cli['oldconfig'], # bool
    print '\t\tAsk for new busybox options if any'
    print '  --menuconfig              ',
    print cli['menuconfig'], # bool
    print '\t\tInteractive busybox options menu'
    print
    print 'Features:'
    print '  --splash=<theme>           "'+cli['splash']+'"                 Include splash support (splashutils must be merged)'
    print '   --sres=YxZ[,YxZ]          "'+cli['sres']+'"                  Splash resolution, all if not set'
#   print '   --sinitrd=/file           ""                       Splash custom initrd.splash (host if found)'
    print '  --disklabel               ',
    print cli['disklabel'], # bool
    print '\t\tInclude support for UUID/LABEL'
    print '  --luks                    ',
    print cli['luks'], # bool 
    print '\t\tInclude LUKS support (host binary if found)'
    print '  --lvm2                    ',
    print cli['lvm2'], # bool
    print '\t\tInclude LVM2 support (host binary if found)'
#   print '  --evms                     False                   Include evms support (evms must be merged)'
#   print '  --dmraid                   False                   Include dmraid support'
#   print '   --selinux                 False                    Include selinux support in --dmraid'
#   print '  --iscsi                    False                   Include iscsi support'
#   print '  --mdadm                    False                   Include mdadm support (mdadm must be merged)'
    print '  --dropbear                ',
    print cli['dropbear'], # bool
    print '\t\tInclude dropbear tools and daemon (host binaries if found)'
    print '   --debugflag              ',
    print cli['debugflag'], # bool
    print '\t\t Compile dropbear with #define DEBUG_TRACE in debug.h'
    print '  --rootpasswd=<passwd>      "'+cli['rootpasswd']+'"                 Create and set root password (required for dropbear)'
#   print '  --unionfs-fuse             False                   Include unionfs-fuse support'
#   print '  --aufs                     False                   Include aufs support'
#   print '  --firmware=/dir            ""                      Include custom firmware support'
    print '  --keymaps                 ',
    print cli['keymaps'], # bool
    print '\t\tInclude all keymaps'
    print '  --ttyecho                 ',
    print cli['ttyecho'], # bool
    print '\t\tInclude the handy ttyecho.c tool'
    print '  --strace                  ',
    print cli['strace'], # bool
    print '\t\tInclude the strace binary tool'
    print '  --screen                  ',
    print cli['screen'], # bool
    print '\t\tInclude the screen binary tool'
    print '  --plugin=/dir[,/dir]       "'+cli['plugin']+'"                 Include list of user generated custom roots'
    print
    print 'Libraries:'
    print '  --glibc                   ',
    print cli['glibc'], # bool
    print '\t\tInclude host GNU C libraries (required for dns,dropbear)'
    print '  --libncurses              ',
    print cli['libncurses'], # bool
    print '\t\tInclude host libncurses (required for dropbear)'
    print '  --zlib                    ',
    print cli['zlib'], # bool
    print '\t\tInclude host zlib (required for dropbear)'
    print
    print 'Misc:'
    print '  --nocache                 ',
    print cli['nocache'],
    print '\t\tDelete previous cached data on startup'
    print '  --hostbin                 ',
    print cli['hostbin'],
    print '\t\tUse host binaries over sources when possible'
    print '  --noboot                  ',
    print cli['noboot'],
    print '\t\tDo not copy initramfs to /boot'
    print '  --rename=/file             "'+cli['rename']+'"'
    print '\t\t\t\t\t\tCustom initramfs file name'
    print '  --logfile=/file            "'+cli['logfile']+'"'
    print '\t\t\t\t\t\tLog to file'
    print '  --debug, -d                False              Debug verbose'
    print
    print 'Tools:'
    print '  --extract=/file            "'+cli['extract']+'"                 Extract initramfs file'
    print '   --to=/dir                 "'+cli['to']+'"'
    print '\t\t\t\t\t\t Custom extracting directory'
    print '  --compress=/dir            "'+cli['compress']+'"                 Compress directory into initramfs'
    print '   --into=/file              "'+cli['into']+'"'
    print '\t\t\t\t\t\t Custom initramfs file'
