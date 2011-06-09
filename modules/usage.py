import sys
import os
import stdout
import credits
import utils.misc

def print_version():
    print(stdout.green('%s' % credits.version))

def print_credits():
    print('Copyright 2010 r1k0')
    print('Portions copyright 2003-2005 Gentoo Foundation (default linuxrc)')
    print('Distributed under the terms of the GNU General Public License v2')
    print() 
    print('Alphabetical list of authors:')
    print()
    for i in credits.author:
        print(stdout.green(i))
    print('Alphabetical list of awesome contributors:')
    print()
    for i in credits.contributor:
        print(stdout.green(i))

def print_usage():
    print()
    print('  a '+stdout.white('Portage')+' kernel|initramfs generator')
    print()
    print('Usage'+':')
    print('      '+stdout.white(sys.argv[0])+' <'+stdout.green('options')+'|'+stdout.turquoise('target')+'>'+' ['+stdout.turquoise('parameters')+']')
    print()
    print(stdout.green('Options') + ':')
    print('  --help, -h                 This and examples')
    print('  --nocolor, -n              Do not colorize output')
    print('  --version                  Version')
    print('  --credits                  Credits and license')
    print()
    print(stdout.turquoise('Targets')+':')
    print('  kernel, k                  Build kernel/modules')
    print('  initramfs, i               Build initramfs')
    print()
    print(stdout.turquoise('Parameters')+':')
    print(' '+os.path.basename(sys.argv[0])+' kernel'+'                --help, -h')
    print(' '+os.path.basename(sys.argv[0])+' initramfs'+'             --help, -h')

def print_examples():
    print()
    print(stdout.white('Examples')+':')
    print(' '+os.path.basename(sys.argv[0])+' kernel --fixdotconfig=splash')
    print(' '+os.path.basename(sys.argv[0])+' --clean --menuconfig k')
    print(' '+os.path.basename(sys.argv[0])+' k --initramfs=/myinitramfsfile')
    print(' '+os.path.basename(sys.argv[0])+' i --splash=sabayon')
    print(' '+os.path.basename(sys.argv[0])+' --disklabel --lvm2 --splash=sabayon --luks -d -n initramfs')
    print(' '+os.path.basename(sys.argv[0])+' i --luks --lvm2 --disklabel --splash=sabayon --glibc --hostbin')
    print(' '+os.path.basename(sys.argv[0])+' i --splash=sabayon --disklabel --luks --lvm2 --dropbear --debugflag --rootpasswd=mypasswd --keymaps --ttyecho --strace --screen --glibc --zlib --libncurses --defconfig --nocache')
    print(' '+os.path.basename(sys.argv[0])+' --extract=/file i --to=/dir')
    print(' '+os.path.basename(sys.argv[0])+' initramfs --compress=/dir --into=/file')


