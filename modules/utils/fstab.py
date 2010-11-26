import os

def fstab():
    ins = open( "/etc/fstab", "r" )
    array = []
    for line in ins:
        if not line.startswith('#'):
            array.append(line.split())
    return array

def check_boot():
    array = fstab()
    for i in array:
        print i
        if i[1] == '/boot':
            if os.path.ismount('/boot') is True:
                return True
            else:
                return False
#                if os.system('mount /boot'):
#                    True
