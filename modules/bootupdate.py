import os
import sys
color = os.getenv("GENKI_STD_COLOR")
if color == '0':
	from portage.output import *
else:
	from nocolor import green, turquoise, white, red, yellow

try:
	import funtoo.boot.config
	import funtoo.core.config
except:
	# for some reason import never fails
	# even if bootupdate is not installed, errrmmm gotta figure this one out
	# hence the check for boot-update
	pass

def get_boot_initrd():
	"""
	Return dictionary of initrd /etc/boot.conf entry

	@arg	none
	@return	dict
	"""
	d = {}

	if os.path.isfile('/sbin/boot-update'):
		if funtoo.boot.config.BootConfigFile('/etc/boot.conf').fileExists():
			bootconf = funtoo.core.config.ConfigFile('/etc/boot.conf')
			try:
				d = bootconf.sectionData['initrd']
			except:
				d = {}
#			modules = d.item("initrd", "load-modules").split()
			return d
		else:
			print yellow(' * ')+ '/etc/boot.conf is ' + yellow('missing')
			return d
	else:
		print yellow(' * ')+ 'sys-apps/boot-update is ' + yellow('missing')
		return d


