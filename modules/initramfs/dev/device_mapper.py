import os
import sys
from stdout import green, turquoise, white, red, yellow
import utils

# OBSOLETE source now inside lvm2

class device_mapper:

    def __init__(self, master_config, temp, verbose):

        self.master_config  = master_config
        self.temp           = temp
        self.verbose        = verbose
        self.dm_tmp         = temp['work'] + '/device-mapper.' + master_config['device-mapper-version']
        self.dm_ver         = str(master_config['device-mapper-version'])

    def build(self):
        pass
        """
        device-mapper build sequence

        @return: bool
        """
        zero = int('0')
        ret = True

        if os.path.isfile('%s/device-mapper.%s.tgz' % (utils.get_distdir(self.temp), self.dm_ver)) is not True:
            ret = self.download()
            if ret is not zero:
                os.system('rm %s/device-mapper.%s.tgz' % (utils.get_distdir(self.temp), self.dm_ver))
                self.fail('download')

        self.extract()
        # grr, tar thing to not return 0 when success

        ret = self.configure()
        if ret is not zero: self.fail('configure')

        ret = self.make()
        if ret is not zero: self.fail('make')

        ret = self.install()
        if ret is not zero: self.fail('install')

        # TODO remove manpage rm -rf %s/device-mapper/man % temp['work']
        os.system('rm -rf %s/man' % self.dm_tmp)

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
        print(red('error')+': initramfs.device_mapper.'+step+'() failed')
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
    	Download device-mapper tarball

    	@return: bool
    	"""
    	print(green(' * ') + '... device_mapper.download')
    	# TODO: get GENTOO_MIRRORS from portageq (better if I could import a portage module)
    	device_mapper_url = 'http://ftp.snt.utwente.nl/pub/os/linux/gentoo/distfiles/device-mapper.' + self.dm_ver + '.tgz'

    	return os.system('/usr/bin/wget %s -O %s/device-mapper.%s.tgz %s' % (device_mapper_url, utils.get_distdir(self.temp), self.dm_ver, self.verbose['std']))

    def extract(self):
    	"""
    	Extract device-mapper tarball

    	@return: bool
    	"""
    	print(green(' * ') + '... device_mapper.extract')

    	os.system('tar xvfz %s/device-mapper.%s.tgz -C %s %s' % (utils.get_distdir(self.temp), self.dm_ver, self.temp['work'], self.verbose['std']))

    def configure(self):
    	"""
    	Configure device-mapper source code

    	@return: bool
    	"""
    	print(green(' * ') + '... device_mapper.configure')
    	self.chgdir(self.dm_tmp)

    	return os.system('./configure --prefix=%s/device-mapper --enable-static_link --disable-selinux %s' % (self.temp['work'], self.verbose['std']))

    def make(self):
    	"""
    	Compile device-mapper source code

    	@return: bool
    	"""
    	print(green(' * ') + '... device_mapper.make')
    	self.chgdir(self.dm_tmp)

    	return os.system('%s %s CC="%s" LD="%s" AS="%s" %s' % (self.master_config['DEFAULT_UTILS_MAKE'], \
    								self.master_config['DEFAULT_MAKEOPTS'], \
    								self.master_config['DEFAULT_UTILS_CC'], \
    								self.master_config['DEFAULT_UTILS_LD'], \
    								self.master_config['DEFAULT_UTILS_AS'], \
    								self.verbose['std']))

    def install(self):
    	"""
    	Install device-mapper

    	@return: bool
    	"""
    	print(green(' * ') + '... device_mapper.install')
    	self.chgdir(self.dm_tmp)

    	return os.system('%s %s CC="%s" LD="%s" AS="%s" install %s' % (self.master_config['DEFAULT_UTILS_MAKE'], \
    						self.master_config['DEFAULT_MAKEOPTS'], \
    						self.master_config['DEFAULT_UTILS_CC'], \
    						self.master_config['DEFAULT_UTILS_LD'], \
    						self.master_config['DEFAULT_UTILS_AS'], \
    						self.verbose['std']))

    def strip(self):
    	"""
    	Strip dmsetup binary

    	@return: bool
    	"""
    	print(green(' * ') + '... device_mapper.strip')
    	self.chgdir(self.temp['work'])

    	return os.system('strip %s/device-mapper/sbin/dmsetup' % (self.temp['work']))

    def compress(self):
    	"""
    	Compress dmsetup binary

    	@return: bool
    	"""
    	print(green(' * ') + '... device_mapper.compress')
    	self.chgdir(self.temp['work'])

    	return os.system('tar -jcf %s device-mapper %s' % (self.temp['cache']+'/dmsetup-device-mapper-'+self.dm_ver+'.tar.bz2', self.verbose['std']))

    def cache(self):
    	"""
    	Cache compressed dmsetup binary

    	@return: bool
    	"""
    	print(green(' * ') + '... device_mapper.cache')
    	self.chgdir(self.dm_tmp)
    	mvv = ''
    	if self.verbose['set'] is '': mvv = '-v'

    	return os.system('mv %s %s %s/device-mapper-%s.tar.bz2' % (mvv, \
                             self.temp['cache']+'/dmsetup-device-mapper-'+self.dm_ver+'.tar.bz2', \
                             self.temp['cache'], \
                             self.master_config['device-mapper-version']))
