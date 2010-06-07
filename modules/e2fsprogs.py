import os
import sys
from stdout import green, turquoise, white, red, yellow
import utils

def download(e2fsprogs_ver, temp, verbose):
    """
    e2fsprogs tarball download routine

    @arg e2fsprogs_ver  string
    @arg verbose        dict

    @return: bool
    """
    print green(' * ') + '... e2fsprogs.download'
    e2fsprogs_url = 'http://downloads.sourceforge.net/project/e2fsprogs/e2fsprogs/' + \
                str(e2fsprogs_ver)  + \
                '/e2fsprogs-' + str(e2fsprogs_ver) + '.tar.gz'
#    return utils.sprocessor('/usr/bin/wget %s -O %s/distfiles/e2fsprogs-%s.tar.gz' % (e2fsprogs_url, utils.get_portdir(temp), str(e2fsprogs_ver)), verbose)
    return os.system('/usr/bin/wget %s -O %s/distfiles/e2fsprogs-%s.tar.gz %s' % (e2fsprogs_url, utils.get_portdir(temp), str(e2fsprogs_ver), verbose['std']))

def extract(e2fsprogs_ver, temp, verbose):
    """
    e2fsprogs tarball extraction routine

    @arg e2fsprogs_ver  string
    @arg temp           dict
    @arg verbose        dict

    @return: bool
    """
    print green(' * ') + '... e2fsprogs.extract'

    os.system('tar xvfz %s/distfiles/e2fsprogs-%s.tar.gz -C %s %s' % (utils.get_portdir(temp), str(e2fsprogs_ver), temp['work'], verbose['std']))

# e2fsprogrs building functions
def configure(e2tmp, master_config, verbose):
    """
    e2fsprogs Makefile interface to configure

    @arg e2tmp          string
    @arg master_config  dict
    @arg verbose        dict

    @return: bool
    """
    print green(' * ') + '... e2fsprogs.configure'
    utils.chgdir(e2tmp)

    return os.system('./configure --with-ldopts=-static %s' % verbose['std'])

def compile(e2tmp, master_config, verbose):
    """
    e2fsprogs Makefile interface to make

    @arg e2tmp              string
    @arg master_config      dict
    @arg verbose            dict

    @return: bool
    """
    print green(' * ') + '... e2fsprogs.compile'
    utils.chgdir(e2tmp)

    return os.system('%s %s %s' % (master_config['DEFAULT_UTILS_MAKE'], master_config['DEFAULT_MAKEOPTS'], verbose['std']))
#   ret = utils.sprocessor('%s %s' % (master_config['DEFAULT_UTILS_MAKE'], master_config['DEFAULT_MAKEOPTS']), verbose)

def strip(e2tmp, master_config):
    """
    blkid strip binary routine

    @arg e2tmp          string
    @arg master_config  dict

    @return: bool
    """
    print green(' * ') + '... e2fsprogs.strip'
    utils.chgdir(e2tmp)

    return os.system('strip %s/misc/blkid ' % e2tmp)

def compress(e2tmp, master_config):
    """
    blkid compression routine

    @arg e2tmp          string
    @arg master_config  dict

    @return: bool
    """
    print green(' * ') + '... e2fsprogs.compress'
    utils.chgdir(e2tmp)

    return os.system('bzip2 %s/misc/blkid' % e2tmp)

def cache(e2tmp, master_config, temp, verbose): # TODO pass arch? should we add 'arch' to blkid-e2fsprogs-%s.bz2? genkernel seems to do so
    """
    blkid tarball cache routine

    @arg e2tmp          string
    @arg master_config  dict
    @arg temp           dict
    @arg verbose        dict

    @return: bool
    """
    print green(' * ') + '... e2fsprogs.cache'
    utils.chgdir(e2tmp)

    return utils.sprocessor('mv %s/misc/blkid.bz2 %s/blkid-e2fsprogs-%s.bz2' % (e2tmp, temp['cache'], master_config['e2fsprogs-version']), verbose)

# e2fsprogs sequence
def build_sequence(master_config, temp, verbose):
    """
    e2fsprogs build sequence

    @arg master_config  dict
    @arg temp           dict
    @arg verbose        dict

    @return: bool
    """
    ret = zero = int('0')

    if os.path.isfile('%s/distfiles/e2fsprogs-%s.tar.gz' % (utils.get_portdir(temp), str(master_config['e2fsprogs-version']))) is not True:
        ret = download(master_config['e2fsprogs-version'], temp, verbose)
        if ret is not zero:
            print red('ERR: ')+'initramfs.e2fsprogs.download() failed'
            sys.exit(2)

    extract(master_config['e2fsprogs-version'], temp, verbose)
#   grr, tar thing to not return 0 when success

    ret = configure(temp['work'] + '/e2fsprogs-' + master_config['e2fsprogs-version'], master_config, verbose)
    if ret is not zero:
        print red('ERR: ')+'initramfs.e2fsprogs.configure() failed'
        sys.exit(2)

    ret = compile(temp['work'] + '/e2fsprogs-' + master_config['e2fsprogs-version'], master_config, verbose)
    if ret is not zero:
        print red('ERR: ')+'initramfs.e2fsprogs.compile() failed'
        sys.exit(2)

    ret = strip(temp['work'] + '/e2fsprogs-' + master_config['e2fsprogs-version'], master_config)
    if ret is not zero:
        print red('ERR: ')+'initramfs.e2fsprogs.strip() failed'
        sys.exit(2)

    ret = compress(temp['work'] + '/e2fsprogs-' + master_config['e2fsprogs-version'], master_config)
    if ret is not zero:
        print red('ERR: ')+'initramfs.e2fsprogs.compress() failed'
        sys.exit(2)

    ret = cache(temp['work'] + '/e2fsprogs-' + master_config['e2fsprogs-version'], master_config, temp, verbose)
    if ret is not zero:
        print red('ERR: ')+'initramfs.e2fsprogs.compress() failed'
        sys.exit(2)

    return ret
