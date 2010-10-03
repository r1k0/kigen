import sys
import os
from default import *
from utils.misc import *
from stdout import white, green, turquoise, yellow, red

# parse /etc/kigen/master.conf
def etc_parser_master():

    etc = { 'kigen':            '/etc/kigen',                           \
            'master_conf':      '/etc/kigen/master.conf'}

    if not os.path.isdir(etc['kigen']):
        print 'error: missing directory ' + red(etc['kigen'])
        sys.exit(2)
    
    if not os.path.isfile(etc['master_conf']):
        print 'error: missing file ' + red(etc['master_conf'])
        sys.exit(2)

    master_conf_temp = parse_config_file(etc['master_conf'])
    master_conf.update(master_conf_temp)

    return master_conf

# parse /etc/kigen/kernel/kernel.conf
def etc_parser_kernel():

    etc = { 'kigen':            '/etc/kigen',                           \
            'kernel_conf':      '/etc/kigen/kernel/default.conf'}

    if not os.path.isfile(etc['kernel_conf']):
        print 'error: missing file ' + red(etc['kernel_conf'])
        sys.exit(2)

    kernel_conf_temp = parse_config_file(etc['kernel_conf'])
    kernel_conf.update(kernel_conf_temp)

    return kernel_conf

# parse /etc/kigen/initramfs/modules.conf and
# /etc/kigen/initramfs/initramfs.conf
def etc_parser_initramfs():
    
    etc = { 'kigen':            '/etc/kigen',                           \
            'initramfs_conf':   '/etc/kigen/initramfs/default.conf',    \
            'modules_conf':     '/etc/kigen/initramfs/modules.conf'}

    if not os.path.isfile(etc['modules_conf']):
        print 'error: missing file ' + red(etc['modules_conf'])
        sys.exit(2)

    if not os.path.isfile(etc['initramfs_conf']):
        print 'error: missing file ' + red(etc['initramfs_conf'])
        sys.exit(2)

    modules_conf_temp = parse_config_file(etc['modules_conf'])
    modules_conf.update(modules_conf_temp)

    initramfs_conf_temp = parse_config_file(etc['initramfs_conf'])
    initramfs_conf.update(initramfs_conf_temp)

    return initramfs_conf, modules_conf
