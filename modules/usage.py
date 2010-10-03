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


def print_usage_kernel(cli, master_conf, kernel_conf):
    print 'Parameter:\t\t     Default value:\tDescription:'
    print
    print  'Kernel:'
    print '  --dotconfig=/file          "'+kernel_conf['dotconfig']+'"',
    print '\t\tCustom kernel .config file'

    print '  --initramfs=/file          "'+kernel_conf['initramfs']+'"',
    print '\t\tEmbed initramfs into the kernel'

    print yellow('   --fixdotconfig           '),
    print kernel_conf['fixdotconfig'],
    print yellow('\t\t Check and auto fix the kernel config file (experimental)')

    print '  --clean                   ',
    print kernel_conf['clean'],
    print '\t\tClean precompiled objects only'

    print '  --mrproper                ',
    print kernel_conf['mrproper'],
    print '\t\tClean precompiled objects and remove config file'

#    print '  --oldconfig               ',
#    print kernel_conf['oldconfig'],
#    print '\t\tAsk for new kernel options if any'

    print '  --menuconfig              ',
    print kernel_conf['menuconfig'],
    print '\t\tInteractive kernel options menu'

    print '  --fakeroot=/dir            "'+cli['fakeroot']+'"\t\tAppend modules to /dir/lib/modules'

    print '  --nooldconfig             ',
    print kernel_conf['nooldconfig'],
    print '\t\tDo not ask for new kernel/initramfs options'

    print '  --nomodinstall            ',
    print kernel_conf['nomodinstall'],
    print '\t\tDo not install modules'
    print
    print 'Misc:'
    print '  --nosaveconfig            ',
    print kernel_conf['nosaveconfig'],
    print '\t\tDo not save kernel config in /etc/kernels'

    print '  --noboot                  ',
    print kernel_conf['noboot'],
    print '\t\tDo not copy kernel to /boot'

    print '  --rename=/file             "'+kernel_conf['rename']+'"',
    print '\t\tCustom kernel file name'

    print '  --logfile=/file            "'+master_conf['logfile']+'"',
    print '\t\tLog to file'

    print '  --debug, -d                '+master_conf['debug']+'\t\tDebug verbose'
    print
    print 'Handy tools:'
    print '  --getdotconfig=/vmlinux    "'+cli['getdotconfig']+'"\t\t\tExtract .config from compiled binary kernel (if IKCONFIG has been set)'

def print_usage_initramfs(cli, initramfs_conf, modules_conf):
    print 'Parameter:\t\t     Default value:\tDescription:'
    print
    print 'Linuxrc:'
    print '  --linuxrc=/linuxrc[,/file] "'+initramfs_conf['linuxrc']+'"',
    print '\t\tInclude custom linuxrc (files copied over to etc)'
    print
    print 'Busybox:'
#    print '  --dotconfig=/file          "'+temp['work'] + '/busybox-' + master_conf['busybox-version']+'/.config"'
    print '  --dotconfig=/file          "'+initramfs_conf['dotconfig']+'"',
    print '\t\tCustom busybox config file'

    print '  --defconfig               ',
    print initramfs_conf['defconfig'], # bool
    print '\t\tSet .config to largest generic options'

    print '  --oldconfig               ',
    print initramfs_conf['oldconfig'], # bool
    print '\t\tAsk for new busybox options if any'

    print '  --menuconfig              ',
    print initramfs_conf['menuconfig'], # bool
    print '\t\tInteractive busybox options menu'
    print
    print 'Features:'
    print '  --splash=<theme>           "'+initramfs_conf['splash']+'"',
    print '\t\tInclude splash support (splashutils must be merged)'

    print '   --sres=YxZ[,YxZ]          "'+initramfs_conf['sres']+'"',
    print '\t\t Splash resolution, all if not set'
#   print '   --sinitrd=/file           ""                       Splash custom initrd.splash (host if found)'

    print '  --disklabel               ',
    print initramfs_conf['disklabel'], # bool
    print '\t\tInclude support for UUID/LABEL'

    print '  --luks                    ',
    print initramfs_conf['luks'], # bool 
    print '\t\tInclude LUKS support (host binary if found)'

    print '  --lvm2                    ',
    print initramfs_conf['lvm2'], # bool
    print '\t\tInclude LVM2 support (host binary if found)'
#   print '  --evms                     False                   Include evms support (evms must be merged)'
#   print '  --dmraid                   False                   Include dmraid support'
#   print '   --selinux                 False                    Include selinux support in --dmraid'
#   print '  --iscsi                    False                   Include iscsi support'
#   print '  --mdadm                    False                   Include mdadm support (mdadm must be merged)'

    print '  --dropbear                ',
    print initramfs_conf['dropbear'], # bool
    print '\t\tInclude dropbear tools and daemon (host binaries if found)'

    print '   --debugflag              ',
    print initramfs_conf['debugflag'], # bool
    print '\t\t Compile dropbear with #define DEBUG_TRACE in debug.h'

    print '  --rootpasswd=<passwd>      "'+cli['rootpasswd']+'"',
    print '\t\tCreate and set root password (required for dropbear)'

#   print '  --unionfs-fuse             False                   Include unionfs-fuse support'
#   print '  --aufs                     False                   Include aufs support'
#   print '  --firmware=/dir            ""                      Include custom firmware support'

    print '  --keymaps                 ',
    print initramfs_conf['keymaps'], # bool
    print '\t\tInclude all keymaps'

    print '  --ttyecho                 ',
    print initramfs_conf['ttyecho'], # bool
    print '\t\tInclude the handy ttyecho.c tool'

    print '  --strace                  ',
    print initramfs_conf['strace'], # bool
    print '\t\tInclude the strace binary tool'

    print '  --screen                  ',
    print initramfs_conf['screen'], # bool
    print '\t\tInclude the screen binary tool'

    print '  --plugin=/dir[,/dir]       "'+initramfs_conf['plugin']+'"',
    print '\t\tInclude list of user generated custom roots'
    print
    print 'Libraries:'
    print '  --glibc                   ',
    print initramfs_conf['glibc'], # bool
    print '\t\tInclude host GNU C libraries (required for dns,dropbear)'

    print '  --libncurses              ',
    print initramfs_conf['libncurses'], # bool
    print '\t\tInclude host libncurses (required for dropbear)'

    print '  --zlib                    ',
    print initramfs_conf['zlib'], # bool
    print '\t\tInclude host zlib (required for dropbear)'
    print
    print 'Misc:'
    print '  --nocache                 ',
    print initramfs_conf['nocache'],
    print '\t\tDelete previous cached data on startup'

    print '  --hostbin                 ',
    print initramfs_conf['hostbin'],
    print '\t\tUse host binaries over sources when possible'

    print '  --noboot                  ',
    print initramfs_conf['noboot'],
    print '\t\tDo not copy initramfs to /boot'

    print '  --rename=/file             "'+initramfs_conf['rename']+'"'
    print '\t\t\t\t\t\tCustom initramfs file name'

    print '  --logfile=/file            "'+master_conf['logfile']+'"',
    print '\t\tLog to file'

    print '  --debug, -d                "'+master_conf['debug']+'"',
    print '\t\tDebug verbose'
    print
    print 'Handy tools:'
    print '  --extract=/file            "'+cli['extract']+'"                 Extract initramfs file'
    print '   --to=/dir                 "'+cli['to']+'"'
    print '\t\t\t\t\t\t Custom extracting directory'

    print '  --compress=/dir            "'+cli['compress']+'"                 Compress directory into initramfs'
    print '   --into=/file              "'+cli['into']+'"'
    print '\t\t\t\t\t\t Custom initramfs file'
