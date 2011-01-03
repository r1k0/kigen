import os
import sys
from stdout import green, turquoise, white, red, yellow
from utils.process import *
from utils.misc import *

class e2fsprogs:

    def __init__(self, master_config, version_conf, temp, verbose):

        self.master_config  = master_config
        self.temp           = temp
        self.verbose        = verbose
        self.e2fsprogs_ver  = version_conf['e2fsprogs-version']
        self.e2tmp          = temp['work'] + '/e2fsprogs-' + self.e2fsprogs_ver
        
    def build(self):
        """
        e2fsprogs build sequence

        @return     bool
        """
        ret = zero = int('0')
    
        if os.path.isfile('%s/e2fsprogs-%s.tar.gz' % (get_distdir(self.temp), self.e2fsprogs_ver)) is not True:
            if self.download() is not zero:
                process('rm %s/e2fsprogs-%s.tar.gz' % (get_distdir(self.temp), self.e2fsprogs_ver), self.verbose)
                self.fail('download')
    
        self.extract()
        # grr, tar thing to not return 0 when success
    
        if self.configure() is not zero: self.fail('configure')
    
        if self.make() is not zero: self.fail('make')
    
        if self.strip() is not zero: self.fail('strip')
    
        if self.compress() is not zero: self.fail('compress')
    
        if self.cache() is not zero: self.fail('cache')
    
    def fail(self, step):
        """
        @arg step   string

        @return     exit
        """
        print(red('error')+': initramfs.e2fsprogs.'+step+'() failed')
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
        e2fsprogs tarball download routine
    
        @return: bool
        """
        print(green(' * ') + '... e2fsprogs.download')
        e2fsprogs_url = 'http://downloads.sourceforge.net/project/e2fsprogs/e2fsprogs/'+str(self.e2fsprogs_ver)+'/e2fsprogs-' + str(self.e2fsprogs_ver) + '.tar.gz'

        # FIXME utils.shell.process does not remove the output!
        return os.system('/usr/bin/wget %s -O %s/e2fsprogs-%s.tar.gz %s' % (e2fsprogs_url, get_distdir(self.temp), str(self.e2fsprogs_ver), self.verbose['std']))
    
    def extract(self):
        """
        e2fsprogs tarball extraction routine
    
        @return: bool
        """
        print(green(' * ') + '... e2fsprogs.extract')
    
        os.system('tar xvfz %s/e2fsprogs-%s.tar.gz -C %s %s' % (get_distdir(self.temp), str(self.e2fsprogs_ver), self.temp['work'], self.verbose['std']))
    
    # e2fsprogrs building functions
    def configure(self):
        """
        e2fsprogs Makefile interface to configure
    
        @return: bool
        """
        print(green(' * ') + '... e2fsprogs.configure')
        self.chgdir(self.e2tmp)
    
        return os.system('LDFLAGS=-static ./configure %s' % self.verbose['std'])
    
    def make(self):
        """
        e2fsprogs Makefile interface to make
    
        @return: bool
        """
        print(green(' * ') + '... e2fsprogs.make')
        self.chgdir(self.e2tmp)
    
        return os.system('%s %s %s' % (self.master_config['DEFAULT_UTILS_MAKE'], self.master_config['DEFAULT_MAKEOPTS'], self.verbose['std']))
    
    def strip(self):
        """
        blkid strip binary routine
    
        @arg e2tmp          string
        @arg master_config  dict
    
        @return: bool
        """
        print(green(' * ') + '... e2fsprogs.strip')
        self.chgdir(self.e2tmp)
        os.system('cp %s/misc/blkid %s/misc/blkid.bak' % (self.e2tmp, self.e2tmp))

        return os.system('strip %s/misc/blkid ' % self.e2tmp)
    
    def compress(self):
        """
        blkid compression routine
    
        @arg e2tmp          string
        @arg master_config  dict
    
        @return: bool
        """
        print(green(' * ') + '... e2fsprogs.compress')
        self.chgdir(self.e2tmp)
    
        return os.system('bzip2 %s/misc/blkid' % self.e2tmp)
    
    def cache(self):
        """
        blkid tarball cache routine
    
        @return: bool
        """
        print(green(' * ') + '... e2fsprogs.cache')
        self.chgdir(self.e2tmp)
    
        return process('mv %s/misc/blkid.bz2 %s/blkid-e2fsprogs-%s.bz2' % (self.e2tmp, self.temp['cache'], self.e2fsprogs_ver), self.verbose)

