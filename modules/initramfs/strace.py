import os
import sys
from stdout import green, turquoise, white, red, yellow
from utils.shell import *
from utils.misc import *

class strace:

    def __init__(self, master_config, temp, verbose):

        self.master_config  = master_config
        self.temp           = temp
        self.verbose        = verbose
        self.strace_ver     = master_config['strace-version']
        self.stracetmp      = temp['work'] + '/strace-' + master_config['strace-version']
        
    def build(self):
        """
        strace build sequence

        @return     bool
        """
        ret = zero = int('0')
    
        if os.path.isfile('%s/distfiles/strace-%s.tar.gz' % (get_portdir(self.temp), self.strace_ver)) is not True:
            ret = self.download()
            if ret is not zero:
                process('rm %s/distfiles/strace-%s.tar.gz' % (get_portdir(self.temp), self.strace_ver), self.verbose)
                self.fail('download')
    
        self.extract()
    #   grr, tar thing to not return 0 when success
    
        ret = self.configure()
        if ret is not zero: self.fail('configure')
    
        ret = self.make()
        if ret is not zero: self.fail('make')
    
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
        print red('error')+': initramfs.strace.'+step+'() failed'
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
        strace tarball download routine
    
        @return: bool
        """
        print green(' * ') + '... strace.download'
        strace_url = 'http://downloads.sourceforge.net/project/strace/strace/'+str(self.strace_ver)+'/strace-' + str(self.strace_ver) + '.tar.gz'

        # FIXME utils.shell.process does not remove the output!!!!
        return os.system('/usr/bin/wget %s -O %s/distfiles/strace-%s.tar.gz %s' % (strace_url, get_portdir(self.temp), str(self.strace_ver), self.verbose['std']))
    
    def extract(self):
        """
        strace tarball extraction routine
    
        @return: bool
        """
        print green(' * ') + '... strace.extract'
    
        os.system('tar xvfz %s/distfiles/strace-%s.tar.gz -C %s %s' % (get_portdir(self.temp), str(self.strace_ver), self.temp['work'], self.verbose['std']))
    
    # e2fsprogrs building functions
    def configure(self):
        """
        strace Makefile interface to configure
    
        @return: bool
        """
        print green(' * ') + '... strace.configure'
        self.chgdir(self.e2tmp)
    
#        return os.system('./configure --with-ldopts=-static %s' % self.verbose['std'])
        return os.system('LDFLAGS=-static ./configure %s' % self.verbose['std'])
    
    def make(self):
        """
        strace Makefile interface to make
    
        @return: bool
        """
        print green(' * ') + '... strace.make'
        self.chgdir(self.e2tmp)
    
        return os.system('%s %s %s' % (self.master_config['DEFAULT_UTILS_MAKE'], self.master_config['DEFAULT_MAKEOPTS'], self.verbose['std']))
    
    def strip(self):
        """
        blkid strip binary routine
    
        @arg e2tmp          string
        @arg master_config  dict
    
        @return: bool
        """
        print green(' * ') + '... strace.strip'
        self.chgdir(self.e2tmp)
    
        return os.system('strip %s/misc/blkid ' % self.e2tmp)
    
    def compress(self):
        """
        blkid compression routine
    
        @arg e2tmp          string
        @arg master_config  dict
    
        @return: bool
        """
        print green(' * ') + '... strace.compress'
        self.chgdir(self.e2tmp)
    
        return os.system('bzip2 %s/misc/blkid' % self.e2tmp)
    
    def cache(self):
        """
        blkid tarball cache routine
    
        @return: bool
        """
        print green(' * ') + '... strace.cache'
        self.chgdir(self.e2tmp)
    
        return process('mv %s/misc/blkid.bz2 %s/blkid-strace-%s.bz2' % (self.e2tmp, self.temp['cache'], self.master_config['strace-version']), self.verbose)

