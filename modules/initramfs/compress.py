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
    print green(' * ')+turquoise('initramfs.compress.initramfs ')+'from '+compress+' into '+into

    if os.path.isdir(os.path.dirname(into)):
        from time import strftime
        os.system('mv %s %s-%s ' % (os.path.dirname(into), os.path.dirname(into), strftime("%Y-%m-%d-%H-%M-%S")))

    if not os.path.isdir(os.path.dirname(into)):
        os.makedirs(os.path.dirname(into))

    process_pipe('echo | cpio --quiet -o -H newc -F %s/initramfs_data.cpio' % os.path.dirname(into), verbose)
    os.chdir(compress)
    process_pipe('find . -print | cpio --quiet -o -H newc --append -F %s/initramfs_data.cpio' % os.path.dirname(into), verbose) 


# gzip it now

    process('gzip %s/initramfs_data.cpio' % os.path.dirname(into), verbose)




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
