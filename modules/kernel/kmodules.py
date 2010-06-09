import sys
import os
import re
color = os.getenv("GENKI_STD_COLOR")
if color == 'ok':
	from portage.output import green, turquoise, white, red, yellow
else:
	from nocolor import green, turquoise, white, red, yellow

def get_sys_modules_list(KV):
	"""
	Get system module list

	@arg: string
	@return: list
	"""
	modlist = []
	moddir  = '/lib/modules/'+KV
	
	for root, subfolders, files in os.walk(moddir):
		for file in files:
			if re.search(".ko", file):
				modlist.append(file)
	return modlist

def get_config_modules_list(master_config):
	"""
	Get configuration module list

	@arg: dict
	@return: list
	"""
	modules_config = master_config['MODULES_ATARAID'] 	\
			+' '+master_config['MODULES_DMRAID'] 	\
			+' '+master_config['MODULES_EVMS'] 	\
			+' '+master_config['MODULES_LVM'] 	\
			+' '+master_config['MODULES_MDADM'] 	\
			+' '+master_config['MODULES_PATA'] 	\
			+' '+master_config['MODULES_SATA'] 	\
			+' '+master_config['MODULES_SCSI'] 	\
			+' '+master_config['MODULES_WAITSCAN'] 	\
			+' '+master_config['MODULES_NET'] 	\
			+' '+master_config['MODULES_ISCSI'] 	\
			+' '+master_config['MODULES_FIREWIRE'] 	\
			+' '+master_config['MODULES_PCMCIA'] 	\
			+' '+master_config['MODULES_USB'] 	\
			+' '+master_config['MODULES_FS']
	return modules_config

def get_config_modules_dict(master_config):
	"""
	Get configuration module dictionary

	@arg: dict
	@return: dict
	"""
	modules_config = { 'MODULES_ATARAID': master_config['MODULES_ATARAID'], \
			'MODULES_DMRAID': master_config['MODULES_DMRAID'], 	\
			'MODULES_EVMS': master_config['MODULES_EVMS'], 		\
			'MODULES_LVM': master_config['MODULES_LVM'], 		\
			'MODULES_MDADM': master_config['MODULES_MDADM'], 	\
			'MODULES_PATA': master_config['MODULES_PATA'], 		\
			'MODULES_SATA': master_config['MODULES_SATA'], 		\
			'MODULES_SCSI': master_config['MODULES_SCSI'], 		\
			'MODULES_WAITSCAN': master_config['MODULES_WAITSCAN'], 	\
			'MODULES_NET': master_config['MODULES_NET'], 		\
			'MODULES_ISCSI': master_config['MODULES_ISCSI'], 	\
			'MODULES_FIREWIRE': master_config['MODULES_FIREWIRE'], 	\
			'MODULES_PCMCIA': master_config['MODULES_PCMCIA'], 	\
			'MODULES_USB': master_config['MODULES_USB'], 		\
			'MODULES_FS': master_config['MODULES_FS'] }
	return modules_config
