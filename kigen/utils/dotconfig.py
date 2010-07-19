import os

# DON'T USE COLOR HERE

def add_option(option, kerneldir):
    option = option.split('=') # list
    found = ['', '']
    for line in open(kerneldir+'/.config'):
        if line.startswith(option[0]):
            # found option=value
            if option[1] is 'y':
                # option is in-kernel
                found[0] = option[0]
                found[1] = 'y'
            if option[1] is 'm':
                # option is a module
                found[0] = option[0]
                found[1] = 'm'
            if isinstance(option[1], str) and option[1] is not '':
                # option is string in-kernel
                option[1] = option[1].replace('"', '')
                option[1] = option[1].replace('\n', '')

                found[0] = option[0]
                found[1] = line.split('=')[1].replace('"', '').replace('\n', '')

    if found[1] is '':
        if file(kerneldir+'/.config', 'a').writelines(option[0]+'="'+option[1] + '"'+'\n'):
            return True

    return False

def remove_option(option, kerneldir):
    os.system('grep -v %s %s > %s' % (option, kerneldir+'/.config', kerneldir+'/.config.kigen.temp'))
    return os.system('mv %s %s' % (kerneldir+'/.config.kigen.temp', kerneldir+'/.config'))
