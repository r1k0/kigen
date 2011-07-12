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
    print('  tool, t                    Handy tools')
    print()
    print(stdout.turquoise('Parameters')+':')
    print(' '+os.path.basename(sys.argv[0])+' kernel'+'                --help, -h')
    print(' '+os.path.basename(sys.argv[0])+' initramfs'+'             --help, -h')
    print(' '+os.path.basename(sys.argv[0])+' tool'+'                  --help, -h')

def print_examples():
    print()
    print(stdout.white('Examples')+':')
    print(' '+os.path.basename(sys.argv[0])+' kernel --fixdotconfig=splash')
    print(' '+os.path.basename(sys.argv[0])+' --clean --menuconfig k')
    print(' '+os.path.basename(sys.argv[0])+' k --initramfs=/myinitramfsfile')
    print(' '+os.path.basename(sys.argv[0])+' i --splash=sabayon')
    print(' '+os.path.basename(sys.argv[0])+' --source-disklabel --source-lvm2 --splash=sabayon --bin-luks -d -n initramfs')
    print(' '+os.path.basename(sys.argv[0])+' i --bin-luks --bin-lvm2 --bin-disklabel --splash=sabayon --bin-glibc --dynlibs')
    print(' '+os.path.basename(sys.argv[0])+' i --splash=emergence --source-disklabel --source-luks --source-lvm2 --source-dropbear --debugflag --rootpasswd=mypasswd --keymaps=all --source-ttyecho --source-strace --source-screen --bin-glibc --bin-zlib --bin-libncurses --defconfig --nocache')
    print(' '+os.path.basename(sys.argv[0])+' --extract=/file t --to=/dir')
    print(' '+os.path.basename(sys.argv[0])+' tool --compress=/dir --into=/file')


def print_usage_kernel(cli, master_conf, kernel_conf):
    print('Parameter:\t\t    Config value:\tDescription:')
    print()
    print('Kernel:')
    print('  --dotconfig=/file         "'+kernel_conf['dotconfig']+'"', end='')
    print('\t\t\tCustom kernel .config file')

    print('  --initramfs=/file         "'+kernel_conf['initramfs']+'"', end='')
    print('\t\t\tEmbed initramfs into the kernel')

    if kernel_conf['fixdotconfig'] != '':
        if len(kernel_conf['fixdotconfig']) <= 4:
            tab = '\t\t\t'
        elif len(kernel_conf['fixdotconfig']) > 4 and len(kernel_conf['fixdotconfig']) < 7:
            tab = '\t\t\t'
        elif len(kernel_conf['fixdotconfig']) > 7 and len(kernel_conf['fixdotconfig']) < 12:
            tab = '\t\t'
        elif len(kernel_conf['fixdotconfig']) > 12:
            tab = ''
    else:
        tab = '\t\t\t'
    print(stdout.yellow('  --fixdotconfig=<feature>  '), end='"')
    print(kernel_conf['fixdotconfig'], end='"')
    print(tab+'Check and auto fix the kernel config file (experimental)')
    print('\t\t\t\t\t\t splash,initramfs,selinux,pax supported (writes to .config)')
    print('  --clean                   ', end='')
    print(kernel_conf['clean'], end='')
    print('\t\tClean precompiled objects only')
    print('  --mrproper                ', end='')
    print(kernel_conf['mrproper'], end='')
    print('\t\tClean precompiled objects and remove config file')
    print('  --localmodconfig          ', end='')
    print(kernel_conf['localmodconfig'], end='')
    print('\t\tUpdate current config disabling modules not loaded')
    print('  --localyesconfig          ', end='')
    print(kernel_conf['localyesconfig'], end='')
    print('\t\tUpdate current config converting local mods to core')
    print('  --silentoldconfig         ', end='')
    print(kernel_conf['silentoldconfig'], end='')
    print('\t\tSame as oldconfig, but quietly, additionally update deps')
    print('  --defconfig               ', end='')
    print(kernel_conf['defconfig'], end='')
    print('\t\tNew config with default from ARCH supplied defconfig')
    print('  --menuconfig              ', end='')
    print(kernel_conf['menuconfig'], end='')
    print('\t\tInteractive kernel options menu')
    print('  --fakeroot=/dir           "'+cli['fakeroot']+'"\t\t\tAppend modules to /dir/lib/modules')
    print('  --module-rebuild          ', end='')
    print(kernel_conf['module-rebuild'], end='')
    print('\t\tCall sys-kernel/module-rebuild last')
    print('  --nooldconfig             ', end='')
    print(kernel_conf['nooldconfig'], end='')
    print('\t\tDo not ask for new kernel/initramfs options')
    print('  --nomodinstall            ', end='')
    print(kernel_conf['nomodinstall'], end='')
    print('\t\tDo not install modules')
    print('  --nomodules               ', end='')
    print(kernel_conf['nomodules'], end='')
    print('\t\tDo not compile or install modules')
    print()
    print('Misc:')
    print('  --nosaveconfig            ', end='')
    print(kernel_conf['nosaveconfig'], end='')
    print('\t\tDo not save kernel config in /etc/kernels')
    print('  --noboot                  ', end='')
    print(kernel_conf['noboot'], end='')
    print('\t\tDo not copy kernel to /boot')
    print('  --rename=/file            "'+kernel_conf['rename']+'"', end='')
    print('\t\t\tCustom kernel file name')
    print('  --logfile=/file           "'+master_conf['logfile']+'"', end='')
    print() #'\t\tLog to file'
    print('  --debug, -d               '+master_conf['debug']+'\t\tDebug verbose')

