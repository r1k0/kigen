import os

def fstab():
    ins = open( "/etc/fstab", "r" )
    array = []
    for line in ins:
        if not line.startswith('#'):
            array.append(line.split())
    return array

def check_boot_fstab():
    array = fstab()
    for i in array:
        if i[1] == '/boot':
            return True
    return False

def check_boot_mount():
    if os.path.ismount('/boot') is True:
        return True
    else:
        return False

def mount_boot():
    if os.system('mount /boot'):
        return True
    else:
        return False
