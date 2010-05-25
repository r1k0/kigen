import os
import sys
color = os.getenv("GENKI_STD_COLOR")
if color == '0':
	from portage.output import green, turquoise, white, red, yellow
else:
	from nocolor import green, white, red, yellow, turquoise

# kernel <target> build_sequence

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
			quiet, 			\
			nomodinstall,		\
			fakeroot):
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
	@arg: string
	@arg: bool
	@arg: string
	@return: bool
	"""
	import kmake
	import utils

	ret = zero = int('0')
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
			print red('ERR')+': '+'kernel.mrproper() failed'
			sys.exit(2)
	if allyesconfig is True:
		ret = kmake.allyesconfig(kerneldir, KV, master_config, arch, quiet)
		if ret is not zero:
			print red('ERR')+': '+'kernel.allyesconfig() failed'
			sys.exit(2)
	elif allnoconfig is True:
		ret = kmake.allnoconfig(kerneldir, KV, master_config, arch, quiet)
		if ret is not zero:
			print red('ERR')+': '+'kernel.allnoconfig() failed'
			sys.exit(2)
	if menuconfig is True or kconf is not '':
		ret = kmake.menuconfig(kerneldir, KV, master_config, arch, quiet)
		if ret is not zero:
			print red('ERR')+': '+'kernel.oldconfig() failed'
			sys.exit(2)
	if oldconfig is True:
		ret = kmake.oldconfig(kerneldir, KV, master_config, arch, quiet)
		if ret is not zero:
			print red('ERR')+': '+'kernel.menuconfig() failed'
			sys.exit(2)

	# check for kernel .config
	if os.path.isfile(kerneldir+'/.config') is not True:
		print red('ERR')+': '+kerneldir+'/.config'+' does not exist.'
		sys.exit(2)

	# prepare
	ret = kmake.prepare(kerneldir, KV, master_config, arch, quiet)
	if ret is not zero:
		print red('ERR')+': '+'kernel.prepare() failed'
		sys.exit(2)

	# bzImage
	ret = kmake.bzImage(kerneldir, KV, master_config, arch, quiet)
	if ret is not zero:
		print red('ERR')+': '+'kernel.bzImage() failed'
		sys.exit(2)

	# modules
	# if --allnoconfig is passed, then modules are disabled
	if allnoconfig is not True:
		ret = kmake.modules(kerneldir, KV, master_config, arch, quiet)
		if ret is not zero:
			print red('ERR')+': '+'kernel.modules() failed'
			sys.exit(2)
		if nomodinstall is False:
			# modules_install
			ret = kmake.modules_install(kerneldir, KV, master_config, arch, quiet, fakeroot)
			if ret is not zero:
				print red('ERR')+': '+'kernel.modules_install() failed'
				sys.exit(2)

	return ret
