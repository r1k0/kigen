import os
import sys
from stdout import green, turquoise, white, red, yellow
import utils

def download(bb_version, quiet):
	"""
	Busybox tarball download command

	@arg bb_version	string
	@arg quiet 		string
	@return			boot
	"""
	print green(' * ') + '... busybox.download'
	bb_url = 'http://www.busybox.net/downloads/busybox-' + str(bb_version) + '.tar.bz2'
	return os.system('/usr/bin/wget %s -O %s/distfiles/busybox-%s.tar.bz2 %s' % (bb_url, utils.get_portdir(), str(bb_version), quiet))

def extract(bb_version, temp, quiet):
	"""
	Busybox tarball extract command

	@arg bb_version	string
	@arg temp		dict
	@arg quiet 		string
	@return			boot
	"""
	print green(' * ') + '... busybox.extract'
	return os.system('tar xvfj %s/distfiles/busybox-%s.tar.bz2 -C %s %s' % (utils.get_portdir(), str(bb_version), temp['work'], quiet))

# TO BE REMOVED: useless function
#def apply_patches(bb_version, patch_dir, temp, quiet):
#	"""
#	Busybox apply patch routine regardless of version
#
#	@arg: string
#	@arg: string
#	@arg: dict
#	@arg: string
#	@return: bool
#	"""
#	ret = True
#	if os.path.isdir(patch_dir):
#		for filename in os.listdir(patch_dir):
#			if filename.endswith('.diff') or filename.endswith('.patch'):
#				print green(' * ') + '... busybox.apply_patch '+filename
#				for i in  [0, 1, 2, 3, 4, 5] :
#					# FIXME: ret just grab the last value
#					ret = os.system('patch -p%s -f --backup-if-mismatch < "%s" %s' % (i, patch_dir +'/' +filename, quiet))
#		# TODO patch .config too by adding CONFIG_MDSTART=n
##		ret = os.system('echo CONFIG_MDSTART=n >> %s/busybox-%s/.config' % (temp['work'], bb_version))
#	return ret

def copy_config(arch, bbconf, bb_version, libdir, temp, quiet):
	"""
	Busybox copy config file routine

	@arg arch			string
	@arg bbconf		string
	@arg bb_version	string
	@arg bb_version	string
	@arg temp 		dict
	@arg quiet		string
	@return			bool
	"""
	print green(' * ') + '... busybox.copy_config'
	cpv = ''
	if quiet is '': cpv = '-v'
	if bbconf:
		# copy bbconf
		return os.system('cp %s %s %s/busybox-%s/.config' % (cpv, bbconf, temp['work'], bb_version))
	else:
		# copy default
		return os.system('cp %s %s %s/busybox-%s/.config' % (cpv, libdir + '/arch/' + arch + '/busybox.config', temp['work'], bb_version))

def strip(bb_tmp, master_config, temp):
	"""
	Busybox binary strip routine

	@arg: string
	@arg: dict
	@arg: string
	"""
	print green(' * ') + '... busybox.strip'
	utils.chgdir(temp['work'] + '/busybox-' + master_config['bb_ver'])
	return os.system('strip %s/busybox ' % (bb_tmp))

def compress(bb_tmp, master_config, temp): # TODO: pass arch?
	"""
	Busybox binary compression routine

	@arg: string
	@arg: dict
	@arg: string
	@return: bool
	"""
	print green(' * ') + '... busybox.compress'
	utils.chgdir(temp['work'] + '/busybox-' + master_config['bb_ver'])
	return os.system('tar -cj -C %s -f %s/busybox-%s.tar.bz2 busybox .config' % (bb_tmp, temp['work'], master_config['bb_ver']))

def cache(bb_tmp, master_config, temp): # TODO pass arch?
	"""
	Busybox cache tarball routine

	@arg: string
	@arg: dict
	@arg: string
	@return: bool
	"""
	print green(' * ') + '... busybox.cache'
	# TODO: use os.file.cp or smthg like that
	return os.system('mv %s/busybox-%s.tar.bz2  %s/busybox-bin-%s.tar.bz2' % (temp['work'], master_config['bb_ver'], temp['cache'], master_config['bb_ver']))

# busybox building functions
def build_command(master_config, arch, target, quiet):
	"""
	Busybox Makefile bash interface

	@arg: dict
	@arg: string
	@arg: string
	@arg: string
	@return: string
	"""
	command = '%s CC="%s" LD="%s" AS="%s" ARCH="%s" %s %s' % (master_config['UTILS_MAKE'],	\
								master_config['UTILS_CC'],	\
								master_config['UTILS_LD'],	\
								master_config['UTILS_AS'],	\
								arch,				\
								target,				\
								quiet)
	return command

def mrproper(master_config, temp, arch, quiet):
	"""
	Busybox mrproper interface

	@arg: dict
	@arg: dict
	@arg: string
	@arg: string
	@return: bool
	"""
	print green(' * ') + '... busybox.mrproper'
	utils.chgdir(temp['work'] + '/busybox-' + master_config['bb_ver'])
	command = build_command(master_config, arch, 'mrproper', quiet)
	if quiet is '':
		print command
	return os.system(command)

