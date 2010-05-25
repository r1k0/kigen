import os
import sys
color = os.getenv("GENKI_STD_COLOR")
if color == '0':
	from portage.output import green, turquoise, white, red, yellow
else:
	from nocolor import green, turquoise, white, red, yellow
import utils

def copy_dotconfig(kernel_config, kerneldir, quiet):
	"""
	Copy kernel .config file to kerneldir 
	(/usr/src/linux by default)

	@arg: string
	@arg: string
	@return: none
	"""
	cpv = ''
	if quiet is '': cpv = '-v'
	print green(' * ') + turquoise('kernel.copy_config')
	if os.path.isfile(kernel_config):
		return os.system('cp %s %s %s' % (cpv, kernel_config, kerneldir))
	else:
		print red('ERR: ') + kernel_config + " doesn't exist."
		sys.exit(2)

# kernel building functions
def build_command(master_config, arch, target, quiet):
	"""
	Kernel Makefile bash build command

	@arg: dict
	@arg: string
	@arg: string
	@arg: string
	@return: string
	"""
	command = '%s %s CC="%s" LD="%s" AS="%s" ARCH="%s" %s %s' % (master_config['DEFAULT_KERNEL_MAKE'], 	\
								master_config['DEFAULT_MAKEOPTS'],      	\
								master_config['DEFAULT_KERNEL_CC'],     	\
								master_config['DEFAULT_KERNEL_LD'],     	\
								master_config['DEFAULT_KERNEL_AS'],     	\
								arch,                                           \
								target, 					\
								quiet)
	return command

def mrproper(kerneldir, KV, master_config, arch, quiet):
	"""
	Kernel command interface for mrproper

	@arg: string
	@arg: dict
	@arg: string
	@arg: string
	@return: bool
	"""
	print green(' * ') + turquoise('kernel.mrproper ') + KV
	utils.chgdir(kerneldir)
	command = build_command(master_config, arch, 'mrproper', quiet)
	if quiet is '':
		print command
	return os.system(command)

# TODO: should we add a sort of yes '' | make oldconfig?
def oldconfig(kerneldir, KV, master_config, arch, quiet):
	"""
	Kernel command interface for oldconfig

	@arg: string
	@arg: dict
	@arg: string
	@arg: string
	@return: bool
	"""
	print green(' * ') + turquoise('kernel.oldconfig ') + KV
	utils.chgdir(kerneldir)
	command = build_command(master_config, arch, 'oldconfig', '')
	if quiet is '':
		print command
	return os.system(command)

def allyesconfig(kerneldir, KV, master_config, arch, quiet):
	"""
	Kernel command interface for allyesconfig

	@arg: string
	@arg: dict
	@arg: string
	@arg: string
	@return: bool
	"""
	print green(' * ') + turquoise('kernel.allyesconfig ') + KV
	utils.chgdir(kerneldir)
	command = build_command(master_config, arch, 'allyesconfig', quiet)
	if quiet is '':
		print command
	return os.system(command)

def allnoconfig(kerneldir, KV, master_config, arch, quiet):
	"""
	Kernel command interface for allnoconfig

	@arg: string
	@arg: dict
	@arg: string
	@arg: string
	@return: bool
	"""
	print green(' * ') + turquoise('kernel.allnoconfig ') + KV
	utils.chgdir(kerneldir)
	command = build_command(master_config, arch, 'allnoconfig', quiet)
	if quiet is '':
		print command
	return os.system(command)

def menuconfig(kerneldir, KV, master_config, arch, quiet):
	"""
	Kernel command interface for menuconfig

	@arg: string
	@arg: dict
	@arg: string
	@arg: string
	@return: bool
	"""
	print green(' * ') + turquoise('kernel.menuconfig ') + KV
	utils.chgdir(kerneldir)
	command = build_command(master_config, arch, 'menuconfig', '')
	return os.system(command)

def prepare(kerneldir, KV, master_config, arch, quiet):
	"""
	Kernel command interface for prepare

	@arg: string
	@arg: dict
	@arg: string
	@arg: string
	@return: bool
	"""
	print green(' * ') + turquoise('kernel.prepare ') + KV
	utils.chgdir(kerneldir)
	command = build_command(master_config, arch, 'prepare', quiet)
	if quiet is '':
		print command
	return os.system(command)
def bzImage(kerneldir, KV, master_config, arch, quiet):
	"""
	Kernel command interface for bzImage

	@arg: string
	@arg: dict
	@arg: string
	@arg: string
	@return: bool
	"""
	print green(' * ') + turquoise('kernel.bzImage ') + KV
	utils.chgdir(kerneldir)
	command = build_command(master_config, arch, 'bzImage', quiet)
	if quiet is '':
		print command
	return os.system(command)

def modules(kerneldir, KV, master_config, arch, quiet):
	"""
	Kernel command interface for modules

	@arg: string
	@arg: dict
	@arg: string
	@arg: string
	@return: bool
	"""
	print green(' * ') + turquoise('kernel.modules ') + KV
	utils.chgdir(kerneldir)
	command = build_command(master_config, arch, 'modules', quiet)
	if quiet is '':
		print command
	return os.system(command)

def modules_install(kerneldir, KV, master_config, arch, quiet, fakeroot):
	"""
	Kernel command interface for modules_install 

	@arg: string
	@arg: dict
	@arg: string
	@arg: string
	@return: bool
	"""
	print green(' * ') + turquoise('kernel.modules_install ') + fakeroot + '/lib/modules/' + KV
	utils.chgdir(kerneldir)

	# export INSTALL_MOD_PATH 
	os.system('export INSTALL_MOD_PATH=%s' % fakeroot)

	command = build_command(master_config, arch, 'modules_install', quiet)
	if quiet is '':
		print command
	return os.system(command)

