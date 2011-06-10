import os
import sys
from stdout import green, turquoise, white, red, yellow
from utils.process import *
from utils.misc import *

class lvm2:

    def __init__(self, master_config, version_conf, url_conf, temp, verbose):

        self.master_config  = master_config
        self.temp           = temp
        self.verbose        = verbose
        self.lvm2_ver       = str(version_conf['lvm2-version'])
        self.url            = url_conf['lvm2']
        self.lvm2_tmp       = temp['work']+'/LVM2.'+self.lvm2_ver

    def build(self):
        """
        lvm2 build sequence
    
        @return: bool
        """
        zero = int('0')
    
        if os.path.isfile('%s/LVM2.%s.tgz' % (get_distdir(self.temp), self.lvm2_ver)) is not True:
            print(green(' * ') + '... lvm2.download')
            if self.download() is not zero:
                process('rm -v %s/LVM2.%s.tgz' % (get_distdir(self.temp), self.lvm2_ver), self.verbose)
                self.fail('download')

        print(green(' * ') + '... lvm2.extract')
        self.extract()
        # grr, tar thing to not return 0 when success

        print(green(' * ') + '... lvm2.configure')
        if self.configure() is not zero: self.fail('configure')

        print(green(' * ') + '... lvm2.make')
        if self.make() is not zero: self.fail('make')

        print(green(' * ') + '... lvm2.install')
        if self.install() is not zero: self.fail('install')

        print(green(' * ') + '... lvm2.strip')
        if self.strip() is not zero: self.fail('strip')

        print(green(' * ') + '... lvm2.compress')
        if self.compress() is not zero: self.fail('compress')
 
        print(green(' * ') + '... lvm2.cache')
        if self.cache() is not zero: self.fail('cache')
    
    def fail(self, step):
        """
        @arg step   string

        @return     exit
        """
        print(red('error')+': initramfs.lvm2.'+step+'() failed')
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
        lvm2 tarball download routine

        @return: bool
        """
        lvm2_url = self.url+'/LVM2.' + self.lvm2_ver + '.tgz'

        # FIXME utils.shell.process does not remove the output!!!!
        return os.system('/usr/bin/wget %s -O %s/LVM2.%s.tgz %s' % (lvm2_url, get_distdir(self.temp), self.lvm2_ver, self.verbose['std']))

    def extract(self):
        """
        lvm2 tarball extraction routine

        @return: bool
        """
        os.system('tar xvfz %s/LVM2.%s.tgz -C %s %s' % (get_distdir(self.temp), self.lvm2_ver, self.temp['work'], self.verbose['std']))
    
    def configure(self):
        """
        lvm2 Makefile interface to configure

        @return: bool
        """
        self.chgdir(self.lvm2_tmp)

        return os.system('./configure --disable-selinux --enable-static_link %s' % self.verbose['std'])

    def make(self):
        """
        lvm2 Makefile interface to make

        @return: bool
        """
        self.chgdir(self.lvm2_tmp)

        return os.system('%s %s CC="%s" LD="%s" AS="%s" %s' % (self.master_config['DEFAULT_UTILS_MAKE'], \
                                                                self.master_config['DEFAULT_MAKEOPTS'], \
                                                                self.master_config['DEFAULT_UTILS_CC'], \
                                                                self.master_config['DEFAULT_UTILS_LD'], \
                                                                self.master_config['DEFAULT_UTILS_AS'], \
                                                                self.verbose['std']))

#    def make_device_mapper(self):
#        """
#        lvm2 Makefile interface to make device-mapper
#
#        @return: bool
#        """
#        self.chgdir(self.lvm2_tmp)
#
#        return os.system('%s %s CC="%s" LD="%s" AS="%s" device-mapper %s' % (self.master_config['DEFAULT_UTILS_MAKE'], \
#                                    self.master_config['DEFAULT_MAKEOPTS'], \
#                                    self.master_config['DEFAULT_UTILS_CC'], \
#                                    self.master_config['DEFAULT_UTILS_LD'], \
#                                    self.master_config['DEFAULT_UTILS_AS'], \
#                                    self.verbose['std']))
#
#    def make_device_mapper_install(self):
#        """
#        lvm2 Makefile interface to make device-mapper_install
#
#        @return: bool
#        """
#        self.chgdir(self.lvm2_tmp)
#
#        return os.system('%s %s CC="%s" LD="%s" AS="%s" device-mapper_install %s' % (self.master_config['DEFAULT_UTILS_MAKE'], \
#                                    self.master_config['DEFAULT_MAKEOPTS'], \
#                                    self.master_config['DEFAULT_UTILS_CC'], \
#                                    self.master_config['DEFAULT_UTILS_LD'], \
#                                    self.master_config['DEFAULT_UTILS_AS'], \
#                                    self.verbose['std']))

    def install(self):
        """
        Install lvm2

        @return: bool
        """
        self.chgdir(self.lvm2_tmp)

        return os.system('%s %s CC="%s" LD="%s" AS="%s" install %s' % (self.master_config['DEFAULT_UTILS_MAKE'], \
                                                                        self.master_config['DEFAULT_MAKEOPTS'], \
                                                                        self.master_config['DEFAULT_UTILS_CC'], \
                                                                        self.master_config['DEFAULT_UTILS_LD'], \
                                                                        self.master_config['DEFAULT_UTILS_AS'], \
                                                                        self.verbose['std']))
    
    def strip(self):
        """
        lvm.static strip binary routine

        @return: bool
        """
        self.chgdir(self.lvm2_tmp)

        return os.system('strip tools/lvm.static ')
    
    def compress(self):
        """
        lvm.static compression routine
    
        @return: bool
        """
        self.chgdir(self.lvm2_tmp)

        return os.system('bzip2 tools/lvm.static')
    
    def cache(self):
        """
        lvm.static tarball cache routine

        @return: bool
        """
        self.chgdir(self.lvm2_tmp)
        mvv = ''
        if self.verbose['set'] is '': mvv = '-v'

        return os.system('mv %s tools/lvm.static.bz2 %s/lvm.static-%s.bz2' % (mvv, self.temp['cache'], self.lvm2_ver))
