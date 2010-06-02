import os
import sys
from stdout import green, turquoise, white, red, yellow
import utils

def download(unionfs_fuse_ver, quiet):
	"""
	Download unionfs-fuse tarball

	@arg unionfs_fuse_ver	string
	@arg quiet		string

	@return: bool
	"""
	print green(' * ') + '... unionfs_fuse.download'
	# TODO: get GENTOO_MIRRORS from portageq (better if I could import a portage module)
	unionfs_fuse_url = 'http://podgorny.cz/unionfs-fuse/releases/unionfs-fuse-' + str(unionfs_fuse_ver) + '.tar.bz2'

	return os.system('/usr/bin/wget %s -O %s/distfiles/unionfs-fuse-%s.tar.bz2 %s' % (unionfs_fuse_url, utils.get_portdir(), str(unionfs_fuse_ver), quiet))

def extract(unionfs_fuse_ver, temp, quiet):
	"""
	Extract unionfs-fuse tarball

	@arg unionfs_fuse_ver	string
	@arg temp		dict
	@arg quiet		string

	@return: bool
	"""
	print green(' * ') + '... unionfs_fuse.extract'
	os.system('tar xvfj %s/distfiles/unionfs-fuse-%s.tar.bz2 -C %s %s' % (utils.get_portdir(), str(unionfs_fuse_ver), temp['work'], quiet))

# unionfs_fuse building functions
#def configure(unionfs_fuse_tmp, master_config, temp, quiet):
#	"""
#	Configure device-mapper source code
#	
#	@arg: string
#	@arg: dict
#	@arg: dict
#	@arg: string
#	@return: bool
#	"""
#	print ' * ' + '... unionfs_fuse.configure'
#	utils.chgdir(unionfs_fuse_tmp)
#	
#	return os.system('LDFLAGS=-L%s/device-mapper/lib \
#                        CFLAGS=-I%s/device-mapper/include \
#                        CPPFLAGS=-I%s/device-mapper/include \
#                        ./configure --enable-static_link --prefix=%s/unionfs_fuse %s' % (temp['work'], temp['work'], temp['work'], temp['work'], quiet))

def compile(unionfs_fuse_tmp, master_config, quiet):
	"""
	Compile unionfs_fuse source code

	@arg unionfs_fuse_tmp	string
	@arg master_config	dict
	@arg quiet		string

	@return: bool
	"""
	print green(' * ') + '... unionfs_fuse.compile'
	utils.chgdir(unionfs_fuse_tmp)

	return os.system('%s %s' % (master_config['DEFAULT_UTILS_MAKE'], quiet))

def strip(master_config, temp):
	"""
	Strip unionfs_fuse binary 

	@arg master_config	dict
	@arg temp		dict

	@return: bool
	"""
	print green(' * ') + '... unionfs_fuse.strip'
#	utils.chgdir(temp['work'])

	return os.system('strip %s/unionfs-fuse-%s/src/unionfs' % (temp['work'], master_config['unionfs_fuse_ver']))

def compress(master_config, temp, quiet):
	"""
	Compress unionfs_fusesetup binary

	@argd master_config	dict
	@arg temp		dict
	@arg quiet		string

	@return: bool
	"""
	print green(' * ') + '... unionfs_fuse.compress'
#	utils.chgdir(temp['work'])

	return os.system('bzip2 -f %s/unionfs-fuse-%s/src/unionfs' % (temp['work'], master_config['unionfs_fuse_ver']))