def print_usage_kernel(cli, master_conf, kernel_conf):
    print('Parameter:\t\t    Config value:\tDescription:')
    print()
    print('Kernel:')
    print('  --dotconfig=/file         "'+kernel_conf['dotconfig']+'"', end='')
    print('\t\tCustom kernel .config file')

    print('  --initramfs=/file         "'+kernel_conf['initramfs']+'"', end='')
    print('\t\tEmbed initramfs into the kernel')

    if kernel_conf['fixdotconfig'] != '':
        if len(kernel_conf['fixdotconfig']) <= 4:
            tab = '\t\t'
        elif len(kernel_conf['fixdotconfig']) > 4 and len(kernel_conf['fixdotconfig']) < 7:
            tab = '\t\t'
        elif len(kernel_conf['fixdotconfig']) > 7 and len(kernel_conf['fixdotconfig']) < 12:
            tab = '\t'
        elif len(kernel_conf['fixdotconfig']) > 12:
            tab = ''
    else:
        tab = '\t\t'
    print(stdout.yellow('  --fixdotconfig=<feature>  '), end='')
    print('"'+kernel_conf['fixdotconfig']+'"', end='')
    print(tab+'Check and auto fix the kernel config file (experimental)')
    print('\t\t\t\t\t splash,initramfs,selinux,pax supported (writes to .config)')

    print('  --clean                   ', end='')
    print(kernel_conf['clean'], end='')
    print('\tClean precompiled objects only')

    print('  --mrproper                ', end='')
    print(kernel_conf['mrproper'], end='')
    print('\tClean precompiled objects and remove config file')

    print('  --menuconfig              ', end='')
    print(kernel_conf['menuconfig'], end='')
    print('\tInteractive kernel options menu')

    print('  --fakeroot=/dir           "'+cli['fakeroot']+'"\t\tAppend modules to /dir/lib/modules')

    print('  --nooldconfig             ', end='')
    print(kernel_conf['nooldconfig'], end='')
    print('\tDo not ask for new kernel/initramfs options')

    print('  --nomodinstall            ', end='')
    print(kernel_conf['nomodinstall'], end='')
    print('\tDo not install modules')

    print('  --nomodules               ', end='')
    print(kernel_conf['nomodules'], end='')
    print('\tDo not compile or install modules')
    print()

    print('Misc:')
    print('  --nosaveconfig            ', end='')
    print(kernel_conf['nosaveconfig'], end='')
    print('\tDo not save kernel config in /etc/kernels')

    print('  --noboot                  ', end='')
    print(kernel_conf['noboot'], end='')
    print('\tDo not copy kernel to /boot')

    print('  --rename=/file            "'+kernel_conf['rename']+'"', end='')
    print('\t\tCustom kernel file name')

    print('  --logfile=/file           "'+master_conf['logfile']+'"', end='')
    print() #'\t\tLog to file'

    print('  --debug, -d               '+master_conf['debug']+'\tDebug verbose')
    print()
    print('Handy tools:')
    print('  --getdotconfig=/vmlinux   "'+cli['getdotconfig']+'"\t\tExtract .config from compiled binary kernel (if IKCONFIG has been set)')

