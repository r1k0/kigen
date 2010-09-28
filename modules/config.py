import sys
import os
from default import *
from utils.misc import *

from stdout import white, green, turquoise, yellow, red

def etc_parser():

    etc = { 'kigen':        '/etc/kigen',               \
            'master_conf':  '/etc/kigen/master.conf',   \
            'modules_conf': '/etc/kigen/modules.conf',  \
            'default_conf': '/etc/kigen/default.conf'}

    if not os.path.isdir(etc['kigen']):
        print 'error: missing directory ' + red(etc['kigen'])
        sys.exit(2)
    
    if not os.path.isfile(etc['master_conf']):
        print 'error: missing file ' + red(etc['master_conf'])
        sys.exit(2)

    if not os.path.isfile(etc['modules_conf']):
        print 'error: missing file ' + red(etc['modules_conf'])
        sys.exit(2)

    if not os.path.isfile(etc['default_conf']):
        print 'error: missing file ' + red(etc['default_conf'])
        sys.exit(2)

    master_conf_temp = parse_config_file(etc['master_conf'])
    master_conf.update(master_conf_temp)

    modules_conf_temp = parse_config_file(etc['modules_conf'])
    modules_conf.update(modules_conf_temp)

    default_conf_temp = parse_config_file(etc['default_conf'])
    default_conf.update(default_conf_temp)

    return master_conf, modules_conf, default_conf
