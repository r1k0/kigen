import os
import sys
from stdout import green, turquoise, white, red, yellow
import utils

class e2fsprogs:

    def __init__(self, master_config, temp, verbose):

        self.master_config  = master_config
        self.temp           = temp
        self.verbose        = verbose
        self.e2fsprogs_ver  = master_config['e2fsprogs-version']
        self.e2tmp          = temp['work'] + '/e2fsprogs-' + master_config['e2fsprogs-version']
        
    def build(self):
        """
        e2fsprogs build sequence

        @return     bool
        """
        ret = zero = int('0')
    
        if os.path.isfile('%s/distfiles/e2fsprogs-%s.tar.gz' % (utils.get_portdir(self.temp), self.master_config['e2fsprogs-version'])) is not True:
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
        @arg step   string

        @return     exit
        """
        print red('error')+': initramfs.e2fsprogs.'+step+'() failed'
        sys.exit(2)

    def download(self):
        """
        e2fsprogs tarball download routine
    
        @return: bool
        """
        print green(' * ') + '... e2fsprogs.download'
        e2fsprogs_url = 'http://downloads.sourceforge.net/project/e2fsprogs/e2fsprogs/' + \
                    str(self.e2fsprogs_ver)  + \
                    '/e2fsprogs-' + str(self.e2fsprogs_ver) + '.tar.gz'
        return os.system('/usr/bin/wget %s -O %s/distfiles/e2fsprogs-%s.tar.gz %s' % (self.e2fsprogs_url, utils.get_portdir(self.temp), str(self.e2fsprogs_ver), self.verbose['std']))
    
    def extract(self):
        """
        e2fsprogs tarball extraction routine
    
        @return: bool
        """
        print green(' * ') + '... e2fsprogs.extract'
    
        os.system('tar xvfz %s/distfiles/e2fsprogs-%s.tar.gz -C %s %s' % (utils.get_portdir(self.temp), str(self.e2fsprogs_ver), self.temp['work'], self.verbose['std']))
    
    # e2fsprogrs building functions
    def configure(self):
        """
        e2fsprogs Makefile interface to configure
    
        @return: bool
        """
        print green(' * ') + '... e2fsprogs.configure'
        utils.chgdir(self.e2tmp)
    
        return os.system('./configure --with-ldopts=-static %s' % self.verbose['std'])
    
    def compile(self):
        """
        e2fsprogs Makefile interface to make
    
        @return: bool
        """
        print green(' * ') + '... e2fsprogs.compile'
        utils.chgdir(self.e2tmp)
    
        return os.system('%s %s %s' % (self.master_config['DEFAULT_UTILS_MAKE'], self.master_config['DEFAULT_MAKEOPTS'], self.verbose['std']))
    
    def strip(self):
        """
        blkid strip binary routine
    
        @arg e2tmp          string
        @arg master_config  dict
    
        @return: bool
        """
        print green(' * ') + '... e2fsprogs.strip'
        utils.chgdir(self.e2tmp)
    
        return os.system('strip %s/misc/blkid ' % self.e2tmp)
    
    def compress(self):
        """
        blkid compression routine
    
        @arg e2tmp          string
        @arg master_config  dict
    
        @return: bool
        """
        print green(' * ') + '... e2fsprogs.compress'
        utils.chgdir(self.e2tmp)
    
        return os.system('bzip2 %s/misc/blkid' % self.e2tmp)
    
    def cache(self):
        """
        blkid tarball cache routine
    
        @return: bool
        """
        print green(' * ') + '... e2fsprogs.cache'
        utils.chgdir(self.e2tmp)
    
        return utils.sprocessor('mv %s/misc/blkid.bz2 %s/blkid-e2fsprogs-%s.bz2' % (self.e2tmp, self.temp['cache'], self.master_config['e2fsprogs-version']), self.verbose)

