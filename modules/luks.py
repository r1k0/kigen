import os
import sys
from stdout import green, turquoise, white, red, yellow
import utils

def download(luks_ver, temp, verbose):
    """
    luks tarball download routine

    @arg luks_ver       string
    @arg verbose        dict

    @return: bool
    """
    print green(' * ') + '... luks.download'
    luks_url = 'http://gentoo.osuosl.org/distfiles/cryptsetup-' + luks_ver + '.tar.bz2'
#    return utils.sprocessor('/usr/bin/wget %s -O %s/distfiles/cryptsetup-%s.tar.bz2' % (luks_url, utils.get_portdir(temp), str(luks_ver)), verbose)
    return os.system('/usr/bin/wget %s -O %s/distfiles/cryptsetup-%s.tar.bz2 %s' % (luks_url, utils.get_portdir(temp), str(luks_ver), verbose['std']))

def extract(luks_ver, temp, verbose):
    """
    luks tarball extraction routine

    @arg luks_ver       string
    @arg temp           dict
    @arg verbose        dict

    @return: bool
    """
    print green(' * ') + '... luks.extract'

    os.system('tar xvfj %s/distfiles/cryptsetup-%s.tar.bz2 -C %s %s' % (utils.get_portdir(temp), str(luks_ver), temp['work'], verbose['std']))

# e2fsprogrs building functions
def configure(lukstmp, master_config, verbose):
    """
    luks Makefile interface to configure

    @arg lukstmp        string
    @arg master_config  dict
    @arg verbose        dict

    @return: bool
    """
    print green(' * ') + '... luks.configure'
    utils.chgdir(lukstmp)

    return os.system('./configure --enable-static %s' % verbose['std'])

def compile(lukstmp, master_config, verbose):
    """
    luks Makefile interface to make

    @arg lukstmp            string
    @arg master_config      dict
    @arg verbose            dict

    @return: bool
    """
    print green(' * ') + '... luks.compile'
    utils.chgdir(lukstmp)

    return os.system('%s %s %s' % (master_config['DEFAULT_UTILS_MAKE'], master_config['DEFAULT_MAKEOPTS'], verbose['std']))

def strip(lukstmp, master_config):
    """
    blkid strip binary routine

    @arg lukstmp        string
    @arg master_config  dict

    @return: bool
    """
    print green(' * ') + '... luks.strip'
    utils.chgdir(lukstmp)

    return os.system('strip %s/src/cryptsetup' % lukstmp)

def compress(lukstmp, master_config):
    """
    blkid compression routine

    @arg lukstmp        string
    @arg master_config  dict

    @return: bool
    """
    print green(' * ') + '... luks.compress'
    utils.chgdir(lukstmp)

    return os.system('bzip2 %s/src/cryptsetup' % lukstmp)

def cache(lukstmp, master_config, temp, verbose):
    """
    blkid tarball cache routine

    @arg lukstmp        string
    @arg master_config  dict
    @arg temp           dict
    @arg verbose        dict

    @return: bool
    """
    print green(' * ') + '... luks.cache'
    utils.chgdir(lukstmp)

    return utils.sprocessor('mv %s/src/cryptsetup.bz2 %s/cryptsetup-%s.bz2' % (lukstmp, temp['cache'], master_config['luks-version']), verbose)

# luks sequence
def build_sequence(master_config, temp, verbose):
    """
    luks build sequence

    @arg master_config  dict
    @arg temp           dict
    @arg verbose        dict

    @return: bool
    """
    ret = zero = int('0')

    if os.path.isfile('%s/distfiles/cryptsetup-%s.tar.bz2' % (utils.get_portdir(temp), str(master_config['luks-version']))) is not True:
        ret = download(master_config['luks-version'], temp, verbose)
        if ret is not zero:
            print red('ERR: ')+'initramfs.luks.download() failed'
            sys.exit(2)

    extract(master_config['luks-version'], temp, verbose)
#   grr, tar thing to not return 0 when success

    ret = configure(temp['work'] + '/cryptsetup-' + master_config['luks-version'], master_config, verbose)
    if ret is not zero:
        print red('ERR: ')+'initramfs.luks.configure() failed'
        sys.exit(2)

    ret = compile(temp['work'] + '/cryptsetup-' + master_config['luks-version'], master_config, verbose)
    if ret is not zero:
        print red('ERR: ')+'initramfs.luks.compile() failed'
        sys.exit(2)

    ret = strip(temp['work'] + '/cryptsetup-' + master_config['luks-version'], master_config)
    if ret is not zero:
        print red('ERR: ')+'initramfs.luks.strip() failed'
        sys.exit(2)

    ret = compress(temp['work'] + '/cryptsetup-' + master_config['luks-version'], master_config)
    if ret is not zero:
        print red('ERR: ')+'initramfs.luks.compress() failed'
        sys.exit(2)

    ret = cache(temp['work'] + '/cryptsetup-' + master_config['luks-version'], master_config, temp, verbose)
    if ret is not zero:
        print red('ERR: ')+'initramfs.luks.compress() failed'
        sys.exit(2)

    return ret