def oldconfig(master_config, temp, arch, quiet):
	"""
	Busybox oldconfig interface

	@arg: dict
	@arg: dict
	@arg: string
	@arg: string
	@return: bool
	"""
	print green(' * ') + '... busybox.oldconfig'
	utils.chgdir(temp['work'] + '/busybox-' + master_config['bb_ver'])
	return os.system('make oldconfig')
	command = build_command(master_config, arch, 'oldconfig', '')
	if quiet is '':
		print command
	return os.system(command)

def allyesconfig(master_config, temp, arch, quiet):
	"""
	Busybox allyesconfig interface

	@arg: dict
	@arg: dict
	@arg: string
	@arg: string
	@return: bool
	"""
	print green(' * ') + '... busybox.allyesconfig'
	utils.chgdir(temp['work'] + '/busybox-' + master_config['bb_ver'])
	command = build_command(master_config, arch, 'allyesconfig', quiet)
	if quiet is '':
		print command
	return os.system(command)

def menuconfig(master_config, temp, arch, quiet):
	"""
	Busybox menuconfig interface

	@arg: dict
	@arg: dict
	@arg: string
	@arg: string
	@return: bool
	"""
	print green(' * ') + '... busybox.menuconfig'
	utils.chgdir(temp['work'] + '/busybox-' + master_config['bb_ver'])
	command = build_command(master_config, arch, 'menuconfig', '')
	if quiet is '':
		print command
	return os.system(command)

def compile(master_config, temp, arch, quiet):
	"""
	Busybox compile interface

	@arg: dict
	@arg: dict
	@arg: string
	@arg: string
	@return: bool
	"""
	print green(' * ') + '... busybox.compile'
	utils.chgdir(temp['work'] + '/busybox-' + master_config['bb_ver'])
	command = build_command(master_config, arch, 'all', quiet)
	if quiet is '':
		print command
	return os.system(command)

#def busybox(master_config, quiet):
#       """
#        Busybox mrproper interface
#
#        @arg: dict
#        @arg: string
#        @return: bool
#        """
#       print ' * ' + '... busybox.busybox'
#   	utils.chgdir('/var/tmp/funkernel/busybox-' + master_config['bb_ver'])
#       return os.system('make busybox')

# busybox sequence
def build_sequence(arch, 			\
				bbconf, 			\
				master_config,		\
				libdir,			\
				temp,			\
				oldConfig,			\
				menuConfig,		\
				allyesConfig,		\
				mrProper,			\
				quiet):
	"""
	Busybox build sequence command

	@arg arch			string
	@arg bbconf		string
	@arg master_config	dict
	@arg libdir		string
	@arg temp 		dict
	@arg oldConfig		bool
	@arg menuConfig	bool
	@arg allYesConfig	bool
	@arg mrProper		bool
	@return			bool
	"""
	ret = zero = int('0')

	if os.path.isfile('%s/distfiles/busybox-%s.tar.bz2' % (utils.get_portdir(), str(master_config['bb_ver']))) is not True:
		ret = download(master_config['bb_ver'], quiet)
		if ret is not zero: 
			print red('ERR')+ ': ' +'initramfs.busybox.download() failed'
			sys.exit(2)

	ret = extract(master_config['bb_ver'], temp, quiet)
	if ret is not zero: 
		print red('ERR')+ ': ' +'initramfs.busybox.extract() failed'
		sys.exit(2)

	ret = copy_config(arch, bbconf, master_config['bb_ver'], libdir, temp, quiet)
	if ret is not zero: 
		print red('ERR')+ ': ' +'initramfs.busybox.copy_config() failed'
		sys.exit(2)

	# customize patches given bb version
	# later versions don't need patches at all :)
#	apply_patches(master_config['bb_ver'], libdir + "/patches/busybox/" + master_config['bb_ver'], temp, quiet)

	if mrProper is True:
		ret = mrproper(master_config, temp, arch, quiet)
		if ret is not zero: 
			print red('ERR')+ ': ' +'initramfs.busybox.mrproper() failed'
			sys.exit(2)

	if allyesConfig is True:
		ret = allyesconfig(master_config, temp, arch, quiet)
		if ret is not zero: 
			print red('ERR')+ ': ' +'initramfs.busybox.allyesconfig() failed'
			sys.exit(2)
	elif oldConfig is True:
		ret = oldconfig(master_config, temp, arch, quiet)
		if ret is not zero:
			print red('ERR')+ ': ' +'initramfs.busybox.oldconfig() failed'
			sys.exit(2)
	if menuConfig is True:
		ret = menuconfig(master_config, temp, arch, quiet)
		if ret is not zero: 
			print red('ERR')+ ': ' +'initramfs.busybox.menuconfig() failed'
			sys.exit(2)

	ret = compile(master_config, temp, arch, quiet)
	if ret is not zero:
		print red('ERR')+ ': ' +'initramfs.busybox.compile() failed'
		sys.exit(2)

	ret = strip(temp['work'] + '/busybox-' + master_config['bb_ver'], master_config, temp)
	if ret is not zero: 
		print red('ERR')+ ': ' +'initramfs.busybox.strip() failed'
		sys.exit(2)

	ret = compress(temp['work'] + '/busybox-' + master_config['bb_ver'], master_config, temp)
	if ret is not zero: 
		print red('ERR')+ ': ' +'initramfs.busybox.compress() failed'
		sys.exit(2)

	ret = cache(temp['work'] + '/busybox-' + master_config['bb_ver'], master_config, temp)
	if ret is not zero: 
		print red('ERR')+ ': ' +'initramfs.busybox.cache() failed'
		sys.exit(2)

	return ret
