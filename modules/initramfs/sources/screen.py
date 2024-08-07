import os
import sys
from stdout import green, turquoise, white, red, yellow
from utils.process import *
from utils.misc import *

class screen:

    def __init__(self, master_config, version_conf, url_conf, temp, verbose):

        self.master_config  = master_config
        self.temp           = temp
        self.verbose        = verbose
        self.screen_ver     = version_conf['screen-version']
        self.url            = url_conf['screen']
        self.screentmp      = temp['work'] + '/screen-' + self.screen_ver

    def build(self):
        """
        screen build sequence

        @return     bool
        """
        zero = int('0')

        if os.path.isfile('%s/screen-%s.tar.gz' % (get_distdir(self.temp), self.screen_ver)) is not True:
            print(green(' * ') + '... screen.download')
            if self.download() is not zero:
                process('rm %s/screen-%s.tar.gz' % (get_distdir(self.temp), self.screen_ver), self.verbose)
                self.fail('download')

        print(green(' * ') + '... screen.extract')
        self.extract()
        # grr, tar thing to not return 0 when success

        print(green(' * ') + '... screen.configure')
        if self.configure() is not zero: self.fail('configure')

        print(green(' * ') + '... screen.make')
        if self.make() is not zero: self.fail('make')

        print(green(' * ') + '... screen.strip')
        if self.strip() is not zero: self.fail('strip')

        print(green(' * ') + '... screen.compress')
        if self.compress() is not zero: self.fail('compress')

        print(green(' * ') + '... screen.cache')
        if self.cache() is not zero: self.fail('cache')

    def fail(self, step):
        """
        @arg step   string

        @return     exit
        """
        print(red('error')+': initramfs.screen.'+step+'() failed')
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
        screen tarball download routine

        @return: bool
        """
        screen_url = self.url + '/screen-' + str(self.screen_ver) + '.tar.gz'

        # FIXME utils.shell.process does not remove the output
        return os.system('/usr/bin/wget %s -O %s/screen-%s.tar.gz %s' % (screen_url, get_distdir(self.temp), str(self.screen_ver), self.verbose['std']))

    def extract(self):
        """
        screen tarball extraction routine

        @return: bool
        """
        os.system('tar xvfz %s/screen-%s.tar.gz -C %s %s' % (get_distdir(self.temp), str(self.screen_ver), self.temp['work'], self.verbose['std']))

    def configure(self):
        """
        screen Makefile interface to configure

        @return: bool
        """
        self.chgdir(self.screentmp)

        return os.system('LDFLAGS=-static ./configure %s' % self.verbose['std'])

    def make(self):
        """
        screen Makefile interface to make

        @return: bool
        """
        self.chgdir(self.screentmp)

        return os.system('%s %s %s' % (self.master_config['DEFAULT_UTILS_MAKE'], self.master_config['DEFAULT_MAKEOPTS'], self.verbose['std']))

    def strip(self):
        """
        screen strip binary routine

        @arg screentmp          string
        @arg master_config  dict

        @return: bool
        """
        self.chgdir(self.screentmp)

        return os.system('strip %s/screen ' % self.screentmp)

    def compress(self):
        """
        screen compression routine

        @arg screentmp          string
        @arg master_config  dict

        @return: bool
        """
        self.chgdir(self.screentmp)

        return os.system('bzip2 %s/screen' % self.screentmp)

    def cache(self):
        """
        screen tarball cache routine

        @return: bool
        """
        self.chgdir(self.screentmp)

        return process('cp %s/screen.bz2 %s/screen-%s.bz2' % (self.screentmp, self.temp['cache'], self.screen_ver), self.verbose)
