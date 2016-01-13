import os
import sys
from stdout import green, turquoise, white, red, yellow
from utils.process import *
from utils.misc import *
from utils.listdynamiclibs import *
from utils.isstatic import *

class screen:

    def __init__(self, cli, temp, verbose):

        self.cli = cli
        self.temp = temp
        self.verbose = verbose

    def build(self):
        """
        Append screen binary from host to the initramfs

        @return: bool
        """
        logging.debug('>>> entering initramfs.append.bin_screen')
        screen_bin = '/usr/bin/screen'

        process('mkdir -p %s' % self.temp['work']+'/initramfs-bin-screen-temp/bin', self.verbose)

         # use from host
        logging.debug('initramfs.append.bin_screen from %s' % white('host'))
        process('cp %s %s/initramfs-bin-screen-temp/bin' % (screen_bin, self.temp['work']), self.verbose)
        process('chmod +rx %s/initramfs-bin-screen-temp/bin/screen' % self.temp['work'], self.verbose)

        if not isstatic(screen_bin, self.verbose) and self.cli['dynlibs'] is True:
            screen_libs = listdynamiclibs(screen_bin, self.verbose)
            process('mkdir -p %s' % self.temp['work']+'/initramfs-bin-screen-temp/lib', self.verbose)
            print(yellow(' * ') + '... ' + yellow('warning')+': '+screen_bin+' is dynamically linked, copying detected libraries')
            for i in screen_libs:
                print(green(' * ') + '... ' + i)
                process('cp %s %s' % (i, self.temp['work']+'/initramfs-bin-screen-temp/lib'), self.verbose)

        # add required /usr/share/terminfo/l/linux for screen
        # FIXME: to support other arch copy accordingly
        os.makedirs(self.temp['work']+'/initramfs-bin-screen-temp/usr/share/terminfo/l')
        process('cp /usr/share/terminfo/l/linux %s' % self.temp['work']+'/initramfs-bin-screen-temp/usr/share/terminfo/l', self.verbose)

        os.chdir(self.temp['work']+'/initramfs-bin-screen-temp')
        return os.system('find . -print | cpio --quiet -o -H newc --append -F %s/initramfs-cpio' % self.temp['cache'])
