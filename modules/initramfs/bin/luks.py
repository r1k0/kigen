import os
import sys
from stdout import green, turquoise, white, red, yellow
from utils.process import *
from utils.misc import *
from utils.listdynamiclibs import *
from utils.isstatic import *

class luks:

    def __init__(self, temp, verbose):
        self.temp = temp
        self.verbose = verbose

    def build(self):
        """
        Append the LUKS static binary to the initramfs
    
        @return: bool
        """
        logging.debug('>>> entering initramfs.append.bin_luks')
#        cryptsetup_bin  = '/bin/cryptsetup'
        cryptsetup_sbin = '/sbin/cryptsetup'

        process('mkdir -p %s' % self.temp['work']+'/initramfs-bin-luks-temp/lib/luks', self.verbose)
        process('mkdir -p %s' % self.temp['work']+'/initramfs-bin-luks-temp/sbin', self.verbose)

#        if os.path.isfile(cryptsetup_bin) and isstatic(cryptsetup_bin, self.verbose):
#            # use from host
#            logging.debug('initramfs.append.bin_luks from %s' % white('host'))
#            print(green(' * ') + turquoise('initramfs.append.bin_luks ')+ cryptsetup_bin +' from ' + white('host'))
#            process('cp %s %s/initramfs-bin-luks-temp/sbin' % (cryptsetup_bin, self.temp['work']), self.verbose)
#            process('chmod +x %s/initramfs-bin-luks-temp/sbin/cryptsetup' % self.temp['work'], self.verbose)
#
##            if not isstatic(cryptsetup_bin, self.verbose):
##                luks_libs = listdynamiclibs(cryptsetup_bin, self.verbose)
##
##                process('mkdir -p %s' % self.temp['work']+'/initramfs-luks-temp/lib', self.verbose)
##                print green(' * ') + '... ' + yellow('warning')+': '+cryptsetup_bin+' is dynamically linked, copying detected libraries'
##                for i in luks_libs:
##                    print green(' * ') + '... ' + i
##                    process('cp %s %s' % (i, self.temp['work']+'/initramfs-luks-temp/lib'), self.verbose)
##            else:
##                logging.debug(cryptsetup_bin+' is statically linked nothing to do')
#
##        elif os.path.isfile(cryptsetup_sbin) and self.hostbin is True and isstatic(cryptsetup_sbin, self.verbose):
#        elif os.path.isfile(cryptsetup_sbin) and isstatic(cryptsetup_sbin, self.verbose):
            # use from host
        logging.debug('initramfs.append.bin_luks from %s' % white('host'))
        process('cp %s %s/initramfs-bin-luks-temp/sbin' % (cryptsetup_sbin, self.temp['work']), self.verbose)
        process('chmod +x %s/initramfs-bin-luks-temp/sbin/cryptsetup' % self.temp['work'], self.verbose)

        if not isstatic(cryptsetup_sbin, self.verbose):
            luks_libs = listdynamiclibs(cryptsetup_sbin, self.verbose)
            process('mkdir -p %s' % self.temp['work']+'/initramfs-bin-luks-temp/lib', self.verbose)
            print(yellow(' * ') + '... ' + yellow('warning')+': '+cryptsetup_sbin+' is dynamically linked, copying detected libraries')
            for i in luks_libs:
                print(green(' * ') + '... ' + i)
                process('cp %s %s' % (i, self.temp['work']+'/initramfs-bin-luks-temp/lib'), self.verbose)
        else:
            logging.debug(cryptsetup_sbin+' is statically linked nothing to do')

        os.chdir(self.temp['work']+'/initramfs-bin-luks-temp')
        return os.system('find . -print | cpio --quiet -o -H newc --append -F %s/initramfs-cpio' % self.temp['cache'])
