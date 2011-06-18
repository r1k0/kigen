import os
import sys
from stdout import green, turquoise, white, red, yellow

# FIXME yuk!

try:
    import funtoo.boot.config
    import funtoo.core.config
except:
    pass

def get_boot_initrd():
    """
    Return dictionary of initrd /etc/boot.conf entry

    @arg        none

    @return     dict
    """
    d = {}

    if os.path.isfile('/sbin/boot-update'):
        if funtoo.boot.config.BootConfigFile('/etc/boot.conf').fileExists():
            bootconf = funtoo.core.config.ConfigFile('/etc/boot.conf')
            try:
                d = bootconf.sectionData['initrd']
                return d
            except:
                d = {}
                return d
        else:
            return d
    else:
        return d
