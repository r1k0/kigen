import os
import sys
import portage
color = os.getenv("GENKI_STD_COLOR")
if color == '0':
	from portage.output import *
else:
	from nocolor import green, turquoise, white, red, yellow
import utils

# bzImage <target> build_sequence

def build_sequence(	kerneldir,		\
			master_config,		\
			arch, 			\
			KV,			\
			oldconfig, 		\
			menuconfig, 		\
			allyesconfig, 		\
			allnoconfig,		\
			mrproper,		\
			kconf,			\
			prepare,		\
			quiet, 			\
			nomodinstall=True):
	"""
	Kernel build sequence

	@arg: dict
	@arg: string
	@arg: string
	@arg: string
	@arg: string
	@arg: string
	@arg: string
	@arg: string
	@arg: string
	@arg: bool
	@arg: bool
	@return: bool
	"""
	import kmake

	ret = zero = int('0')
	# deal with the --kconf= option
	if kconf:
		# backup the previous .config found
		if os.path.isfile(kerneldir + '/.config'):
			from time import time
			kmake.copy_dotconfig(kerneldir + '/.config', kerneldir + '/.config.' + str(time()), quiet)
		# copy the custom .config
		kmake.copy_dotconfig(kconf, kerneldir + '/.config', quiet)

	if mrproper is True:
		ret = kmake.mrproper(kerneldir, KV, master_config, arch, quiet)
		if ret is not zero:
			print red('ERR: ')+'kernel.mrproper() failed'
			sys.exit(2)
	if allyesconfig is True:
		ret = kmake.allyesconfig(kerneldir, KV, master_config, arch, quiet)
		if ret is not zero:
			print red('ERR: ')+'kernel.allyesconfig() failed'
			sys.exit(2)
	elif allnoconfig is True:
		ret = kmake.allnoconfig(kerneldir, KV, master_config, arch, quiet)
		if ret is not zero:
			print red('ERR: ')+'kernel.allnoconfig() failed'
			sys.exit(2)
	if menuconfig is True or kconf is not '':
		ret = kmake.menuconfig(kerneldir, KV, master_config, arch, quiet)
		if ret is not zero:
			print red('ERR: ')+'kernel.oldconfig() failed'
			sys.exit(2)
	if oldconfig is True:
		ret = kmake.oldconfig(kerneldir, KV, master_config, arch, quiet)
		if ret is not zero:
			print red('ERR: ')+'kernel.menuconfig() failed'
			sys.exit(2)

	# check for kernel .config
	if os.path.isfile(kerneldir+'/.config') is not True:
		print red('ERR: ')+kerneldir+'/.config'+' does not exist.'
		sys.exit(2)

	# prepare
	if prepare is True:
		ret = kmake.prepare(kerneldir, KV, master_config, arch, quiet)
		if ret is not zero:
			print red('ERR: ')+'kernel.prepare() failed'
			sys.exit(2)

	# bzImage
	ret = kmake.bzImage(kerneldir, KV, master_config, arch, quiet)
	if ret is not zero:
		print red('ERR: ')+'kernel.bzImage() failed'
		sys.exit(2)

#	# copy bzImage and System.map
#	utils.chgdir(kerneldir)
#
#	bzImage_path  = 'arch/x86/boot/bzImage' # TODO remove hardcoded arch but do we for x86_64?
#	systemap_path = 'System.map'
#
#	# TODO: check /boot is available
#	utils.copy_file(bzImage_path,  '/boot/kernel-funkernel-'+arch+'-'+KV, quiet)
#	utils.copy_file(systemap_path, '/boot/System.map-funkernel-'+arch+'-'+KV, quiet)
#	utils.copy_file(kerneldir+'/.config', '/etc/kernels/kernel-config-funkernel-'+arch+'-'+KV, quiet)

	return ret
