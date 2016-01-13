import os
import sys
from stdout import green, turquoise, white, red, yellow
from utils.process import *
from utils.misc import *

class dropbear:

    def __init__(self, master_config, version_conf, url_conf, hostsshkeys, debugflag, temp, verbose):

        self.master_config  = master_config
        self.temp           = temp
        self.verbose        = verbose
        self.dropbear_ver   = version_conf['dropbear-version']
        self.url            = url_conf['dropbear']
        self.hostsshkeys    = hostsshkeys
        self.dropbeartmp    = temp['work'] + '/dropbear-' + self.dropbear_ver
        self.debugflag      = debugflag

    def build(self):
        """
        dropbear build sequence

        @return:    bool
        """
        zero = int('0')

        if os.path.isfile('%s/dropbear-%s.tar.bz2' % (get_distdir(self.temp), str(self.dropbear_ver))) is not True:
            print(green(' * ') + '... dropbear.download')
            if self.download() is not zero:
                process('rm -v %s/dropbear-%s.tar.bz2' % (get_distdir(self.temp), str(self.dropbear_ver)), self.verbose)
                self.fail('download')

        print(green(' * ') + '... dropbear.extract')
        self.extract()
        # grr, tar thing to not return 0 when success

# FIXME there is no need to patch for scp->dbscp
# FIXME because there is NO scp bin inside the initramfs
# FIXME the patch only applies for cases when openssh is already installed
# FIXME to make dropbear and openssh coexist
# FIXME       if self.patch() is not zero: self.fail('patch')

        if self.debugflag is True:
            print(green(' * ') + '... dropbear.patch_debug_header #define DEBUG_TRACE')
            if self.patch_debug_header() is not zero: self.fail('patch_debug_header')

        print(green(' * ') + '... dropbear.configure')
        if self.configure() is not zero: self.fail('configure')

        print(green(' * ') + '... dropbear.make')
        if self.make() is not zero: self.fail('make')

        print(green(' * ') + '... dropbear.strip')
        if self.strip() is not zero: self.fail('strip')

        if self.hostsshkeys is True:
            print(green(' * ') + '... dropbear.host-dsskey')
            if self.hostsshkeys_dsa() is not zero: self.fail('host-dsskey')

            print(green(' * ') + '... dropbear.host-rsakey')
            if self.hostsshkeys_rsa() is not zero: self.fail('host-rsakey')
        else:
            print(green(' * ') + '... dropbear.dsskey')
            if self.dsskey() is not zero: self.fail('dsskey')

            print(green(' * ') + '... dropbear.rsakey')
            if self.rsakey() is not zero: self.fail('rsakey')

        print(green(' * ') + '... dropbear.compress')
        if self.compress() is not zero: self.fail('compress')

        print(green(' * ') + '... dropbear.cache')
        if self.cache() is not zero: self.fail('cache')

    def fail(self, step):
        """
        Exit

        @arg step   string
        @return     exit
        """
        print(red('error')+': initramfs.dropbear.'+step+'() failed')
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
        dropbear tarball download routine

        @return: bool
        """
        dropbear_url = self.url + '/dropbear-' + str(self.dropbear_ver) + '.tar.bz2'

#       return utils.process('/usr/bin/wget %s -O %s/opendropbear-%s.tar.bz2' % (dropbear_url, utils.get_distdir(temp), str(dropbearversion)), verbose)
        return os.system('/usr/bin/wget %s -O %s/dropbear-%s.tar.bz2 %s' % (dropbear_url, get_distdir(self.temp), str(self.dropbear_ver), self.verbose['std']))

    def extract(self):
        """
        dropbear tarball extraction routine

        @return: bool
        """
        self.chgdir(self.temp['work'])

        os.system('tar xvfj %s/dropbear-%s.tar.bz2 -C %s %s' % (get_distdir(self.temp), str(self.dropbear_ver), self.temp['work'], self.verbose['std']))

#    def patch(self): #, file):
#        """
#        patch dropbear-0.46-dbscp.patch
#
#        @return:    bool
#        """
#        # cd $D
#        # patch -p0 < dropbear-0.46-dbscp.patch
#        print green(' * ') + '... dropbear.patch'
#        self.chgdir(self.dropbeartmp)
#        # get dropbear-0.46-dbscp.patch
#        return os.system('patch -p0 < dropbear-0.46-dbscp.patch %s' % self.verbose['std'])

