import os
import sys
from stdout import green, turquoise, white, red, yellow
from utils.process import *
from utils.misc import *

class dmraid:

    def __init__(self, master_config, version_conf, selinux, temp, verbose):

        self.master_config  = master_config
        self.temp           = temp
        self.verbose        = verbose
        self.dmraid_ver     = version_conf['dmraid-version']
        self.dmraidtmp      = temp['work'] + '/dmraid/' + self.dmraid_ver
        self.selinux        = selinux
        
    def build(self):
        """
        dmraid build sequence

        @return     bool
        """
        zero = int('0')
    
        if os.path.isfile('%s/distfiles/dmraid-%s.tar.bz2' % (get_portdir(self.temp), self.dmraid_ver)) is not True:
            if self.download() is not zero:
                process('rm %s/distfiles/dmraid-%s.tar.bz2' % (get_portdir(self.temp), self.dmraid_ver), self.verbose)
                self.fail('download')
    
        self.extract()
        # grr, tar thing to not return 0 when success
    
        if self.configure() is not zero: self.fail('configure')
    
        if self.unset_selinux() is not zero: self.fail('selinux')

        if self.make() is not zero: self.fail('make')
    
        if self.strip() is not zero: self.fail('strip')
    
        if self.compress() is not zero: self.fail('compress')
    
        if self.cache() is not zero: self.fail('cache')
   
    def set_config(self):
        self.chgdir(self.dmraidtmp)
        print green(' * ') + '... dmraid.set_selinux'
        return os.system('echo "DMRAIDLIBS += -lselinux -lsepol" >> tools/Makefile')

    def unset_selinux(self):
        self.chgdir(self.dmraidtmp)
        print green(' * ') + '... dmraid.unset_selinux'
        return os.system('sed -i tools/Makefile -e "s|DMRAIDLIBS += -lselinux||g"')

    def fail(self, step):
        """
        @arg step   string

        @return     exit
        """
        print red('error')+': initramfs.dmraid.'+step+'() failed'
        sys.exit(2)

    def chgdir(self, dir):
        """
        Change to directory
    
        @arg: string
        @return: none
        """
        if not os.path.isdir(dir):
            print red('error') + ': ' + 'cannot change dir to ' + dir
            sys.exit(2)
        if not os.getcwd() == dir:
            os.chdir(dir)

    def download(self):
        """
        dmraid tarball download routine
    
        @return: bool
        """
        print green(' * ') + '... dmraid.download'
        dmraid_url = 'http://people.redhat.com/~heinzm/sw/dmraid/src/dmraid-' + str(self.dmraid_ver) + '.tar.bz2'

        # FIXME utils.shell.process does not remove the output
        return os.system('/usr/bin/wget %s -O %s/distfiles/dmraid-%s.tar.bz2 %s' % (dmraid_url, get_portdir(self.temp), str(self.dmraid_ver), self.verbose['std']))
    
    def extract(self):
        """
        dmraid tarball extraction routine
    
        @return: bool
        """
        print green(' * ') + '... dmraid.extract'
    
        os.system('tar xvfj %s/distfiles/dmraid-%s.tar.bz2 -C %s %s' % (get_portdir(self.temp), str(self.dmraid_ver), self.temp['work'], self.verbose['std']))
    
    def configure(self):
        """
        dmraid Makefile interface to configure
    
        @return: bool
        """
        print green(' * ') + '... dmraid.configure'
        self.chgdir(self.dmraidtmp)
    
#        return os.system('LDFLAGS=-static ./configure %s' % self.verbose['std'])
        return os.system('LDFLAGS=-L%s/device-mapper/lib \
                CFLAGS=-I%s/device-mapper/include \
                CPPFLAGS=-I%s/device-mapper/include \
                ./configure --enable-static_link --prefix=%s/dmraid %s' % (self.temp['work'], self.temp['work'], self.temp['work'], self.temp['work'], self.verbose['std']))

    
    def make(self):
        """
        dmraid Makefile interface to make
    
        @return: bool
        """
        print green(' * ') + '... dmraid.make'
        self.chgdir(self.dmraidtmp)
    
        return os.system('%s %s %s' % (self.master_config['DEFAULT_UTILS_MAKE'], self.master_config['DEFAULT_MAKEOPTS'], self.verbose['std']))
    
    def strip(self):
        """
        dmraid strip binary routine
    
        @arg dmraidtmp          string
        @arg master_config  dict
    
        @return: bool
        """
        print green(' * ') + '... dmraid.strip'
        self.chgdir(self.dmraidtmp)
    
#        return os.system('strip %s/dmraid ' % self.dmraidtmp)
        return os.system('strip %s/dmraid/%s/tools/dmraid.static' % (self.temp['work'], self.dmraid_ver))

    
    def compress(self):
        """
        dmraid compression routine
    
        @arg dmraidtmp          string
        @arg master_config  dict
    
        @return: bool
        """
        print green(' * ') + '... dmraid.compress'
        self.chgdir(self.dmraidtmp)
    
#        return os.system('bzip2 %s/dmraid' % self.dmraidtmp)
        return os.system('bzip2 %s/dmraid/%s/tools/dmraid.static' % (self.temp['work'], self.dmraid_ver))
    
    def cache(self):
        """
        dmraid tarball cache routine
    
        @return: bool
        """
        print green(' * ') + '... dmraid.cache'
        self.chgdir(self.dmraidtmp)
    
#        return process('mv %s/dmraid.bz2 %s/dmraid-%s.bz2' % (self.dmraidtmp, self.temp['cache'], self.dmraid_ver), self.verbose)
        return process('mv %s/tools/dmraid.static.bz2 %s/dmraid.static-%s.bz2' % (self.dmraidtmp, self.temp['cache'], self.dmraid_ver), self.verbose)

