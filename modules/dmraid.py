import os
import sys
color = os.getenv("GENKI_STD_COLOR")
if color == '0':
	from portage.output import *
else:
	from nocolor import green, turquoise, white, red, yellow
import utils

def download(dmraid_ver, quiet):
	"""
	Download dmraid tarball

	@arg: string
	@arg: string
	@return: bool
	"""
	print green(' * ') + '... dmraid.download'
	# TODO: get GENTOO_MIRRORS from portageq (better if I could import a portage module)
	dmraid_url = 'http://people.redhat.com/~heinzm/sw/dmraid/src/dmraid-' + str(dmraid_ver) + '.tar.bz2'

	return os.system('/usr/bin/wget %s -O %s/distfiles/dmraid-%s.tar.bz2 %s' % (dmraid_url, utils.get_portdir(), str(dmraid_ver), quiet))

def extract(dmraid_ver, temp, quiet):
	"""
	Extract dmraid tarball

	@arg: string
	@arg: dict
	@arg: string
	@return: bool
	"""
	print green(' * ') + '... dmraid.extract'
	os.system('tar xvfj %s/distfiles/dmraid-%s.tar.bz2 -C %s %s' % (utils.get_portdir(), str(dmraid_ver), temp['work'], quiet))

# dmraid building functions
def configure(dmraidtmp, master_config, temp, quiet):
	"""
	Configure device-mapper source code
	
	@arg: string
	@arg: dict
	@arg: dict
	@arg: string
	@return: bool
	"""
	print green(' * ') + '... dmraid.configure'
	utils.chgdir(dmraidtmp)
	
	return os.system('LDFLAGS=-L%s/device-mapper/lib \
				CFLAGS=-I%s/device-mapper/include \
				CPPFLAGS=-I%s/device-mapper/include \
				./configure --enable-static_link --prefix=%s/dmraid %s' % (temp['work'], temp['work'], temp['work'], temp['work'], quiet))

def compile(dmraidtmp, master_config, quiet):
	"""
	Compile dmraid source code

	@arg: string
	@arg: dict
	@arg: string
	@return: bool
	"""
	print green(' * ') + '... dmraid.compile'
	utils.chgdir(dmraidtmp)
	return os.system('%s %s' % (master_config['DEFAULT_UTILS_MAKE'], \
					quiet))

def strip(master_config, temp):
	"""
	Strip dmraidsetup binary

	@arg: dict
	@arg: dict
	@return: bool
	"""
	print green(' * ') + '... dmraid.strip'
#	utils.chgdir(temp['work'])

	return os.system('strip %s/dmraid/%s/tools/dmraid.static' % (temp['work'], master_config['dmraid_ver']))

def compress(master_config, temp, quiet):
	"""
	Compress dmraidsetup binary

	@arg: dict
	@arg: dict
	@arg: string
	@return: bool
	"""
	print green(' * ') + '... dmraid.compress'
#	utils.chgdir(temp['work'])

	return os.system('bzip2 -f %s/dmraid/%s/tools/dmraid.static' % (temp['work'], master_config['dmraid_ver']))

def cache(dmraidtmp, master_config, temp, quiet): # TODO pass arch? should we add 'arch' to blkid-dmraid-%s.bz2? genkernel seems to do so
	"""
	Cache compressed dmraidsetup binary

	@arg: string
	@arg: dict
	@arg: dict
	@arg: string
	@return: bool
	"""
	print green(' * ') + '... dmraid.cache'
	utils.chgdir(dmraidtmp)
	mvv = ''
	if quiet is '': mvv = '-v'

	return os.system('mv %s %s/dmraid/%s/tools/dmraid.static.bz2 %s/dmraid.static-%s.bz2' % (mvv, \
				temp['work'], \
				master_config['dmraid_ver'], \
				temp['cache'],      \
				master_config['dmraid_ver']))
	# TODO: use os.file.cp or smthg like that

# dmraid sequence
def build_sequence(master_config, selinux, temp, quiet):
	"""
	dmraid build sequence

	@arg: dict
	@arg: bool
	@arg: dict
	@arg: string
	@return: bool
	"""
	zero = int('0')
	ret = True

	if os.path.isfile('%s/distfiles/dmraid-%s.tar.bz2' % (utils.get_portdir(), str(master_config['dmraid_ver']))) is not True:
		ret = download(master_config['dmraid_ver'], quiet)
		if ret is not zero:
			print red('ERR: ')+'initramfs.dmraid.download() failed'
			sys.exit(2)

	ret = extract(master_config['dmraid_ver'], temp, quiet)
	ret = zero # grr, tar thing to not return 0

	ret = configure(temp['work'] + '/dmraid/' + master_config['dmraid_ver'], master_config, temp, quiet)
	if ret is not zero:
		print red('ERR: ')+'initramfs.dmraid.configure() failed'
		sys.exit(2)

	# we don't have selinux by default
	utils.chgdir(temp['work'] + '/dmraid/' + master_config['dmraid_ver'])
	os.system('sed -i tools/Makefile -e "s|DMRAIDLIBS += -lselinux||g"')

	# we want selinux
	if selinux is True:
		#TODO check we have selinux
		#if check file lib for selinux:
		os.system('echo "DMRAIDLIBS += -lselinux -lsepol" >> tools/Makefile')
		#else fail

	ret = compile(temp['work'] + '/dmraid/' + master_config['dmraid_ver'], master_config, quiet)
	if ret is not zero:
		print red('ERR: ')+'initramfs.dmraid.compile() failed'
		sys.exit(2)

# TODO remove manpage rm -rf %s/dmraid/man % temp['work']

	ret = strip(master_config, temp)
	if ret is not zero:
		print red('ERR: ')+'initramfs.dmraid.strip() failed'
		sys.exit(2)

	ret = compress(master_config, temp, quiet)
	if ret is not zero:
		print red('ERR: ')+'initramfs.dmraid.compress() failed'
		sys.exit(2)

	ret = cache(temp['work'] + '/dmraid/' + master_config['dmraid_ver'], master_config, temp, quiet)
	if ret is not zero:
		print red('ERR: ')+'initramfs.dmraid.compress() failed'

	return ret
