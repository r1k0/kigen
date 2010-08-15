import os
import sys

def getdotconfig(binary, kerneldir, verbose):
    if os.path.isfile(kerneldir+'/scripts/extract-ikconfig'):
        print 'err: kernel sources not found'

    if os.path.isfile('/var/tmp/kigen/dotconfig'):
        from time import strftime
        os.system('mv %s %s-%s ' % ('/var/tmp/kigen/dotconfig', '/var/tmp/kigen/dotconfig', strftime("%Y-%m-%d-%H-%M-%S")))

    os.system('%s %s > /var/tmp/kigen/dotconfig')
