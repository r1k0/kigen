import os
import sys
from stdout import green, turquoise, white, red, yellow
import utils

class lvm2:

    def __init__(self, master_config, temp, verbose):

        self.master_config  = master_config
        self.temp           = temp
        self.verbose        = verbose
        self.lvm2_ver       = str(master_config['lvm2-version'])
        self.lvm2_tmp       = temp['work']+'/LVM2.'+master_config['lvm2-version']

    def build(self):
        """
        lvm2 build sequence
    
        @return: bool
        """
        zero = int('0')
        ret = True
    
        if os.path.isfile('%s/distfiles/LVM2.%s.tgz' % (utils.get_portdir(self.temp), self.lvm2_ver)) is not True:
            ret = self.download()
            if ret is not True: self.fail('download')
    
        self.extract()
        # grr, tar thing to not return 0 when success
    
        ret = self.configure()
        if ret is not zero: self.fail('configure')
    
        ret = self.compile()
        if ret is not zero: self.fail('compile')
    
        ret = self.install()
        if ret is not zero: self.fail('install')
    
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
        print red('error')+': initramfs.lvm2.'+step+'() failed'
        sys.exit(2)

    def download(self):
    	"""
    	lvm2 tarball download routine
    
    	@return: bool
    	"""
    	print green(' * ') + '... lvm2.download'
    	lvm2_url = 'ftp://sources.redhat.com/pub/lvm2/' + '/LVM2.' + self.lvm2_ver + '.tgz'
    	
    	return os.system('/usr/bin/wget %s -O %s/distfiles/LVM2.%s.tgz %s' % (lvm2_url, utils.get_portdir(self.temp), self.lvm2_ver, self.verbose['std']))
    
    def extract(self):
    	"""
    	lvm2 tarball extraction routine
    
    	@return: bool
    	"""
    	print green(' * ') + '... lvm2.extract'

    	os.system('tar xvfz %s/distfiles/LVM2.%s.tgz -C %s %s' % (utils.get_portdir(self.temp), self.lvm2_ver, self.temp['work'], self.verbose['std']))
    
    def configure(self):
    	"""
    	lvm2 Makefile interface to configure
    
    	@return: bool
    	"""
    	print green(' * ') + '... lvm2.configure'
    	utils.chgdir(self.lvm2_tmp)
    	return os.system('LDFLAGS=-L%s/device-mapper/lib \
    			CFLAGS=-I%s/device-mapper/include \
    			CPPFLAGS=-I%s/device-mapper/include \
    			./configure --enable-static_link --prefix=%s/lvm %s' % (self.temp['work'], self.temp['work'], self.temp['work'], self.temp['work'], self.verbose['std']))
    
    def compile(self):
    	"""
    	lvm2 Makefile interface to make
    
    	@return: bool
    	"""
    	print green(' * ') + '... lvm2.compile'
    	utils.chgdir(self.lvm2_tmp)
    	return os.system('%s %s CC="%s" LD="%s" AS="%s" %s' % (self.master_config['DEFAULT_UTILS_MAKE'], \
    								self.master_config['DEFAULT_MAKEOPTS'], \
    								self.master_config['DEFAULT_UTILS_CC'], \
    								self.master_config['DEFAULT_UTILS_LD'], \
    								self.master_config['DEFAULT_UTILS_AS'], \
    								self.verbose['std']))
    def install(self):
    	"""
    	Install lvm2
    
    	@return: bool
    	"""
    	print green(' * ') + '... lvm2.install'
    	utils.chgdir(self.lvm2_tmp)
    
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
    	print green(' * ') + '... lvm2.strip'
    
    	utils.chgdir(self.lvm2_tmp)

    	return os.system('strip tools/lvm.static ')
    
    def compress(self):
    	"""
    	lvm.static compression routine
    
    	@return: bool
    	"""
    	print green(' * ') + '... lvm2.compress'
    	utils.chgdir(self.lvm2_tmp)
    
    #	return os.system('tar -cj -f %s tools/lvm.static %s' % (temp['cache']+'/lvm.static-'+master_config['lvm2-version']+'.tar.bz2', verbose))
        return os.system('bzip2 tools/lvm.static')
#    	return os.system('bzip2 tools/lvm')
    
    def cache(self):
    	"""
    	lvm.static tarball cache routine
    
    	@return: bool
    	"""
    	print green(' * ') + '... lvm2.cache'
    	utils.chgdir(self.lvm2_tmp)
    	mvv = ''
    	if self.verbose['set'] is '': mvv = '-v'

    	return os.system('mv %s tools/lvm.static.bz2 %s/lvm.static-%s.bz2' % (mvv, self.temp['cache'], self.master_config['lvm2-version']))