def print_usage_initramfs(cli, master_conf, initramfs_conf, modules_conf):
    print('Parameter:\t\t    Config value:\tDescription:')
    print()
    print('Features:')
    print('+ from source code')
    print('| --source-luks             ', end='')
    print(initramfs_conf['source-luks'], end='') # bool 
    print('\t\tInclude LUKS support from sources')
    print('| --source-lvm2             ', end='')
    print(initramfs_conf['source-lvm2'], end='') # bool
    print('\t\tInclude LVM2 support from sources')
    print('| --source-dropbear         ', end='')
    print(initramfs_conf['source-dropbear'], end='') # bool
    print('\t\tInclude dropbear support from sources')
    print('|  --debugflag              ', end='')
    print(initramfs_conf['debugflag'], end='') # bool
    print('\t\t Compile dropbear with #define DEBUG_TRACE in debug.h')
    print('| --source-screen           ', end='')
    print(initramfs_conf['source-screen'], end='') # bool
    print('\t\tInclude the screen binary tool from sources')
    print('| --source-disklabel        ', end='')
    print(initramfs_conf['source-disklabel'], end='') # bool
    print('\t\tInclude support for UUID/LABEL from sources')
    print('| --source-ttyecho          ', end='')
    print(initramfs_conf['source-ttyecho'], end='') # bool
    print('\t\tCompile and include the handy ttyecho.c tool')
    print('| --source-strace           ', end='')
    print(initramfs_conf['source-strace'], end='') # bool
    print('\t\tCompile and include the strace binary tool from sources')
    print('| --source-dmraid           ', end='')
    print(initramfs_conf['source-dmraid'], end='') # bool
    print('\t\tInclude DMRAID support from sources')
#    print('| --source-all              ', end='')
#    print(initramfs_conf['source-all'], end='') # bool
#    print('\t\tInclude all possible features from sources')

    print('+ from host binaries')
    print('| --bin-busybox             ', end='')
    print(initramfs_conf['bin-busybox'], end='') # bool 
    print('\t\tInclude busybox support from host')
    print('| --bin-luks                ', end='')
    print(initramfs_conf['bin-luks'], end='') # bool 
    print('\t\tInclude LUKS support from host')
    print('| --bin-lvm2                ', end='')
    print(initramfs_conf['bin-lvm2'], end='') # bool
    print('\t\tInclude LVM2 support from host')
    print('| --bin-dropbear            ', end='')
    print(initramfs_conf['bin-dropbear'], end='') # bool
    print('\t\tInclude dropbear support from host')
    print('| --bin-screen              ', end='')
    print(initramfs_conf['bin-screen'], end='') # bool
    print('\t\tInclude the screen binary tool from host')
    print('| --bin-disklabel           ', end='')
    print(initramfs_conf['bin-disklabel'], end='') # bool
    print('\t\tInclude support for UUID/LABEL from host')
    print('| --bin-strace              ', end='')
    print(initramfs_conf['bin-strace'], end='') # bool
    print('\t\tInclude the strace binary tool from host')
