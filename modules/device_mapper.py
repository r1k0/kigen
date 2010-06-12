import os
import sys
from stdout import green, turquoise, white, red, yellow
import utils

def download(dm_ver, temp, verbose):
	"""
	Download device-mapper tarball

	@arg: string
	@arg: string
	@return: bool
	"""
	print green(' * ') + '... device_mapper.download'
	# TODO: get GENTOO_MIRRORS from portageq (better if I could import a portage module)
	device_mapper_url = 'http://ftp.snt.utwente.nl/pub/os/linux/gentoo/distfiles/device-mapper.' + str(dm_ver) + '.tgz'

	return os.system('/usr/bin/wget %s -O %s/distfiles/device-mapper.%s.tgz %s' % (device_mapper_url, utils.get_portdir(temp), str(dm_ver), verbose['std']))

def extract(dm_ver, temp, verbose):
	"""
	Extract device-mapper tarball

	@arg: string
	@arg: dict
	@arg: string
	@return: bool
	"""
	print green(' * ') + '... device_mapper.extract'
	os.system('tar xvfz %s/distfiles/device-mapper.%s.tgz -C %s %s' % (utils.get_portdir(temp), str(dm_ver), temp['work'], verbose['std']))

# device-mapper building functions
def configure(dmtmp, master_config, temp, verbose):
	"""
	Configure device-mapper source code

	@arg: string
	@arg: dict
	@arg: dict
	@arg: string
	@return: bool
	"""
	print green(' * ') + '... device_mapper.configure'
	utils.chgdir(dmtmp)

	return os.system('./configure --prefix=%s/device-mapper --enable-static_link --disable-selinux %s' % (temp['work'], verbose['std']))

def compile(dmtmp, master_config, verbose):
	"""
	Compile device-mapper source code

	@arg: string
	@arg: dict
	@arg: string
	@return: bool
	"""
	print green(' * ') + '... device_mapper.compile'
	utils.chgdir(dmtmp)

	return os.system('%s %s CC="%s" LD="%s" AS="%s" %s' % (master_config['DEFAULT_UTILS_MAKE'], \
								master_config['DEFAULT_MAKEOPTS'], \
								master_config['DEFAULT_UTILS_CC'], \
								master_config['DEFAULT_UTILS_LD'], \
								master_config['DEFAULT_UTILS_AS'], \
								verbose))

def install(dmtmp, master_config, verbose):
	"""
	Install device-mapper

	@arg: string
	@arg: dict
	@arg: string
	@return: bool
	"""
	print green(' * ') + '... device_mapper.install'
	utils.chgdir(dmtmp)

	return os.system('%s %s CC="%s" LD="%s" AS="%s" install %s' % (master_config['DEFAULT_UTILS_MAKE'], \
						master_config['DEFAULT_MAKEOPTS'], \
						master_config['DEFAULT_UTILS_CC'], \
						master_config['DEFAULT_UTILS_LD'], \
						master_config['DEFAULT_UTILS_AS'], \
						verbose))

def strip(master_config, temp):
	"""
	Strip dmsetup binary

	@arg: dict
	@arg: dict
	@return: bool
	"""
	print green(' * ') + '... device_mapper.strip'
	utils.chgdir(temp['work'])

	return os.system('strip %s/device-mapper/sbin/dmsetup' % (temp['work']))

def compress(master_config, temp, verbose):
	"""
	Compress dmsetup binary

	@arg: dict
	@arg: dict
	@arg: string
	@return: bool
	"""
	print green(' * ') + '... device_mapper.compress'
	utils.chgdir(temp['work'])

#	return os.system('tar -jcf %s device-mapper %s' % (temp['cache']+'/dmsetup-device-mapper-'+master_config['dm_ver']+'.tar.bz2', temp['work'], verbose))
	return os.system('tar -jcf %s device-mapper %s' % (temp['cache']+'/dmsetup-device-mapper-'+master_config['device-mapper-version']+'.tar.bz2', verbose))

def cache(dmtmp, master_config, temp, verbose): # TODO pass arch? should we add 'arch' to blkid-device_mapper-%s.bz2? genkernel seems to do so
	"""
	Cache compressed dmsetup binary

	@arg: string
	@arg: dict
	@arg: dict
	@arg: string
	@return: bool
	"""
	print green(' * ') + '... device_mapper.cache'
	utils.chgdir(dmtmp)
	mvv = ''
	if verbose is '': mvv = '-v'

	return os.system('mv %s %s %s/device-mapper-%s.tar.bz2' % (mvv, temp['cache']+'/dmsetup-device-mapper-'+master_config['device-mapper-version']+'.tar.bz2', temp['cache'], master_config['device-mapper-version']))
	# TODO: use os.file.cp or smthg like that

# device_mapper sequence
def build_sequence(master_config, temp, verbose):
	"""
	device-mapper build sequence

	@arg: dict
	@arg: dict
	@arg: string
	@return: bool
	"""
	zero = int('0')
	ret = True

	if os.path.isfile('%s/distfiles/device-mapper.%s.tgz' % (utils.get_portdir(temp), str(master_config['device-mapper-version']))) is not True:
		ret = download(master_config['device-mapper-version'], temp, verbose)
		if ret is not zero:
			print red('ERR: ')+'initramfs.device_mapper.download() failed'
			sys.exit(2)

	ret = extract(master_config['device-mapper-version'], temp, verbose)
	ret = zero # grr, tar thing to not return 0 when success

	ret = configure(temp['work'] + '/device-mapper.' + master_config['device-mapper-version'], master_config, temp, verbose)
	if ret is not zero:
		print red('ERR: ')+'initramfs.device_mapper.configure() failed'
		sys.exit(2)

	ret = compile(temp['work'] + '/device-mapper.' + master_config['device-mapper-version'], master_config, verbose)
	if ret is not zero:
		print red('ERR: ')+'initramfs.device_mapper.compile() failed'
		sys.exit(2)

	ret = install(temp['work'] + '/device-mapper.' + master_config['device-mapper-version'], master_config, verbose)
	if ret is not zero:
		print red('ERR: ')+'initramfs.device_mapper.install() failed'
		sys.exit(2)
# TODO remove manpage rm -rf %s/device-mapper/man % temp['work']
	ret = strip(master_config, temp)
	if ret is not zero:
		print red('ERR: ')+'initramfs.device_mapper.strip() failed'
		sys.exit(2)

	ret = compress(master_config, temp, verbose)
	if ret is not zero:
		print red('ERR: ')+'initramfs.device_mapper.compress() failed'
		sys.exit(2)

	ret = cache(temp['work'] + '/device-mapper.' + master_config['device-mapper-version'], master_config, temp, verbose)
	if ret is not zero:
		print red('ERR: ')+'initramfs.device_mapper.compress() failed'
		sys.exit(2)

	return ret