#    def get_config(self):
#        """
#        """
#        # get /etc/portage/savedconfig/net-misc/dropbear-0.52?
#        pass

    def patch_debug_header(self):
        """
        Patch debug.h by adding
        #define DEBUG_TRACE
        """
        self.chgdir(self.dropbeartmp)

        return os.system('mv debug.h debug.h.tmp && echo "#define DEBUG_TRACE" > debug.h && cat debug.h.tmp >> debug.h && rm debug.h.tmp')

    def configure(self):
        """
        dropbear interface to configure

        @return: bool
        """
        self.chgdir(self.dropbeartmp)

        return os.system('CFLAGS="-Os -static -Wall" LDFLAGS="-static" ./configure --disable-zlib %s' % self.verbose['std'])

    def make(self):
        """
        dropbear interface to Makefile

        @return: bool
        """
        self.chgdir(self.dropbeartmp)

        return os.system('STATIC=1 PROGRAMS="dropbear dbclient dropbearkey dropbearconvert scp" %s %s %s' % (self.master_config['DEFAULT_UTILS_MAKE'], self.master_config['DEFAULT_MAKEOPTS'], self.verbose['std']))

    def strip(self):
        """
        dropbear strip binary routine

        @return: bool
        """
        self.chgdir(self.dropbeartmp)

        os.system('strip %s/dbclient'           % self.dropbeartmp)
        os.system('strip %s/dropbear'           % self.dropbeartmp)
        os.system('strip %s/dropbearconvert'    % self.dropbeartmp)
        os.system('strip %s/scp'                % self.dropbeartmp)
        return os.system('strip %s/dropbearkey ' % self.dropbeartmp)

    def dsskey(self):
        """
        dropbear dsskey creation
        """
        self.chgdir(self.dropbeartmp)
        process('mkdir -p %s/etc/dropbear' % self.dropbeartmp, self.verbose)

        return process('./dropbearkey -t dss -f %s/etc/dropbear/dropbear_dss_host_key' % self.dropbeartmp, self.verbose)

    def rsakey(self):
        """
        dropbear rsakey creation
        """
        self.chgdir(self.dropbeartmp)
        process('mkdir -p %s/etc/dropbear' % self.dropbeartmp, self.verbose)

        return process('./dropbearkey -t rsa -s 4096 -f %s/etc/dropbear/dropbear_rsa_host_key' % self.dropbeartmp, self.verbose)

    def hostsshkeys_rsa(self):
        """
        dropbear host rsa ssh key convertion
        """
        self.chgdir(self.dropbeartmp)
        process('mkdir -p %s/etc/dropbear' % self.dropbeartmp, self.verbose)

        return process('./dropbearconvert openssh dropbear /etc/ssh/ssh_host_rsa_key %s/etc/dropbear/dropbear_rsa_host_key' % self.dropbeartmp, self.verbose)

    def hostsshkeys_dsa(self):
        """
        dropbear host dsa ssh key convertion
        """
        self.chgdir(self.dropbeartmp)
        process('mkdir -p %s/etc/dropbear' % self.dropbeartmp, self.verbose)

        return process('./dropbearconvert openssh dropbear /etc/ssh/ssh_host_dsa_key %s/etc/dropbear/dropbear_dss_host_key' % self.dropbeartmp, self.verbose)

    def compress(self):
        """
        dropbear compression routine

        @return: bool
        """
        self.chgdir(self.dropbeartmp)
        # create temp bin and sbin
        process('mkdir -p bin sbin usr/local/etc', self.verbose)
        process('cp dbclient dropbearconvert dropbearkey scp bin', self.verbose)
        process('cp dropbear sbin', self.verbose)
        # that is where dropbeard expects its conf file
#        process('cp dropbeard_config usr/local/etc', self.verbose)

#        return os.system('tar cf dropbear.tar bin sbin dev etc lib proc usr var')
        return os.system('tar cf dropbear.tar bin etc sbin  usr')

    def cache(self):
        """
        dropbear tarball cache routine

        @return: bool
        """
        self.chgdir(self.dropbeartmp)

        return process('mv %s/dropbear.tar %s/dropbear-%s.tar' % (self.dropbeartmp, self.temp['cache'], self.dropbear_ver), self.verbose)
