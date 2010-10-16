import os
import sys
import shutil
from utils.process import *
from stdout import white, green, turquoise, yellow, red

def initramfs(temproot, extract, to, verbose):
    """
    Extract user initramfs

    @return: bool
    """
    # copy initramfs to /usr/src/linux/usr/initramfs_data.cpio.gz, should we care?
    print green(' * ') + turquoise('initramfs.extract.initramfs ') + 'to ' + to

    # clean previous root
    if os.path.isdir(to):
        from time import strftime
        os.system('mv %s %s-%s ' % (to, to, strftime("%Y-%m-%d-%H-%M-%S")))
    process('mkdir -p %s' % to, verbose)

    # create dir if needed
    if not os.path.isdir(to):
        os.makedirs(to)

    process('cp %s %s/initramfs_data.cpio.gz' % (extract, to), verbose)
    # extract gzip archive
    process('gzip -d -f %s/initramfs_data.cpio.gz' % to, verbose)

    # extract cpio archive
    os.chdir(to)
    os.system('cpio -id < initramfs_data.cpio &>/dev/null')
    os.system('rm initramfs_data.cpio')

