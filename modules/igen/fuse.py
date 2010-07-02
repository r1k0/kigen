import os
import sys
import utils
from stdout import green, turquoise, white, red, yellow

def download(fuse_ver, temp, verbose):
	"""
	Download fuse tarball

	@arg: string
	@arg: string
	@return: bool
	"""
	print green(' * ') + '... fuse.download'
	# TODO: get GENTOO_MIRRORS from portageq (better if I could import a portage module)
	fuse_url = 'http://sourceforge.net/projects/fuse/files/fuse-2.X/'+str(fuse_ver)+'/fuse-'+str(fuse_ver)+'.tar.gz/download'

	return os.system('/usr/bin/wget %s -O %s/distfiles/fuse-%s.tar.gz %s' % (fuse_url, utils.get_portdir(temp), str(fuse_ver), verbose['std']))

def extract(fuse_ver, temp, verbose):
	"""
	Extract fuse tarball

	@arg: string
	@arg: dict
	@arg: string
	@return: bool
	"""
	print green(' * ') + '... fuse.extract'
	os.system('tar xvfz %s/distfiles/fuse-%s.tar.gz -C %s %s' % (utils.get_portdir(temp), str(fuse_ver), temp['work'], verbose['std']))

# fuse building functions
def configure(fusetmp, master_config, temp, verbose):
	"""
	Configure fuse source code

	@arg: string
	@arg: dict
	@arg: dict
	@arg: string
	@return: bool
	"""
	print green(' * ') + '... fuse.configure'
	utils.chgdir(fusetmp)

	return os.system('./configure --disable-kernel-module --disable-example %s' %  verbose['std'])

def compile(fusetmp, master_config, verbose):
	"""
	Compile fuse source code

	@arg: string
	@arg: dict
	@arg: string
	@return: bool
	"""
	print green(' * ') + '... fuse.compile'
	utils.chgdir(fusetmp)

	return os.system('%s %s CC="%s" LD="%s" AS="%s" %s' % (master_config['DEFAULT_UTILS_MAKE'], \
								master_config['DEFAULT_MAKEOPTS'], \
								master_config['DEFAULT_UTILS_CC'], \
								master_config['DEFAULT_UTILS_LD'], \
								master_config['DEFAULT_UTILS_AS'], \
								verbose['std']))
#def install(fusetmp, master_config, verbose):
#	"""
#	Install fuse
#
#        @arg: string
#        @arg: dict
#        @arg: string
#        @return: bool
#	"""
#	print ' * ' + '... fuse.install'
#	utils.chgdir(fusetmp)
#
#	return os.system('%s %s CC="%s" LD="%s" AS="%s" install %s' % (master_config['DEFAULT_UTILS_MAKE'], \
#						master_config['DEFAULT_MAKEOPTS'], \
#						master_config['DEFAULT_UTILS_CC'], \
#						master_config['DEFAULT_UTILS_LD'], \
#						master_config['DEFAULT_UTILS_AS'], \
#
#						verbose))
#def strip(master_config, temp):
#	"""
#	Strip dmsetup binary
#
#        @arg: dict
#        @arg: dict
#        @return: bool
#	"""
#	print ' * ' + '... fuse.strip'
#	utils.chgdir(temp['work'])
#
#	return os.system('strip %s/fuse/sbin/dmsetup' % (temp['work']))
#
#def compress(master_config, temp, verbose):
#	"""
#	Compress dmsetup binary
#
#        @arg: dict
#        @arg: dict
#        @arg: string
#        @return: bool
#	"""
#	print ' * ' + '... fuse.compress'
#	utils.chgdir(temp['work'])
#
#	return os.system('tar -jcf %s %s %s' % (temp['cache']+'/fuse-dircache-'+master_config['fuse_ver']+'.tar.bz2', temp['work']+'/fuse-'+master_config['fuse_ver'], verbose))

def cache(fusetmp, master_config, temp, verbose): # TODO pass arch? should we add 'arch' to blkid-fuse-%s.bz2? genkernel seems to do so
	"""
	Cache compressed dmsetup binary

        @arg: string
        @arg: dict
	@arg: dict
        @arg: string
        @return: bool
	"""
	print green(' * ') + '... fuse.cache'
	utils.chgdir(temp['work'])
	mvv = ''
	if verbose['set'] is '': mvv = '-v'

	return os.system('tar -jcf %s %s %s' % (temp['cache']+'/fuse-dircache-'+master_config['fuse_ver']+'.tar.bz2', 'fuse-'+master_config['fuse_ver'], verbose['std']))
#	return os.system('mv %s %s %s/fuse-driname-%s.tar.bz2' % (mvv, temp['cache']+'/fuse-dircache-'+master_config['fuse_ver']+'.tar.bz2', temp['cache'], master_config['fuse_ver']))
	# TODO: use os.file.cp or smthg like that

# fuse sequence
def build_sequence(master_config, temp, verbose):
	"""
	fuse build sequence

	@arg: dict
	@arg: dict
	@arg: string
	@return: bool
	"""
	zero = int('0')
	ret = True

	if os.path.isfile('%s/distfiles/fuse-%s.tar.gz' % (utils.get_portdir(temp), str(master_config['fuse_ver']))) is not True:
		ret = download(master_config['fuse_ver'], temp, verbose)
		if ret is not zero:
			print red('error: ')+'initramfs.fuse.download() failed'
			sys.exit(2)

	ret = extract(master_config['fuse_ver'], temp, verbose)
	ret = zero # grr, tar thing to not return 0 when success

	ret = configure(temp['work'] + '/fuse-' + master_config['fuse_ver'], master_config, temp, verbose)
	if ret is not zero:
		print red('error: ')+'initramfs.fuse.configure() failed'
		sys.exit(2)

	ret = compile(temp['work'] + '/fuse-' + master_config['fuse_ver'], master_config, verbose)
	if ret is not zero:
		print red('error: ')+'initramfs.fuse.compile() failed'
		sys.exit(2)

#	ret = install(temp['work'] + '/fuse-' + master_config['fuse_ver'], master_config, verbose)
#	if ret is not zero:
#		print red('error: ')+'initramfs.fuse.install() failed'
#		sys.exit(2)
#
#	ret = strip(master_config, temp)
#	if ret is not zero:
#		print red('error: ')+'initramfs.fuse.strip() failed'
#		sys.exit(2)
#
#	ret = compress(master_config, temp, verbose)
#	if ret is not zero:
#		print red('error: ')+'initramfs.fuse.compress() failed'
#		sys.exit(2)

	ret = cache(temp['work'] + '/fuse-' + master_config['fuse_ver'], master_config, temp, verbose)
	if ret is not zero:
		print red('error: ')+'initramfs.fuse.compress() failed'
		sys.exit(2)

	return ret
