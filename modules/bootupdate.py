import os
import sys
from stdout import green, turquoise, white, red, yellow

import funtoo.boot.config
import funtoo.core.config

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
#			print yellow(' * ')+ '/etc/boot.conf is ' + yellow('missing')
			return d
	else:
#		print yellow(' * ')+ 'sys-apps/boot-update is ' + yellow('missing')
		return d


