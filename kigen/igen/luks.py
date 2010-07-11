import os
import sys
from stdout import green, turquoise, white, red, yellow
import utils

class luks:

    def __init__(self, master_config, temp, verbose):

        self.master_config  = master_config
        self.temp           = temp
        self.verbose        = verbose
        self.luks_ver       = master_config['luks-version']
        self.lukstmp        = temp['work'] + '/cryptsetup-' + master_config['luks-version']

    def build(self):
        """
        luks build sequence
    
        @return: bool
        """
        ret = zero = int('0')
    
        if os.path.isfile('%s/distfiles/cryptsetup-%s.tar.bz2' % (utils.get_portdir(self.temp), self.luks_ver)) is not True:
            ret = self.download()
            if ret is not zero: 
                os.system('rm %s/distfiles/cryptsetup-%s.tar.bz2' % (utils.get_portdir(self.temp), self.luks_ver))
                self.fail('download')
    
        self.extract()
    #   grr, tar thing to not return 0 when success
    
        ret = self.configure()
        if ret is not zero: self.fail('configure')
    
        ret = self.compile()
        if ret is not zero: self.fail('compile')
    
        ret = self.strip()
        if ret is not zero: self.fail('strip')
    
        ret = self.compress()
        if ret is not zero: self.fail('compress')
    
        ret = self.cache()
        if ret is not zero: self.fail('cache')
    
        return ret

    def fail(self, step):
        """
        Exit

        @arg step   string
        @return     exit
        """
        print red('error')+': initramfs.luks.'+step+'() failed'
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
        luks tarball download routine
    
        @return: bool
        """
        print green(' * ') + '... luks.download'
        luks_url = 'http://gentoo.osuosl.org/distfiles/cryptsetup-' + self.luks_ver + '.tar.bz2'

        return os.system('/usr/bin/wget %s -O %s/distfiles/cryptsetup-%s.tar.bz2 %s' % (luks_url, utils.get_portdir(self.temp), str(self.luks_ver), self.verbose['std']))
    
    def extract(self):
        """
        luks tarball extraction routine
    
        @return: bool
        """
        print green(' * ') + '... luks.extract'
    
        os.system('tar xvfj %s/distfiles/cryptsetup-%s.tar.bz2 -C %s %s' % (utils.get_portdir(self.temp), str(self.luks_ver), self.temp['work'], self.verbose['std']))
    
    def configure(self):
        """
        luks Makefile interface to configure
    
        @return: bool
        """
        print green(' * ') + '... luks.configure'
        self.chgdir(self.lukstmp)
    
        return os.system('./configure --enable-static %s' % self.verbose['std'])
    
    def compile(self):
        """
        luks Makefile interface to make
    
        @return: bool
        """
        print green(' * ') + '... luks.compile'
        self.chgdir(self.lukstmp)
    
        return os.system('%s %s %s' % (self.master_config['DEFAULT_UTILS_MAKE'], self.master_config['DEFAULT_MAKEOPTS'], self.verbose['std']))
    
    def strip(self):
        """
        blkid strip binary routine
    
        @return: bool
        """
        print green(' * ') + '... luks.strip'
        self.chgdir(self.lukstmp)
    
        return os.system('strip %s/src/cryptsetup' % self.lukstmp)
    
    def compress(self):
        """
        blkid compression routine
    
        @return: bool
        """
        print green(' * ') + '... luks.compress'
        self.chgdir(self.lukstmp)
    
        return os.system('bzip2 %s/src/cryptsetup' % self.lukstmp)
    
    def cache(self):
        """
        blkid tarball cache routine
    
        @return: bool
        """
        print green(' * ') + '... luks.cache'
        self.chgdir(self.lukstmp)
    
        return utils.sprocessor('mv %s/src/cryptsetup.bz2 %s/cryptsetup-%s.bz2' % (self.lukstmp, self.temp['cache'], self.master_config['luks-version']), self.verbose)

