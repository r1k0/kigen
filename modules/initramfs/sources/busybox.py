import os
import sys
from stdout import green, turquoise, white, red, yellow
from utils.process import *
from utils.misc import *

class busybox:

    def __init__(self,          \
                arch,           \
                dotconfig,      \
                master_conf,    \
                version_conf,   \
                url_conf,       \
                libdir,         \
                temp,           \
                defconfig,      \
                oldconfig,      \
                menuconfig,     \
                verbose):

        self.arch       = arch
        self.dotconfig  = dotconfig
        self.master_conf= master_conf
        self.libdir     = libdir
        self.temp       = temp
        self.defconfig  = defconfig
        self.oldconfig  = oldconfig
        self.menuconfig = menuconfig
        self.verbose    = verbose
        self.bb_version = version_conf['busybox-version']
        self.url        = url_conf['busybox']
        self.bb_tmp     = temp['work'] + '/busybox-' + self.bb_version

    def build(self):
        """
        Busybox build sequence command

        @return         bool
        """
        zero = int('0')

        if os.path.isfile('%s/busybox-%s.tar.bz2' % (get_distdir(self.temp), str(self.bb_version))) is not True:
            print(green(' * ') + '... busybox.download')
            if self.download() is not zero:
                process('rm -v %s/busybox-%s.tar.bz2' % (get_distdir(self.temp), str(self.bb_version)), self.verbose)
                self.fail('download')

        print(green(' * ') + '... busybox.extract')
        if self.extract() is not zero: self.fail('extract')

        print(green(' * ') + '... busybox.copy_config '+self.dotconfig)
        if self.copy_config() is not zero: self.fail('copy_config')

        # compare bb .config version and the one from version.conf
        # if no match call oldconfig
        head = []
        nlines = 0
        for line in open(self.bb_tmp+'/.config'):
            line = line.replace(' ','')
            head.append(line.rstrip())
            nlines += 1
            if nlines >= 3:
                break
        lhead = head.pop()
        version = lhead.rsplit(':')
        version = version.pop()
        if version != self.bb_version:
            print(yellow(' * busybox .config version doesnt match the sources version, calling --oldconfig'))
            self.oldconfig = True

        if self.defconfig is True:
            print(green(' * ') + '... busybox.defconfig')
            if self.make_defconfig() is not zero: self.fail('defconfig')

        if self.oldconfig is True:
            print(green(' * ') + '... busybox.oldconfig')
            if self.make_oldconfig() is not zero: self.fail('oldconfig')

        if self.menuconfig is True:
            print(green(' * ') + '... busybox.menuconfig')
            if self.make_menuconfig() is not zero: self.fail('menuconfig')

        print(green(' * ') + '... busybox.make')
        if self.make() is not zero: self.fail('make')

        print(green(' * ') + '... busybox.strip')
        if self.strip() is not zero: self.fail('stip')

        print(green(' * ') + '... busybox.compress')
        if self.compress() is not zero: self.fail('compress')

        print(green(' * ') + '... busybox.cache')
        if self.cache() is not zero: self.fail('cache')

    def fail(self, step):
        """
        @arg step   string

        @return     exit
        """
        print(red('error')+': initramfs.busybox.'+step+'() failed')
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
        Busybox tarball download command

        """
        bb_url = self.url + '/busybox-' + str(self.bb_version) + '.tar.bz2'

        # FIXME utils.shell.process does not remove the output!!!!
        return os.system('/usr/bin/wget %s -O %s/busybox-%s.tar.bz2 %s' % (bb_url, get_distdir(self.temp), str(self.bb_version), self.verbose['std']))

    def extract(self):
        """
        Busybox tarball extract command

        @return         boot
        """
        return os.system('tar xvfj %s/busybox-%s.tar.bz2 -C %s %s' % (get_distdir(self.temp), str(self.bb_version), self.temp['work'], self.verbose['std']))

    def copy_config(self):
        """
        Busybox copy config file routine

        @return         bool
        """
        cpv = ''
        if self.verbose['set'] is True: cpv = '-v'
        if self.dotconfig:
            # copy dotconfig
            return os.system('cp %s %s %s/busybox-%s/.config' % (cpv, self.dotconfig, self.temp['work'], self.bb_version))
        else:
            # copy default
            return os.system('cp %s %s %s/busybox-%s/.config' % (cpv, self.libdir + '/arch/' + self.arch + '/busybox.config', self.temp['work'], self.bb_version))

    def strip(self):
        """
        Busybox binary strip routine
        """
        self.chgdir(self.bb_tmp)

        return os.system('strip %s/busybox ' % (self.bb_tmp))

    def compress(self):
        """
        Busybox binary compression routine

        @return: bool
        """
        self.chgdir(self.bb_tmp)

        return os.system('tar -cj -C %s -f %s/busybox-%s.tar.bz2 busybox .config' % (self.bb_tmp, self.temp['work'], self.bb_version))

    def cache(self):
        """
        Busybox cache tarball routine

        @return: bool
        """
        return os.system('mv %s/busybox-%s.tar.bz2  %s/busybox-bin-%s.tar.bz2' % (self.temp['work'], self.bb_version, self.temp['cache'], self.bb_version))

    # busybox building functions
    def build_command(self, target, verbose):
        """
        Busybox Makefile bash interface

        @arg: string

        @return: string
        """
        command = '%s CC="%s" LD="%s" AS="%s" ARCH="%s" %s %s' % (self.master_conf['UTILS_MAKE'],	\
                    self.master_conf['UTILS_CC'],	\
                    self.master_conf['UTILS_LD'],	\
                    self.master_conf['UTILS_AS'],	\
                    self.arch,                      \
                    target,                          \
                    verbose)
        return command

    def make_defconfig(self):
        """
        Busybox defconfig interface

        @return: bool
        """
        self.chgdir(self.bb_tmp)
        command = self.build_command('defconfig', self.verbose['std'])
        if self.verbose['set'] is True:
            print(command)

        return os.system(command)

    def make_oldconfig(self):
        """
        Busybox oldconfig interface

        @return: bool
        """
        self.chgdir(self.bb_tmp)
        command = self.build_command('oldconfig', '')
        if self.verbose['set'] is True:
            print(command)

        return os.system(command)

    def make_menuconfig(self):
        """
        Busybox menuconfig interface

        @return: bool
        """
        self.chgdir(self.bb_tmp)
        command = self.build_command('menuconfig', '')
        if self.verbose['set'] is True:
            print(command)

        return os.system(command)

    def make(self):
        """
        Busybox Makefile interface

        @return: bool
        """
        self.chgdir(self.bb_tmp)
        command = self.build_command('all', self.verbose['std'])
        if self.verbose['set'] is True:
            print(command)

        return os.system(command)
