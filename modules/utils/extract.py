import os
import sys
import shutil
from utils.shell import *
from stdout import white, green, turquoise, yellow, red

def initramfs(temproot, extract, to, verbose):
    """
    Extract user initramfs

    @return: bool
    """
    initramfsdir = to

    # copy initramfs to /usr/src/linux/usr/initramfs_data.cpio.gz, should we care?
    print green(' * ') + turquoise('utils.extract.initramfs ') + 'to ' + initramfsdir

    # clean previous root
    if os.path.isdir(initramfsdir):
        from time import time
        os.system('mv %s %s-%s ' % (initramfsdir, initramfsdir, str(time())))
    process('mkdir -p %s' % initramfsdir, verbose)

    # create dir if needed
    if not os.path.isdir(initramfsdir):
        os.makedirs(initramfsdir)

    process('cp %s %s/initramfs_data.cpio.gz' % (extract, to), verbose)
    # extract gzip archive
    process('gzip -d -f %s/initramfs_data.cpio.gz' % to, verbose)

    # extract cpio archive
    os.chdir(initramfsdir)
    os.system('cpio -id < initramfs_data.cpio &>/dev/null')
    os.system('rm initramfs_data.cpio')

