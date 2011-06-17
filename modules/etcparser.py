import sys
import os
from default import *
import utils.misc
from stdout import *

# WARN don't import logging here as it's not already declared in kigen

# parse /etc/kigen/master.conf
def etc_parser_master():

    master_conf = {}

    etc = { 'kigen':            '/etc/kigen',                           \
            'master_conf':      '/etc/kigen/master.conf'}

    if not os.path.isdir(etc['kigen']):
        print('error: missing directory ' + red(etc['kigen']))
        sys.exit(2)
    
    if not os.path.isfile(etc['master_conf']):
        print('error: missing file ' + red(etc['master_conf']))
        sys.exit(2)

    master_conf_temp = utils.misc.parse_config_file(etc['master_conf'])
    master_conf.update(master_conf_temp)

    return master_conf

# parse /etc/kigen/kernel/kernel.conf
def etc_parser_kernel():

    kernel_conf = {}

    etc = { 'kigen':            '/etc/kigen',                           \
            'kernel_conf':      '/etc/kigen/kernel/default.conf'}

    if not os.path.isfile(etc['kernel_conf']):
        print('error: missing file ' + red(etc['kernel_conf']))
        sys.exit(2)

    kernel_conf_temp = utils.misc.parse_config_file(etc['kernel_conf'])
    kernel_conf.update(kernel_conf_temp)

    return kernel_conf

# parse /etc/kigen/initramfs/{modules.conf,initramfs.conf,version.conf}
def etc_parser_initramfs():

    # do not declare modules_conf initramfs_conf version_conf url_conf
    # we already import their defaults from default.py
#    modules_conf    = {}
#    initramfs_conf  = {}
#    version_conf    = {}
#    url_conf        = {}

    etc = { 'kigen'         :   '/etc/kigen',                           \
            'initramfs_conf':   '/etc/kigen/initramfs/default.conf',    \
            'modules_conf'  :   '/etc/kigen/initramfs/modules.conf',    \
            'version_conf'  :   '/etc/kigen/initramfs/version.conf',    \
            'url_conf'      :   '/etc/kigen/initramfs/url.conf'}

    if not os.path.isfile(etc['modules_conf']):
        print('error: missing file ' + red(etc['modules_conf']))
        sys.exit(2)

    if not os.path.isfile(etc['initramfs_conf']):
        print('error: missing file ' + red(etc['initramfs_conf']))
        sys.exit(2)

    if not os.path.isfile(etc['version_conf']):
        print('error: missing file ' + red(etc['version_conf']))
        sys.exit(2)

    modules_conf_temp = utils.misc.parse_config_file(etc['modules_conf'])
    modules_conf.update(modules_conf_temp)

    initramfs_conf_temp = utils.misc.parse_config_file(etc['initramfs_conf'])
    initramfs_conf.update(initramfs_conf_temp)

    version_conf_temp = utils.misc.parse_config_file(etc['version_conf'])
    version_conf.update(version_conf_temp)

    url_conf_temp = utils.misc.parse_config_file(etc['url_conf'])
    url_conf.update(url_conf_temp)

    return initramfs_conf, modules_conf, version_conf, url_conf
