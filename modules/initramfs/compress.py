import os
import sys
import shutil
from utils.shell import *
from stdout import white, green, turquoise, yellow, red

def initramfs(temproot, compress, into, verbose):
    """
    Compress user initramfs

    @return: bool
    """
    print green(' * ') + turquoise('initramfs.compress.initramfs ') + 'into ' + into

    #process('cpio -f %s' % ,verbose)






#    # clean previous root
#    if os.path.isdir(to):
#        from time import strftime
#        os.system('mv %s %s-%s ' % (to, to, strftime("%Y-%m-%d-%H-%M-%S")))
#    process('mkdir -p %s' % to, verbose)
#
#    # create dir if needed
#    if not os.path.isdir(to):
#        os.makedirs(to)
#
#    process('cp %s %s/initramfs_data.cpio.gz' % (extract, to), verbose)
#    # extract gzip archive
#    process('gzip -d -f %s/initramfs_data.cpio.gz' % to, verbose)
#
#    # extract cpio archive
#    os.chdir(to)
#    os.system('cpio -id < initramfs_data.cpio &>/dev/null')
#    os.system('rm initramfs_data.cpio')
#
