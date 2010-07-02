import os
import sys
from stdout import green, turquoise, white, red, yellow
import utils

def download(sshversion, temp, verbose):
    """
    ssh tarball download routine

    @arg sshversion     string
    @arg verbose        dict

    @return: bool
    """
    print green(' * ') + '... ssh.download'
    ssh_url = 'ftp://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable' + \
                '/openssh-' + str(sshversion) + '.tar.gz'
#    return utils.sprocessor('/usr/bin/wget %s -O %s/distfiles/openssh-%s.tar.gz' % (ssh_url, utils.get_portdir(temp), str(sshversion)), verbose)
    return os.system('/usr/bin/wget %s -O %s/distfiles/openssh-%s.tar.gz %s' % (ssh_url, utils.get_portdir(temp), str(sshversion), verbose['std']))

def extract(sshversion, temp, verbose):
    """
    ssh tarball extraction routine

    @arg sshversion     string
    @arg temp           dict
    @arg verbose        dict

    @return: bool
    """
    print green(' * ') + '... ssh.extract'

    os.system('tar xvfz %s/distfiles/openssh-%s.tar.gz -C %s %s' % (utils.get_portdir(temp), str(sshversion), temp['work'], verbose['std']))

# e2fsprogrs building functions
def configure(sshtmp, master_config, verbose):
    """
    ssh Makefile interface to configure

    @arg sshtmp         string
    @arg master_config  dict
    @arg verbose        dict

    @return: bool
    """
    print green(' * ') + '... ssh.configure'
    utils.chgdir(sshtmp)

    return os.system('./configure --with-ldflags=-static %s' % verbose['std'])

def compile(sshtmp, master_config, verbose):
    """
    ssh Makefile interface to make

    @arg sshtmp             string
    @arg master_config      dict
    @arg verbose            dict

    @return: bool
    """
    print green(' * ') + '... ssh.compile'
    utils.chgdir(sshtmp)

    return os.system('%s %s %s' % (master_config['DEFAULT_UTILS_MAKE'], master_config['DEFAULT_MAKEOPTS'], verbose['std']))
#   ret = utils.sprocessor('%s %s' % (master_config['DEFAULT_UTILS_MAKE'], master_config['DEFAULT_MAKEOPTS']), verbose)

def strip(sshtmp, master_config):
    """
    blkid strip binary routine

    @arg sshtmp          string
    @arg master_config   dict

    @return: bool
    """
    print green(' * ') + '... ssh.strip'
    utils.chgdir(sshtmp)

    os.system('strip %s/sftp ' % sshtmp)
    os.system('strip %s/scp ' % sshtmp)
    return os.system('strip %s/sshd ' % sshtmp)

def compress(sshtmp, master_config, verbose):
    """
    blkid compression routine

    @arg sshtmp         string
    @arg master_config  dict

    @return: bool
    """
    print green(' * ') + '... ssh.compress'

    utils.chgdir(sshtmp)
    # create temp bin and sbin
    utils.sprocessor('mkdir -p bin', verbose)
    utils.sprocessor('mkdir -p sbin', verbose)
    utils.sprocessor('mkdir -p usr/local/etc', verbose)
    utils.sprocessor('cp ssh sftp scp bin', verbose)
    utils.sprocessor('cp sshd sbin', verbose)
    # that is where sshd expects its conf file
    utils.sprocessor('cp sshd_config usr/local/etc', verbose)
    # TODO create user/group ssh 

    return os.system('tar cf ssh.tar bin sbin usr')

def cache(sshtmp, master_config, temp, verbose):
    """
    blkid tarball cache routine

    @arg sshtmp         string
    @arg master_config  dict
    @arg temp           dict
    @arg verbose        dict

    @return: bool
    """
    print green(' * ') + '... ssh.cache'
    utils.chgdir(sshtmp)

    return utils.sprocessor('mv %s/ssh.tar %s/ssh-%s.tar' % (sshtmp, temp['cache'], master_config['ssh-version']), verbose)

# ssh sequence
def build_sequence(master_config, temp, verbose):
    """
    ssh build sequence

    @arg master_config  dict
    @arg temp           dict
    @arg verbose        dict

    @return: bool
    """
    ret = zero = int('0')

    if os.path.isfile('%s/distfiles/openssh-%s.tar.gz' % (utils.get_portdir(temp), str(master_config['ssh-version']))) is not True:
        ret = download(master_config['ssh-version'], temp, verbose)
        if ret is not zero:
            print red('error')+ ': '+'initramfs.ssh.download() failed'
            sys.exit(2)

    extract(master_config['ssh-version'], temp, verbose)
#   grr, tar thing to not return 0 when success

    ret = configure(temp['work'] + '/openssh-' + master_config['ssh-version'], master_config, verbose)
    if ret is not zero:
        print red('error: ')+'initramfs.ssh.configure() failed'
        sys.exit(2)

    ret = compile(temp['work'] + '/openssh-' + master_config['ssh-version'], master_config, verbose)
    if ret is not zero:
        print red('error: ')+'initramfs.ssh.compile() failed'
        sys.exit(2)

    ret = strip(temp['work'] + '/openssh-' + master_config['ssh-version'], master_config)
    if ret is not zero:
        print red('error: ')+'initramfs.ssh.strip() failed'
        sys.exit(2)

    ret = compress(temp['work'] + '/openssh-' + master_config['ssh-version'], master_config, verbose)
    if ret is not zero:
        print red('error: ')+'initramfs.ssh.compress() failed'
        sys.exit(2)

    ret = cache(temp['work'] + '/openssh-' + master_config['ssh-version'], master_config, temp, verbose)
    if ret is not zero:
        print red('error: ')+'initramfs.ssh.compress() failed'
        sys.exit(2)

    return ret
