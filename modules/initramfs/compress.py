import os
import sys
import shutil
from utils.process import *
from stdout import white, green, turquoise, yellow, red

def initramfs(temproot, compress, into, verbose):
    """
    Compress user initramfs

    @return: bool
    """
    print(green(' * ')+turquoise('tool.compress.initramfs ')+'from '+compress+' into '+into)

    if os.path.isfile(into):
        from time import strftime
        os.system('mv %s %s-%s ' % (into, into, strftime("%Y-%m-%d-%H-%M-%S")))

    if not os.path.isdir(os.path.dirname(into)):
        os.makedirs(os.path.dirname(into))

    process_pipe('echo -n | cpio --quiet -o -H newc -F %s/initramfs_data.cpio' % os.path.dirname(into), verbose)
#    os.system('echo | cpio --quiet -o -H newc -F %s/initramfs_data.cpio 2>/dev/null' % os.path.dirname(into))
    os.chdir(compress)
    process_pipe('find . -print | cpio --quiet -o -H newc --append -F %s/initramfs_data.cpio' % os.path.dirname(into), verbose)
    process('gzip %s/initramfs_data.cpio' % os.path.dirname(into), verbose)
#    process('mv %s/initramfs_data.cpio.gz %s' % (os.path.dirname(into), into), verbose)
    os.system('mv %s/initramfs_data.cpio.gz %s 2>/dev/null' % (os.path.dirname(into), into))
