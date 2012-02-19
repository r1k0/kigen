import os
import sys
from stdout import green, turquoise, white, red, yellow
from utils.process import *
from utils.misc import *

class strace:

    def __init__(self, master_config, version_conf, url_conf, temp, verbose):

        self.master_config  = master_config
        self.temp           = temp
        self.verbose        = verbose
        self.strace_ver     = version_conf['strace-version']
        self.url            = url_conf['strace']
        self.stracetmp      = temp['work'] + '/strace-' + self.strace_ver
        
    def build(self):
        """
        strace build sequence

        @return     bool
        """
        zero = int('0')
    
        if os.path.isfile('%s/strace-%s.tar.bz2' % (get_distdir(self.temp), self.strace_ver)) is not True:
            print(green(' * ') + '... strace.download')
            if self.download() is not zero:
                process('rm %s/strace-%s.tar.bz2' % (get_distdir(self.temp), self.strace_ver), self.verbose)
                self.fail('download')
    
        print(green(' * ') + '... strace.extract')
        self.extract()
        # grr, tar thing to not return 0 when success
    
        print(green(' * ') + '... strace.configure')
        if self.configure() is not zero: self.fail('configure')
    
        print(green(' * ') + '... strace.make')
        if self.make() is not zero: self.fail('make')
    
        print(green(' * ') + '... strace.strip')
        if self.strip() is not zero: self.fail('strip')
    
        print(green(' * ') + '... strace.compress')
        if self.compress() is not zero: self.fail('compress')
    
        print(green(' * ') + '... strace.cache')
        if self.cache() is not zero: self.fail('cache')
    
    def fail(self, step):
        """
        @arg step   string

        @return     exit
        """
        print(red('error')+': initramfs.strace.'+step+'() failed')
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
        strace tarball download routine
    
        @return: bool
        """
        strace_url = self.url+'/'+str(self.strace_ver)+'/strace-' + str(self.strace_ver) + '.tar.bz2'

        # FIXME utils.shell.process does not remove the output!!!!
        return os.system('/usr/bin/wget --no-proxy %s -O %s/strace-%s.tar.bz2 %s' % (strace_url, get_distdir(self.temp), str(self.strace_ver), self.verbose['std']))
    
    def extract(self):
        """
        strace tarball extraction routine
    
        @return: bool
        """
        os.system('tar xvfj %s/strace-%s.tar.bz2 -C %s %s' % (get_distdir(self.temp), str(self.strace_ver), self.temp['work'], self.verbose['std']))
    
    # strace building functions
    def configure(self):
        """
        strace Makefile interface to configure
    
        @return: bool
        """
        self.chgdir(self.stracetmp)
    
        return os.system('LDFLAGS=-static ./configure %s' % self.verbose['std'])
    
    def make(self):
        """
        strace Makefile interface to make
    
        @return: bool
        """
        self.chgdir(self.stracetmp)
    
        return os.system('%s %s %s' % (self.master_config['DEFAULT_UTILS_MAKE'], self.master_config['DEFAULT_MAKEOPTS'], self.verbose['std']))
    
    def strip(self):
        """
        strace strip binary routine
    
        @arg stracetmp          string
        @arg master_config  dict
    
        @return: bool
        """
        self.chgdir(self.stracetmp)
    
        return os.system('strip %s/strace ' % self.stracetmp)
    
    def compress(self):
        """
        strace compression routine
    
        @arg stracetmp          string
        @arg master_config  dict
    
        @return: bool
        """
        self.chgdir(self.stracetmp)
    
        return os.system('bzip2 %s/strace' % self.stracetmp)
    
    def cache(self):
        """
        strace tarball cache routine
    
        @return: bool
        """
        self.chgdir(self.stracetmp)
    
        return process('mv %s/strace.bz2 %s/strace-%s.bz2' % (self.stracetmp, self.temp['cache'], self.strace_ver), self.verbose)
