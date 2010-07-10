import os
import sys
from stdout import green, turquoise, white, red, yellow
import utils

class dropbear:

    def __init__(self, master_config, temp, verbose):
        
        self.master_config  = master_config
        self.temp           = temp
        self.verbose        = verbose
        self.dropbear_ver   = master_config['dropbear-version']
        self.dropbeartmp    = temp['work'] + '/dropbear-' + master_config['dropbear-version']

    def build():
        """
        dropbear build sequence

        @return:    bool
        """
        ret = zero = int('0')
    
        if os.path.isfile('%s/distfiles/opendropbear-%s.tar.gz' % (utils.get_portdir(self.temp), str(self.dropbear_ver))) is not True:
            ret = self.download()
            if ret is not zero: self.fail('download')
    
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
        print red('error')+': initramfs.dropbear.'+step+'() failed'
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
        dropbear tarball download routine
    
        @return: bool
        """
        print green(' * ') + '... dropbear.download'
        dropbear_url = 'http://matt.ucc.asn.au/dropbear/releases/' + '/dropbear-' + str(dropbear_ver) + '.tar.gz'
    #    return utils.sprocessor('/usr/bin/wget %s -O %s/distfiles/opendropbear-%s.tar.gz' % (dropbear_url, utils.get_portdir(temp), str(dropbearversion)), verbose)
        return os.system('/usr/bin/wget %s -O %s/distfiles/dropbear-%s.tar.gz %s' % (dropbear_url, utils.get_portdir(self.temp), str(self.dropbear_ver), self.verbose['std']))
    
    def extract(self):
        """
        dropbear tarball extraction routine
    
        @return: bool
        """
        print green(' * ') + '... dropbear.extract'
    
        os.system('tar xvfz %s/distfiles/dropbear-%s.tar.gz -C %s %s' % (utils.get_portdir(self.temp), str(self.dropbear_ver), self.temp['work'], self.verbose['std']))
    
    def configure(self):
        """
        dropbear Makefile interface to configure
    
        @return: bool
        """
        print green(' * ') + '... dropbear.configure'
        utils.chgdir(self.dropbeartmp)
    
        return os.system('CFLAGS="-Os -static -Wall" LDFLAGS="-static" ./configure --disable-zlib %s' % self.verbose['std'])
    
    def compile(self):
        """
        dropbear Makefile interface to make
    
        @return: bool
        """
        print green(' * ') + '... dropbear.compile'
        utils.chgdir(self.dropbeartmp)
    
        return os.system('%s %s %s' % (self.master_config['DEFAULT_UTILS_MAKE'], self.master_config['DEFAULT_MAKEOPTS'], self.verbose['std']))
    
    def strip(self):
        """
        blkid strip binary routine
    
        @return: bool
        """
        print green(' * ') + '... dropbear.strip'
        utils.chgdir(self.dropbeartmp)
    
        os.system('strip %s/dbclient ' % self.dropbeartmp)
        os.system('strip %s/dropbear ' % self.dropbeartmp)
        os.system('strip %s/dropbearconvert ' % self.dropbeartmp)
        return os.system('strip %s/dropbearkey ' % self.dropbeartmp)
    
    def compress(self):
        """
        blkid compression routine
    
        @return: bool
        """
        print green(' * ') + '... dropbear.compress'
    
        utils.chgdir(self.dropbeartmp)
        # create temp bin and sbin
        utils.sprocessor('mkdir -p bin', self.verbose)
        utils.sprocessor('mkdir -p sbin', self.verbose)
        utils.sprocessor('mkdir -p usr/local/etc', self.verbose)
        utils.sprocessor('cp dropbear sftp scp bin', self.verbose)
        utils.sprocessor('cp dropbeard sbin', self.verbose)
        # that is where dropbeard expects its conf file
        utils.sprocessor('cp dropbeard_config usr/local/etc', self.verbose)
        # TODO create user/group dropbear 
    
        return os.system('tar cf dropbear.tar bin sbin usr')
    
    def cache(self):
        """
        blkid tarball cache routine
    
        @return: bool
        """
        print green(' * ') + '... dropbear.cache'
        utils.chgdir(self.dropbeartmp)
    
        return utils.sprocessor('mv %s/dropbear.tar %s/dropbear-%s.tar' % (self.dropbeartmp, self.temp['cache'], self.master_config['dropbear-version']), self.verbose)
