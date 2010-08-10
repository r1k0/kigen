import os
import sys
from modules.stdout import green, turquoise, white, red, yellow
from modules.utils.shell import *
from modules.utils.misc import *

class busybox:

    def __init__(self,          \
                arch,           \
                dotconfig,      \
                master_config,  \
                libdir,         \
                temp,           \
                oldconfig,      \
                menuconfig,     \
                mrproper,       \
                verbose):

        self.arch       = arch
        self.dotconfig     = dotconfig
        self.master_config = master_config
        self.libdir     = libdir
        self.temp       = temp
        self.oldconfig  = oldconfig
        self.menuconfig = menuconfig
        self.mrproper   = mrproper
        self.verbose    = verbose
        self.bb_version = master_config['busybox-version']
        self.bb_tmp     = temp['work'] + '/busybox-' + master_config['busybox-version']
 
    def build(self):
        """
        Busybox build sequence command
    
        @return         bool
        """
        ret = zero = int('0')
    
        if os.path.isfile('%s/distfiles/busybox-%s.tar.bz2' % (get_portdir(self.temp), str(self.master_config['busybox-version']))) is not True:
            ret = self.download()
            if ret is not zero: 
                process('rm -v %s/distfiles/busybox-%s.tar.bz2' % (get_portdir(self.temp), str(self.master_config['busybox-version'])), self.verbose)
                self.fail('download')
    
        ret = self.extract()
        if ret is not zero: self.fail('extract')
    
        ret = self.copy_config()
        if ret is not zero: self.fail('copy_config')
    
        if self.mrproper is True:
            ret = self.make_mrproper()
            if ret is not zero: self.fail('mrproper')
    
        if self.oldconfig is True:
            ret = self.make_oldconfig()
            if ret is not zero: self.fail('oldconfig')

        if self.menuconfig is True:
            ret = self.make_menuconfig()
            if ret is not zero: self.fail('menuconfig')
    
        ret = self.make()
        if ret is not zero: self.fail('make')
    
        ret = self.strip()
        if ret is not zero: self.fail('stip')
    
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
        print red('error')+': initramfs.busybox.'+step+'() failed'
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
        Busybox tarball download command
        
        """
        print green(' * ') + '... busybox.download'
        bb_url = 'http://www.busybox.net/downloads/busybox-' + str(self.bb_version) + '.tar.bz2'

        # FIXME utils.shell.process does not remove the output!!!!
        return os.system('/usr/bin/wget %s -O %s/distfiles/busybox-%s.tar.bz2 %s' % (bb_url, get_portdir(self.temp), str(self.bb_version), self.verbose['std']))
    
    def extract(self):
        """
        Busybox tarball extract command
        
        @return         boot
        """
        print green(' * ') + '... busybox.extract'

        return os.system('tar xvfj %s/distfiles/busybox-%s.tar.bz2 -C %s %s' % (get_portdir(self.temp), str(self.bb_version), self.temp['work'], self.verbose['std']))
    
    def copy_config(self):
        """
        Busybox copy config file routine
        
        @return         bool
        """
        print green(' * ') + '... busybox.copy_config'
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
        print green(' * ') + '... busybox.strip'
        self.chgdir(self.bb_tmp)

        return os.system('strip %s/busybox ' % (self.bb_tmp))
    
    def compress(self):
        """
        Busybox binary compression routine
        
        @return: bool
        """
        print green(' * ') + '... busybox.compress'
        self.chgdir(self.bb_tmp)

        return os.system('tar -cj -C %s -f %s/busybox-%s.tar.bz2 busybox .config' % (self.bb_tmp, self.temp['work'], self.master_config['busybox-version']))
    
    def cache(self):
        """
        Busybox cache tarball routine
        
        @return: bool
        """
        print green(' * ') + '... busybox.cache'

        return os.system('mv %s/busybox-%s.tar.bz2  %s/busybox-bin-%s.tar.bz2' % (self.temp['work'], self.master_config['busybox-version'], self.temp['cache'], self.master_config['busybox-version']))
    
    # busybox building functions
    def build_command(self, target, verbose):
        """
        Busybox Makefile bash interface
        
        @arg: string

        @return: string
        """
        command = '%s CC="%s" LD="%s" AS="%s" ARCH="%s" %s %s' % (self.master_config['UTILS_MAKE'],	\
                    self.master_config['UTILS_CC'],	\
                    self.master_config['UTILS_LD'],	\
                    self.master_config['UTILS_AS'],	\
                    self.arch,                      \
                    target,                          \
                    verbose)
        return command
    
    def make_mrproper(self):
        """
        Busybox mrproper interface
        
        @return: bool
        """
        print green(' * ') + '... busybox.mrproper'
        self.chgdir(self.bb_tmp)
        command = self.build_command('mrproper', self.verbose['std'])
        if self.verbose['set'] is True:
            print command

        return os.system(command)
    
    def make_oldconfig(self):
        """
        Busybox oldconfig interface
        
        @return: bool
        """
        print green(' * ') + '... busybox.oldconfig'
        self.chgdir(self.bb_tmp)
#        return os.system('make oldconfig')
        command = self.build_command('oldconfig', '')
        if self.verbose['set'] is True:
        	print command

        return os.system(command)
    
    def make_menuconfig(self):
        """
        Busybox menuconfig interface
        
        @return: bool
        """
        print green(' * ') + '... busybox.menuconfig'
        self.chgdir(self.bb_tmp)
        command = self.build_command('menuconfig', '')
        if self.verbose['set'] is True:
            print command

        return os.system(command)
    
    def make(self):
        """
        Busybox Makefile interface
        
        @return: bool
        """
        print green(' * ') + '... busybox.make'
        self.chgdir(self.bb_tmp)
        command = self.build_command('all', self.verbose['std'])
        if self.verbose['set'] is True:
            print command
        
        return os.system(command)
        
