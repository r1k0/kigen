import os
import sys
from stdout import green, turquoise, white, red, yellow
from utils.process import *
from utils.misc import *

class luks:

    def __init__(self, master_config, version_conf, url_conf, temp, verbose):

        self.master_config  = master_config
        self.temp           = temp
        self.verbose        = verbose
        self.url            = url_conf['luks']
        self.luks_ver       = version_conf['luks-version']
        self.lukstmp        = temp['work'] + '/cryptsetup-' + self.luks_ver

    def build(self):
        """
        luks build sequence
    
        @return: bool
        """
        zero = int('0')

        # make sure dev-libs/libgcrypt has static-libs use flag enabled
        if not pkg_has_useflag('dev-libs', 'libgcrypt', 'static-libs'):
            print(red('error')+': utils.pkg_has_useflag("dev-libs", "libgcrypt", "static-libs") failed, remerge libgcrypt with +static-libs')
            sys.exit(2)

        if os.path.isfile('%s/cryptsetup-%s.tar.bz2' % (get_distdir(self.temp), self.luks_ver)) is not True:
            if self.download() is not zero: 
                process('rm -v %s/cryptsetup-%s.tar.bz2' % (get_distdir(self.temp), self.luks_ver), self.verbose)
                self.fail('download')
    
        self.extract()
        # grr, tar thing to not return 0 when success
    
        if self.configure()is not zero: self.fail('configure')
    
        if self.make() is not zero: self.fail('make')
    
        if self.strip() is not zero: self.fail('strip')
    
        if self.compress() is not zero: self.fail('compress')
    
        if self.cache() is not zero: self.fail('cache')
    
    def fail(self, step):
        """
        Exit

        @arg step   string
        @return     exit
        """
        print(red('error')+': initramfs.luks.'+step+'() failed')
        sys.exit(2)

    def chgdir(self, dir):
        """
        Change to directory
    
        @arg: string
        @return: none
        """
        if not os.path.isdir(dir):
            print(red('error') + ': ' + 'cannot change dir to ' + dir)
            sys.exit(2)
        if not os.getcwd() == dir:
            os.chdir(dir)

    def download(self):
        """
        luks tarball download routine
    
        @return: bool
        """
        print(green(' * ') + '... luks.download')
        luks_url = self.url +'/cryptsetup-'+ self.luks_ver + '.tar.bz2'

        # FIXME wget sucks at print to stdout so no utils.shell.process here
        return os.system('/usr/bin/wget %s -v -O %s/cryptsetup-%s.tar.bz2 %s' % (luks_url, get_distdir(self.temp), str(self.luks_ver), self.verbose['std']))
    
    def extract(self):
        """
        luks tarball extraction routine
    
        @return: bool
        """
        print(green(' * ') + '... luks.extract')
    
        os.system('tar xvfj %s/cryptsetup-%s.tar.bz2 -C %s %s' % (get_distdir(self.temp), str(self.luks_ver), self.temp['work'], self.verbose['std']))
    
    def configure(self):
        """
        luks Makefile interface to configure
    
        @return: bool
        """
        print(green(' * ') + '... luks.configure')
        self.chgdir(self.lukstmp)
    
        return os.system('./configure --disable-selinux --enable-static %s' % self.verbose['std'])
    
    def make(self):
        """
        luks Makefile interface to make
    
        @return: bool
        """
        print(green(' * ') + '... luks.make')
        self.chgdir(self.lukstmp)
    
        return os.system('%s %s %s' % (self.master_config['DEFAULT_UTILS_MAKE'], self.master_config['DEFAULT_MAKEOPTS'], self.verbose['std']))
    
    def strip(self):
        """
        blkid strip binary routine
    
        @return: bool
        """
        print(green(' * ') + '... luks.strip')
        self.chgdir(self.lukstmp)
    
        return process('strip %s/src/cryptsetup' % self.lukstmp, self.verbose)
    
    def compress(self):
        """
        blkid compression routine
    
        @return: bool
        """
        print(green(' * ') + '... luks.compress')
        self.chgdir(self.lukstmp)
    
        return process('bzip2 %s/src/cryptsetup' % self.lukstmp, self.verbose)
    
    def cache(self):
        """
        blkid tarball cache routine
    
        @return: bool
        """
        print(green(' * ') + '... luks.cache')
        self.chgdir(self.lukstmp)
    
        return process('mv %s/src/cryptsetup.bz2 %s/cryptsetup-%s.bz2' % (self.lukstmp, self.temp['cache'], self.luks_ver), self.verbose)

