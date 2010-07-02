import os
import sys
from stdout import green, turquoise, white, red, yellow
import utils

def download(iscsi_ver, temp, quiet):
	"""
	Download iscsi tarball

	@arg: string
	@arg: string
	@return: bool
	"""
	print green(' * ') + '... iscsi.download'
	# TODO: get GENTOO_MIRRORS from portageq (better if I could import a portage module)
	iscsi_url = 'http://www.open-iscsi.org/bits/open-iscsi-' + str(iscsi_ver) + '.tar.gz'

	return os.system('/usr/bin/wget %s -O %s/distfiles/open-iscsi-%s.tar.gz %s' % (iscsi_url, utils.get_portdir(temp), str(iscsi_ver), quiet))

def extract(iscsi_ver, temp, quiet):
	"""
	Extract iscsi tarball

	@arg: string
	@arg: dict
	@arg: string
	@return: none because of tar
	"""
	print green(' * ') + '... iscsi.extract'
	os.system('tar xvfz %s/distfiles/open-iscsi-%s.tar.gz -C %s %s' % (utils.get_portdir(temp), str(iscsi_ver), temp['work'], quiet))

# iscsi building functions
def compile(iscsitmp, master_config, quiet):
	"""
	Compile iscsi source code

	@arg: string
	@arg: dict
	@arg: string
	@return: bool
	"""
	print green(' * ') + '... iscsi.compile'
	utils.chgdir(iscsitmp)

	return os.system('%s user %s' % (master_config['DEFAULT_UTILS_MAKE'], \
					quiet))

def strip(master_config, temp):
	"""
	Strip iscsisetup binary

	@arg: dict
	@arg: dict
	@return: bool
	"""
	print green(' * ') + '... iscsi.strip'
	utils.chgdir(temp['work'])

	return os.system('strip %s/open-iscsi-%s/usr/iscsistart' % (temp['work'], master_config['iscsi_ver']))

def compress(master_config, temp, quiet):
	"""
	Compress iscsisetup binary

	@arg: dict
	@arg: dict
	@arg: string
	@return: bool
	"""
	print green(' * ') + '... iscsi.compress'
	utils.chgdir(temp['work'])

	return os.system('bzip2 %s/open-iscsi-%s/usr/iscsistart' % (temp['work'], master_config['iscsi_ver']))

def cache(iscsitmp, master_config, temp, quiet): # TODO pass arch? should we add 'arch' to blkid-iscsi-%s.bz2? genkernel seems to do so
	"""
	Cache compressed iscsisetup binary

	@arg: string
	@arg: dict
	@arg: dict
	@arg: string
	@return: bool
	"""
	print green(' * ') + '... iscsi.cache'
	utils.chgdir(iscsitmp)
	mvv = ''
	if quiet is '': mvv = '-v'

	return os.system('mv %s %s/open-iscsi-%s/usr/iscsistart.bz2 %s/iscsistart-%s.bz2' % (mvv, temp['work'], master_config['iscsi_ver'], temp['cache'], master_config['iscsi_ver']))
	# TODO: use os.file.cp or smthg like that

# iscsi sequence
def build_sequence(master_config, temp, quiet):
	"""
	iscsi build sequence

	@arg: dict
	@arg: dict
	@arg: string
	@return: bool
	"""
	zero = int('0')
	ret = True

	if os.path.isfile('%s/distfiles/open-iscsi-%s.tar.gz' % (utils.get_portdir(temp), str(master_config['iscsi_ver']))) is not True:
		ret = download(master_config['iscsi_ver'], temp, quiet)
		if ret is not zero:
			print red('error: ')+'initramfs.iscsi.download() failed'
			sys.exit(2)

	ret = extract(master_config['iscsi_ver'], temp, quiet)
	ret = zero # grr, tar thing to not return 0

	ret = compile(temp['work'] + '/open-iscsi-' + master_config['iscsi_ver'], master_config, quiet)
	if ret is not zero:
		print red('error: ')+'initramfs.iscsi.compile() failed'
		sys.exit(2)

# TODO remove manpage rm -rf %s/iscsi/man % temp['work']

	ret = strip(master_config, temp)
	if ret is not zero:
		print red('error: ')+'initramfs.iscsi.strip() failed'
		sys.exit(2)

	ret = compress(master_config, temp, quiet)
	if ret is not zero: 
		print red('error: ')+'initramfs.iscsi.compress() failed'
		sys.exit(2)

	ret = cache(temp['work'] + '/open-iscsi-' + master_config['iscsi_ver'], master_config, temp, quiet)
	if ret is not zero: 
		print red('error: ')+'initramfs.iscsi.compress() failed'
		sys.exit(2)

	return ret
