import sys
import os

def etc_parser():

# check /etc/kigen isdir
# check /etc/kigen/master.conf E
# check /etc/kigen/modules.conf E
# check /etc/kigen/default.conf E
# parse /etc/kigen/master.conf
# parse /etc/kigen/modules.conf
# parse /etc/kigen/default.conf
#

    etc = { 'kigen':        '/etc/kigen',  \
            'master_conf'   '/etc/kigen/master.conf', \
            'modules_conf'  '/etc/kigen/modules.conf', \
            'default_conf'  '/etc/kigen/default.conf'}

    # parse kigen config file
    kigen_conf = etc['config']
    if os.path.isfile(kigen_conf):
        master_config_temp = parse_config_file(kigen_conf)
        master_config.update(master_config_temp)
    else:
        print 'error: missing ' + red(kigen_conf)
        sys.exit(2)


    return etc
