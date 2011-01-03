import os
import sys
from utils.process import *
from stdout import white, green, turquoise, yellow, red

def getdotconfig(binary, kerneldir, verbose):

    print(green(' * ')+turquoise('kernel.extract.getdotconfig ')+'from '+binary+' to /var/tmp/kigen/dotconfig')

    if not os.path.isfile(kerneldir+'/scripts/extract-ikconfig'):
        print('err: kernel sources not found')
        sys.exit(2)

    if os.path.isfile('/var/tmp/kigen/dotconfig'):
        from time import strftime
        os.system('mv %s %s-%s ' % ('/var/tmp/kigen/dotconfig', '/var/tmp/kigen/dotconfig', strftime("%Y-%m-%d-%H-%M-%S")))

    os.system('%s %s > /var/tmp/kigen/dotconfig &>/dev/null' % (kerneldir+'/scripts/extract-ikconfig', binary))