def print_usage_initramfs(cli, master_conf, initramfs_conf, modules_conf):
    print('Parameter:\t\t    Config value:\tDescription:')
    print()

    print('Linuxrc:')
    print('  --linuxrc=/linuxrc[,/file]"'+initramfs_conf['linuxrc']+'"', end='')
    print('\t\t\tInclude custom linuxrc (files copied over to etc)')
    print()

    print('Busybox:')
    print('  --dotconfig=/file         "'+initramfs_conf['dotconfig']+'"', end='')
    print('\t\t\tCustom busybox config file')
    print('  --defconfig               ', end='')
    print(initramfs_conf['defconfig'], end='') # bool
    print('\t\tSet .config to largest generic options')
    print('  --oldconfig               ', end='')
    print(initramfs_conf['oldconfig'], end='') # bool
    print('\t\tAsk for new busybox options if any')
    print('  --menuconfig              ', end='')
    print(initramfs_conf['menuconfig'], end='') # bool
    print('\t\tInteractive busybox options menu')
    print()

    print('Features:')
    print('+ from host binaries')
    print('| --bin-luks                ', end='')
    print(initramfs_conf['bin-luks'], end='') # bool 
    print('\t\tInclude LUKS support from host')
    print('| --bin-lvm2                ', end='')
    print(initramfs_conf['bin-lvm2'], end='') # bool
    print('\t\tInclude LVM2 support from host')
    print('| --bin-screen              ', end='')
    print(initramfs_conf['bin-screen'], end='') # bool
    print('\t\tInclude the screen binary tool from host')
    print('| --bin-disklabel           ', end='')
    print(initramfs_conf['bin-disklabel'], end='') # bool
    print('\t\tInclude support for UUID/LABEL from host')
    print('| --bin-strace              ', end='')
    print(initramfs_conf['bin-strace'], end='') # bool
    print('\t\tInclude the strace binary tool from host')
    print('| --bin-evms                ', end='')
    print(initramfs_conf['bin-evms'], end='') # bool
    print('\t\tInclude the evms binary tool from host')
    print('| --bin-glibc               ', end='')
    print(initramfs_conf['bin-glibc'], end='') # bool
    print('\t\tInclude host GNU C libraries (required for dns,dropbear)')
    
    print('+ from source code')
    print('| --source-luks             ', end='')
    print(initramfs_conf['source-luks'], end='') # bool 
    print('\t\tInclude LUKS support from sources')
    print('| --source-lvm2             ', end='')
    print(initramfs_conf['source-lvm2'], end='') # bool
    print('\t\tInclude LVM2 support from sources')
    print('| --source-screen           ', end='')
    print(initramfs_conf['source-screen'], end='') # bool
    print('\t\tInclude the screen binary tool from sources')
    print('| --source-disklabel        ', end='')
    print(initramfs_conf['source-disklabel'], end='') # bool
    print('\t\tInclude support for UUID/LABEL from sources')
    print('| --source-ttyecho          ', end='')
    print(initramfs_conf['ttyecho'], end='') # bool
    print('\t\tCompile and include the handy ttyecho.c tool')
    print('| --source-strace           ', end='')
    print(initramfs_conf['source-strace'], end='') # bool
    print('\t\tCompile and include the strace binary tool from sources')
    print()

    # fix \t display depending on length of cli[splash']
    if cli['splash'] != '':
        if len(cli['splash']) <= 4:
            tab = '\t\t\t'
        elif len(cli['splash']) > 4 and len(cli['splash']) < 8:
            tab = '\t\t'
        elif len(cli['splash']) > 8:
            tab = '\t\t'
    else:
        tab = '\t\t\t'
    print('  --splash=<theme>          "'+initramfs_conf['splash']+'"', end='')
    print(tab+'Include splash support (splashutils must be merged)')
    print('   --sres=YxZ[,YxZ]         "'+initramfs_conf['sres']+'"', end='')
    print('\t\t\t Splash resolution, all if not set')
#    print('  --disklabel               ', end='')
#    print(initramfs_conf['disklabel'], end='') # bool
#    print('\t\tInclude support for UUID/LABEL (host binary or sources)')
#    print('  --luks                    ', end='')
#    print(initramfs_conf['luks'], end='') # bool 
#    print('\t\tInclude LUKS support (host binary or sources)')
#    print(stdout.yellow('  --evms                    '), end='')
#    print(initramfs_conf['evms'], end='') # bool
#    print('\t\tInclude EVMS support (host binary only)')
    print(stdout.yellow('  --dmraid                  '), end='')
    print(initramfs_conf['dmraid'], end='') # bool
    print('\t\tInclude DMRAID support (host binary or sources)')
#    print stdout.yellow('   --selinux                '),
#    print initramfs_conf['selinux'], # bool
#    print stdout.yellow('\t\t Include selinux support in --dmraid (selinux libs required)')
#   print '  --iscsi                    False                   Include iscsi support'
#   print '  --mdadm                    False                   Include mdadm support (mdadm must be merged)'
    print('  --dropbear                ', end='')
    print(initramfs_conf['dropbear'], end='') # bool
    print('\t\tInclude dropbear tools and daemon (host binary or sources)')
    print('   --debugflag              ', end='')
    print(initramfs_conf['debugflag'], end='') # bool
    print('\t\t Compile dropbear with #define DEBUG_TRACE in debug.h')
    # fix \t display depending on length of cli['rootpasswd']
    if cli['rootpasswd'] != '':
        if len(cli['rootpasswd']) <= 4:
            tab = '\t\t'
        elif len(cli['rootpasswd']) > 4:
            tab = '\t\t'
    else:
        tab = '\t\t'
    print('  --rootpasswd=<passwd>     "'+cli['rootpasswd']+'"', end='')
    print(tab+'Create and set root password (required for dropbear)')