#    print('| --bin-evms                ', end='')
#    print(initramfs_conf['bin-evms'], end='') # bool
#    print('\t\tInclude the evms binary tool from host')
    print('| --bin-glibc               ', end='')
    print(initramfs_conf['bin-glibc'], end='') # bool
    print('\t\tInclude host GNU C libraries (required for dns,dropbear)')
    print('| --bin-libncurses          ', end='')
    print(initramfs_conf['bin-libncurses'], end='') # bool
    print('\t\tInclude host libncurses (required for dropbear)')
    print('| --bin-zlib                ', end='')
    print(initramfs_conf['bin-zlib'], end='') # bool
    print('\t\tInclude host zlib (required for dropbear)')
    print('| --bin-dmraid              ', end='')
    print(initramfs_conf['bin-dmraid'], end='') # bool
    print('\t\tInclude DMRAID support from host')
#    print('| --bin-all                 ', end='')
#    print(initramfs_conf['bin-all'], end='') # bool
#    print('\t\tInclude all possible features from host')
    print()

    print(stdout.yellow('  --dynlibs                 '), end='')
    print(initramfs_conf['dynlibs'], end='') # bool
    print('\t\tInclude detected libraries from dynamically linked binaries')

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
    print('  --splash=<theme>          "'+initramfs_conf['splash'], end='"')
    print(tab+'Include splash support (splashutils must be merged)')
    print('   --sres=YxZ[,YxZ]         "'+initramfs_conf['sres'], end='"')
    print('\t\t\t Splash resolution, all if not set')

    # fix \t display depending on length of cli['rootpasswd']
    if cli['rootpasswd'] != '':
        if len(cli['rootpasswd']) <= 4:
            tab = '\t\t'
        elif len(cli['rootpasswd']) > 4:
            tab = '\t\t'
    else:
        tab = '\t\t\t'
    print('  --rootpasswd=<passwd>     "'+cli['rootpasswd'], end='"')
    print(tab+'Create and set root password (required for dropbear)')
    if cli['keymaps'] != '':
        if len(cli['keymaps']) <= 4:
            tab = '\t\t\t'
        elif len(cli['keymaps']) > 4 and len(cli['keymaps']) < 8:
            tab = '\t\t'
        elif len(cli['keymaps']) > 8:
            tab = '\t'
    else:
        tab = '\t\t\t'
    print('  --keymaps=xx[,xx]|all     ', end='"')
    print(initramfs_conf['keymaps'], end='"') # bool
    print(tab+'Include all keymaps')
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

# NOFIX this works but force user to use --plugin= instead
#    print('Linuxrc:')
#    print('  --linuxrc=/linuxrc[,/file]"'+initramfs_conf['linuxrc']+'"', end='')
#    print('\t\t\tInclude custom linuxrc (files copied over to etc)')
#    print()

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

    print('Misc:')
    print('  --nocache                 ', end='')
    print(initramfs_conf['nocache'], end='')
    print('\t\tDelete previous cached data on startup')
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

def print_usage_tool(cli):
    print('Parameter:\t\t    Config value:\tDescription:')
    print()
    print('Kernel:')
    print('  --getdotconfig=/vmlinux   "'+cli['getdotconfig']+'"\t\t\tExtract .config from compiled binary kernel (if IKCONFIG has been set)')
    print()
    print('Initramfs:')
    print('  --extract=/file           "'+cli['extract']+'"                  Extract initramfs file')
    print('   --to=/dir                "'+cli['to']+'"')
    print('\t\t\t\t\t\t Custom extracting directory')
    print('  --compress=/dir           "'+cli['compress']+'"                  Compress directory into initramfs')
    print('   --into=/file             "'+cli['into']+'"')
    print('\t\t\t\t\t\t Custom initramfs file')
    print()
    print('Misc:')
    print('  --rmcache                 ', end='')
    print(cli['rmcache'], end='')
    print('\t\tRemove cached data')

