import os
import sys
from stdout import green, turquoise, white, red, yellow
import utils

def download(lvm2_ver, temp, verbose):
	"""
	lvm2 tarball download routine

	@arg lvm2_ver	string
	@arg verbose	string

	@return: bool
	"""
	print green(' * ') + '... lvm2.download'
	lvm2_url = 'ftp://sources.redhat.com/pub/lvm2/' + \
				'/LVM2.' + str(lvm2_ver) + '.tgz'
	
	return os.system('/usr/bin/wget %s -O %s/distfiles/LVM2.%s.tgz %s' % (lvm2_url, utils.get_portdir(temp), str(lvm2_ver), verbose['std']))

def extract(lvm2_ver, temp, verbose):
	"""
	lvm2 tarball extraction routine

	@arg lvm2_ver	string
	@arg temp	dict
	@arg verbose	string

	@return: bool
	"""
	print green(' * ') + '... lvm2.extract'
	os.system('tar xvfz %s/distfiles/LVM2.%s.tgz -C %s %s' % (utils.get_portdir(temp), str(lvm2_ver), temp['work'], verbose['std']))

# LVM2 building functions
def configure(temp, master_config, verbose):
	"""
	lvm2 Makefile interface to configure

	@arg temp		dict
	@arg master_config	dict
	@arg verbose		string

	@return: bool
	"""
	print green(' * ') + '... lvm2.configure'
	utils.chgdir(temp['work']+'/LVM2.'+master_config['lvm2-version'])
	return os.system('LDFLAGS=-L%s/device-mapper/lib \
			CFLAGS=-I%s/device-mapper/include \
			CPPFLAGS=-I%s/device-mapper/include \
			./configure --enable-static_link --prefix=%s/lvm %s' % (temp['work'], temp['work'], temp['work'], temp['work'], verbose['std']))

def compile(temp, master_config, verbose):
	"""
	lvm2 Makefile interface to make

	@arg temp		dict
	@arg master_config	dict
	@arg verbose		string
	@return: bool
	"""
	print green(' * ') + '... lvm2.compile'
	utils.chgdir(temp['work']+'/LVM2.'+master_config['lvm2-version'])
	return os.system('%s %s CC="%s" LD="%s" AS="%s" %s' % (master_config['DEFAULT_UTILS_MAKE'], \
								master_config['DEFAULT_MAKEOPTS'], \
								master_config['DEFAULT_UTILS_CC'], \
								master_config['DEFAULT_UTILS_LD'], \
								master_config['DEFAULT_UTILS_AS'], \
								verbose['std']))
def install(temp, master_config, verbose):
	"""
	Install lvm2

	@arg temp		dict
	@arg master_config	dict
	@arg verbose		string

	@return: bool
	"""
	print green(' * ') + '... lvm2.install'
	utils.chgdir(temp['work']+'/LVM2.'+master_config['lvm2-version'])

	return os.system('%s %s CC="%s" LD="%s" AS="%s" install %s' % (master_config['DEFAULT_UTILS_MAKE'], \
									master_config['DEFAULT_MAKEOPTS'], \
									master_config['DEFAULT_UTILS_CC'], \
									master_config['DEFAULT_UTILS_LD'], \
									master_config['DEFAULT_UTILS_AS'], \
									verbose['std']))

def strip(master_config, temp):
	"""
	lvm.static strip binary routine

	@arg master_config	dict
	@arg temp		dict

	@return: bool
	"""
	print green(' * ') + '... lvm2.strip'

	utils.chgdir(temp['work']+'/LVM2.'+master_config['lvm2-version'])
	return os.system('strip tools/lvm.static ')

def compress(master_config, temp, verbose):
	"""
	lvm.static compression routine

	@arg master_config	dict
	@arg temp		dict

	@return: bool
	"""
	print green(' * ') + '... lvm2.compress'
	utils.chgdir(temp['work']+'/LVM2.'+master_config['lvm2-version'])

#	return os.system('tar -cj -f %s tools/lvm.static %s' % (temp['cache']+'/lvm.static-'+master_config['lvm2-version']+'.tar.bz2', verbose))
	return os.system('bzip2 tools/lvm.static')

def cache(master_config, temp, verbose): # TODO pass arch? should we add 'arch' to blkid-lvm2-%s.bz2? genkernel seems to do so
	"""
	lvm.static tarball cache routine

	@arg master_config	dict
	@arg temp		dict
	@arg verbose		string

	@return: bool
	"""
	print green(' * ') + '... lvm2.cache'
	utils.chgdir(temp['work']+'/LVM2.'+master_config['lvm2-version'])
	mvv = ''
	if verbose is '': mvv = '-v'
	return os.system('mv %s tools/lvm.static.bz2 %s/lvm.static-%s.bz2' % (mvv, temp['cache'], master_config['lvm2-version']))
	# TODO: use os.file.cp or smthg like that

# lvm2 sequence
def build_sequence(master_config, temp, verbose):
	"""
	lvm2 build sequence

	@arg master_config	dict
	@arg temp		dict
	@arg verbose		string

	@return: bool
	"""
	zero = int('0')
	ret = True
	
	if os.path.isfile('%s/distfiles/LVM2.%s.tgz' % (utils.get_portdir(temp), str(master_config['lvm2-version']))) is not True:
		ret = download(master_config['lvm2-version'], temp, verbose)
		if ret is not True:
			print red('ERR: ')+'initramfs.lvm2.download() failed'
			sys.exit(2)

	ret = extract(master_config['lvm2-version'], temp, verbose)
	ret = True # grr, tar thing to not return 0 when success

	ret = configure(temp, master_config, verbose)
	if ret is not zero: 
		print red('ERR') + ': ' + 'initramfs.lvm2.configure() failed'
		sys.exit(2)

	ret = compile(temp, master_config, verbose)
	if ret is not zero:
		print red('ERR') + ': ' +'initramfs.lvm2.compile() failed'
		sys.exit(2)

	ret = install(temp, master_config, verbose)
	if ret is not zero:
		print red('ERR') + ': ' +'initramfs.lvm2.install() failed'
		sys.exit(2)

	ret = strip(master_config, temp)
	if ret is not zero:
		print red('ERR') + ': ' +'initramfs.lvm2.strip() failed'
		sys.exit(2)

	ret = compress(master_config, temp, verbose)
	if ret is not zero:
		print red('ERR') + ': ' +'initramfs.lvm2.compress() failed'
		sys.exit(2)

	ret = cache(master_config, temp, verbose)
	if ret is not zero:
		print red('ERR') + ': ' +'initramfs.lvm2.compress() failed'
		sys.exit(2)

	return ret