#   print '  --unionfs-fuse             False                   Include unionfs-fuse support'
#   print '  --aufs                     False                   Include aufs support'
#   print '  --firmware=/dir            ""                      Include custom firmware support'
    # fix \t display depending on length of cli[splash']
    if cli['keymaps'] != '':
        if len(cli['keymaps']) <= 4:
            tab = '\t\t'
        elif len(cli['keymaps']) > 4 and len(cli['keymaps']) < 8:
            tab = '\t'
        elif len(cli['keymaps']) > 8:
            tab = '\t'
    else:
        tab = '\t\t'
#    print('  --keymaps                 ', end='')
    print('  --keymaps=xx[,xx]|all     ', end='')
    print(initramfs_conf['keymaps'], end='') # bool
    print(tab+'Include all keymaps')
#    print('  --ttyecho                 ', end='')
#    print(initramfs_conf['ttyecho'], end='') # bool
#    print('\t\tInclude the handy ttyecho.c tool')
#    print('  --strace                  ', end='')
#    print(initramfs_conf['strace'], end='') # bool
#    print('\t\tInclude the strace binary tool (host binary or sources)')
#    print('  --screen                  ', end='')
#    print(initramfs_conf['screen'], end='') # bool
#    print('\t\tInclude the screen binary tool (host binary or sources)')
    # fix \t display depending on length of cli['plugin']
    if cli['plugin'] != '': 
        if len(cli['plugin']) <= 4:
            tab = '\t\t\t'
        elif len(cli['plugin']) > 4:
            tab = '\t\t'
    else: 
        tab = '\t\t\t'
    print('  --plugin=/dir[,/dir]      "'+cli['plugin']+'"', end='')
    print(tab+'Include list of user generated custom roots')
    print()

    print('Libraries: (host only)')
#    print('  --glibc                   ', end='')
#    print(initramfs_conf['glibc'], end='') # bool
#    print('\t\tInclude host GNU C libraries (required for dns,dropbear)')
    print('  --libncurses              ', end='')
    print(initramfs_conf['libncurses'], end='') # bool
    print('\t\tInclude host libncurses (required for dropbear)')
    print('  --zlib                    ', end='')
    print(initramfs_conf['zlib'], end='') # bool
    print('\t\tInclude host zlib (required for dropbear)')
    print()

    print('Misc:')
    print('  --nocache                 ', end='')
    print(initramfs_conf['nocache'], end='')
    print('\t\tDelete previous cached data on startup')
    print(stdout.yellow('  --hostbin                 '), end='')
    print(initramfs_conf['hostbin'], end='')
    print('\t\tUse host binaries (fall back to sources if dynamic linkage detected)')
    print('  --nomodules               ', end='')
    print(initramfs_conf['nomodules'], end='')
    print('\t\tDo not install kernel modules (all is kernel builtin)')
    print('  --noboot                  ', end='')
    print(initramfs_conf['noboot'], end='')
    print('\t\tDo not copy initramfs to /boot')
    print('  --rename=/file            "'+initramfs_conf['rename']+'"', end='')
    print('\t\t\tCustom initramfs file name')
    print('  --logfile=/file           "'+master_conf['logfile']+'"', end='')
    print() #'\t\tLog to file'
    print('  --debug, -d               '+master_conf['debug']+'', end='')
    print('\t\tDebug verbose')
    print()

    print('Handy tools:')
    print('  --extract=/file           "'+cli['extract']+'"                  Extract initramfs file')
    print('   --to=/dir                "'+cli['to']+'"')
    print('\t\t\t\t\t\t Custom extracting directory')
    print('  --compress=/dir           "'+cli['compress']+'"                  Compress directory into initramfs')
    print('   --into=/file             "'+cli['into']+'"')
    print('\t\t\t\t\t\t Custom initramfs file')