def cache(unionfs_fuse_tmp, master_config, temp, quiet): # TODO pass arch? should we add 'arch' to blkid-unionfs_fuse-%s.bz2? genkernel seems to do so
	"""
	Cache compressed unionfs_fusesetup binary

	@arg unionfs_fuse_tmp	string
	@arg master_config	dict
	@arg temp		dict
	@arg quiet		string

	@return: bool
	"""
	print green(' * ') + '... unionfs_fuse.cache'
	utils.chgdir(unionfs_fuse_tmp)
	mvv = ''
	if quiet is '': mvv = '-v'

	return os.system('mv %s %s/unionfs-fuse-%s/src/unionfs.bz2 %s/unionfs-fuse.static-%s.bz2' % (mvv, \
				temp['work'], \
				master_config['unionfs_fuse_ver'], \
				temp['cache'],      \
				master_config['unionfs_fuse_ver']))
	# TODO: use os.file.cp or smthg like that

# unionfs_fuse sequence
def build_sequence(master_config, temp, quiet):
	"""
	unionfs_fuse build sequence

	@arg master_config	dict
	@arg temp		dict
	@arg quiet		string

	@return: bool
	"""
	zero = int('0')
	ret = True

	if os.path.isfile('%s/distfiles/unionfs-fuse-%s.tar.bz2' % (utils.get_portdir(), str(master_config['unionfs_fuse_ver']))) is not True:
		ret = download(master_config['unionfs_fuse_ver'], quiet)
		if ret is not zero:
			print red('ERR: ')+'initramfs.unionfs_fuse.download() failed'
			sys.exit(2)

	ret = extract(master_config['unionfs_fuse_ver'], temp, quiet)
	ret = zero # grr, tar thing to not return 0

#	ret = configure(temp['work'] + '/unionfs_fuse/' + master_config['unionfs_fuse_ver'], master_config, temp, quiet)
#	if ret is not zero:
#		print red('ERR: ')+'initramfs.unionfs_fuse.configure() failed'
#		sys.exit(2)

	# add fuse lib path
	os.system('echo "CPPFLAGS += -static -I%s/include -L%s/lib/.libs" >> %s' % (temp['work'] + '/fuse-' + master_config['fuse_ver'], temp['work'] + '/fuse-' + master_config['fuse_ver'], temp['work'] + '/unionfs-fuse-' + master_config['unionfs_fuse_ver']+'/Makefile'))
	os.system('echo "CPPFLAGS += -static -I%s/include -L%s/lib/.libs" >> %s' % (temp['work'] + '/fuse-' + master_config['fuse_ver'], temp['work'] + '/fuse-' + master_config['fuse_ver'], temp['work'] + '/unionfs-fuse-' + master_config['unionfs_fuse_ver']+'/src/Makefile'))
	os.system('echo "LIB += -static -L%s/lib/.libs -ldl -lrt" >> %s' % (temp['work'] + '/fuse-' + master_config['fuse_ver'], temp['work'] + '/unionfs-fuse-' + master_config['unionfs_fuse_ver']+'/Makefile'))
	os.system('echo "LIB += -static -L%s/lib/.libs -ldl -lrt" >> %s' % (temp['work'] + '/fuse-' + master_config['fuse_ver'], temp['work'] + '/unionfs-fuse-' + master_config['unionfs_fuse_ver']+'/src/Makefile'))

	ret = compile(temp['work'] + '/unionfs-fuse-' + master_config['unionfs_fuse_ver'], master_config, quiet)
	if ret is not zero:
		print red('ERR: ')+'initramfs.unionfs_fuse.compile() failed'
		sys.exit(2)

# TODO remove manpage rm -rf %s/unionfs_fuse/man % temp['work']

	ret = strip(master_config, temp)
	if ret is not zero:
		print red('ERR: ')+'initramfs.unionfs_fuse.strip() failed'
		sys.exit(2)

	ret = compress(master_config, temp, quiet)
	if ret is not zero:
		print red('ERR: ')+'initramfs.unionfs_fuse.compress() failed'
		sys.exit(2)

	ret = cache(temp['work'] + '/unionfs-fuse-' + master_config['unionfs_fuse_ver'], master_config, temp, quiet)
	if ret is not zero:
		print red('ERR: ')+'initramfs.unionfs_fuse.compress() failed'

	return ret
