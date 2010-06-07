import os
import sys
from stdout import white, green, turquoise
import error
import warning
import utils
import logging
import commands

class initramfs:

    def __init__(self,              \
                kernel_dir_opt,     \
                arch,               \
                KV,                 \
                libdir,             \
                master_config,      \
                cli,                \
                temp,               \
                bootupdateset,      \
                bootupdateinitrd,   \
                verbose):
        """
        init class
        """
        self.kernel_dir_opt     = kernel_dir_opt
        self.arch               = arch
        self.KV                 = KV
        self.libdir             = libdir
        self.master_config      = master_config # TODO replace 
        self.linuxrc            = cli['linuxrc']
        self.oldconfig          = cli['bboldconfig']
        self.menuconfig         = cli['bbmenuconfig']
        self.allyesconfig       = cli['allyesconfig']
        self.mrproper           = cli['mrproper']
        self.bbconf             = cli['bbconf']
        self.nocache            = cli['nocache']
        self.firmware           = cli['firmware']
        self.verbosestd         = verbose['std']
        self.verboseset         = verbose['set']
        self.verbose            = verbose # TODO replace 
        self.temproot           = temp['root']
        self.tempcache          = temp['cache']
        self.temp               = temp # TODO replace 
        self.bbconf             = cli['bbconf']
        self.nocache            = cli['nocache']
        self.firmware           = cli['firmware']
        self.cli                = cli # TODO replace
        self.bootupdateset      = bootupdateset
        self.bootupdateinitrd   = bootupdateinitrd

    def build(self):
        """
        Initramfs build sequence
    
        @arg kernel_dir_opt     string
        @arg arch               string
        @arg KV                 string
        @arg libdir             string
        @arg master_config      dict
        @arg cli                dict
        @arg temp               dict
        @arg corebootset        bool
        @arg corebootinitrd     string
        @arg verbose            dict
    
        @return: bool
        """
        ret = zero = int('0')
        import shutil
        cpv = ''
        if self.verboseset is True: cpv = '-v'
    
        # for the sake of knowing where we are
        os.chdir(self.temproot)

        # 1) create initial cpio
        ret, output = utils.spprocessor('echo | cpio --quiet -o -H newc -F %s/initramfs-cpio' % self.tempcache, self.verbose)
        if ret is not zero:
            raise error.fail('initial cpio creation failed')
        # 2) append base
        ret = append_base(self.linuxrc, self.kernel_dir_opt, self.arch, self.master_config, self.libdir, self.temp, self.oldconfig, self.menuconfig, self.allyesconfig, self.mrproper, self.verbose)
        if ret is not zero:
            raise error.fail('initramfs.append_baselayout()')
        # 3) append busybox
        os.chdir(self.temp['work'])
        ret = append_busybox(self.arch, self.bbconf, self.master_config, self.libdir, self.temp, self.oldconfig, self.menuconfig, self.allyesconfig, self.mrproper, self.master_config['busybox-progs'], self.nocache, self.verbose)
        if ret is not zero:
            raise error.fail('initramfs.append_busybox()')
        # 4) append lvm2
        if self.cli['lvm2'] is True:
            os.chdir(self.temp['work'])
            ret = append_lvm2(self.master_config, self.temp, self.nocache, self.verbose)
            if ret is not zero:
                raise error.fail('initramfs.append_lvm2()')
        # 5) append dmraid
        if self.cli['dmraid'] is True:
            os.chdir(self.temp['work'])
            ret = append_dmraid(self.master_config, self.cli['selinux'], self.temp, self.nocache, self.verbose)
            if ret is not zero:
                raise error.fail('initramfs.append_dmraid()')
        # 6) append iscsi
        if self.cli['iscsi'] is True:
            os.chdir(self.temp['work'])
            ret = append_iscsi(self.master_config, self.temp, self.nocache, self.verbose)
            if ret is not zero:
                raise error.fail('initramfs.append_iscsi()')
        # 7) append evms
        if self.cli['evms'] is True:
            os.chdir(self.temp['work'])
            ret = append_evms(self.temp, self.verbose)
            if ret is not zero: 
                raise error.fail('initramfs.append_evms()')
        # 8) append mdadm
        if self.cli['mdadm'] is True:
            os.chdir(self.temp['work'])
            ret = append_mdadm(self.temp, self.verbose)
            if ret is not zero: 
                raise error.fail('initramfs.append_mdadm()')
        # 9) append luks
        if self.cli['luks'] is True:
            os.chdir(self.temp['work'])
            ret = append_luks(self.master_config, self.temp, self.nocache, self.verbose)
            if ret is not zero: 
                raise error.fail('initramfs.append_luks()')
        # 10) append multipath
        # TODO
        # 11) append modules
        # note that /etc/boot.conf initrd modules overlap the ones from /etc/funkernel.conf
        ret = append_modules(self.master_config, self.KV, self.libdir, self.temp, self.verbose, self.bootupdateset, self.bootupdateinitrd)
        if ret is not zero: 
            raise error.fail('initramfs.append_modules()')
        # 12) append blkid
        if self.cli['disklabel'] is True:
            os.chdir(self.temp['work'])
            ret = append_blkid(self.master_config, self.libdir, self.temp, self.nocache, self.verbose)
            if ret is not zero: 
                raise error.fail('initramfs.append_blkid()')
        # 13) append ssh
        if self.cli['ssh'] is True:
            os.chdir(self.temp['work'])
            ret = append_ssh(self.master_config, self.libdir, self.temp, self.nocache, self.verbose)
            if ret is not zero:
                raise error.fail('initramfs.append_ssh()')
        # 13) append unionfs_fuse
        if self.cli['unionfs'] is True:
            os.chdir(self.temp['work'])
            ret = append_unionfs_fuse(self.master_config, self.temp, self.nocache, self.verbose)
            if ret is not zero: 
                raise error.fail('initramfs.append_unionfs-fuse()')
        # 14) append aufs
        if self.cli['aufs'] is True:
            os.chdir(self.temp['work'])
            ret = append_aufs(self.master_config, self.temp, self.nocache, self.verbose)
            if ret is not zero:
                raise error.fail('initramfs.append_aufs()')
        # 15) append splash
        if self.cli['splash'] is True:
            os.chdir(self.temp['work'])
            ret = append_splash(self.cli['stheme'], self.cli['sres'], self.master_config, self.temp, self.verbose)
            if ret is not zero:
                raise error.fail('initramfs.append_splash()')
        # 16) append firmware
        if os.path.isdir(self.firmware):
            os.chdir(self.temp['work'])
            ret = append_firmware(self.cli['firmware'], self.temp, self.verbose)
            if ret is not zero: 
                raise error.fail('initramfs.append_firmware()')
    
        # 17) append overlay
        # TODO
    
        # compress initramfs-cpio
        print green(' * ') + turquoise('initramfs.compress')
        utils.sprocessor('gzip -f -9 %s/initramfs-cpio' % self.temp['cache'], self.verbose)
        if ret is not zero: 
            raise error.fail('utils.copy_initramfs() compression pre copy')
    
        return ret
 
def append_cpio(temp):
    """
    Builds command with correct path

    @arg temp: string

    @return: string
    """
    cmd = 'find . -print | cpio --quiet -o -H newc --append -F %s/initramfs-cpio' % temp['cache']
    return cmd

def append_base(linuxrc, kernel_dir_opt, arch, master_config, libdir, temp, oldconfig, menuconfig, allyesconfig, mrproper, verbose):
    """
    Append baselayout to the initramfs

    @arg linuxrc        string
    @arg kernel_dir_opt string
    @arg master_config  dict
    @arg libdir         string
    @arg temp           dict
    @arg oldconfig      string
    @arg menuconfig     string
    @arg allyesconfig   string
    @arg mrproper       string
    @arg verbose        dict

    @return: bool
    """
    ret = int('0')
    logging.debug('initramfs.append_base')
    print green(' * ') + turquoise('initramfs.append_base'),

    # create the baselayout
    for i in ['dev', 'bin', 'etc', 'usr', 'proc', 'temp', 'sys', 'var/lock/dmraid', 'sbin', 'usr/bin', 'usr/sbin']:
        os.makedirs(temp['work']+'/initramfs-base-temp/%s' % i)

    os.chdir(kernel_dir_opt) # WHY? # TODO: change os.chdir by subprocess.popen(..., cwd=kernel_dir_opt

    # init
    if linuxrc is '':
    # TODO: copy linuxrc depending on arch
    # if netboot is True:
    #       cp "${GK_SHARE}/netboot/linuxrc.x" "${TEMP}/initramfs-aux-temp/init"
    # elif arch is 'x86':
    #       os.system('cp %s/arch/linuxrc %s/initramfs-base-temp/init' % (libdir, temp['work']))
    # elif arch is 'amd64':
    #       blablabla
        print
        utils.sprocessor('cp %s/defaults/linuxrc %s/initramfs-base-temp/init' % (libdir, temp['work']), verbose)
    else:
        # cp custom linuxrc to initramfs
        print white(linuxrc) + ' from host'
        utils.sprocessor('cp %s %s/initramfs-base-temp/init' % (linuxrc, temp['work']), verbose)

    # make init executable
    utils.sprocessor('chmod 0755 %s/initramfs-base-temp/init' % temp['work'], verbose)

    # link lib to lib64
    utils.sprocessor('ln -s lib %s/initramfs-base-temp/lib64' % temp['work'], verbose)

    # create fstab
    utils.srprocessor('echo /dev/ram0 / ext2 defaults 0 0\n > '+temp['work']+'/initramfs-base-temp/etc/fstab', verbose)
    utils.arprocessor('echo proc /proc proc defaults 0 0\n >> '+temp['work']+'/initramfs-base-temp/etc/fstab', verbose)

    os.chdir(temp['work']+'/initramfs-base-temp/dev')

    # create nodes
    utils.sprocessor('mknod -m 660 console c 5 1', verbose)
    utils.sprocessor('mknod -m 660 null    c 1 3', verbose)
    utils.sprocessor('mknod -m 660 tty1    c 4 1', verbose)

    # timestamp the build
    from time import strftime
    build_date = open(temp['work']+'/initramfs-base-temp/etc/build_date', 'w')
    build_date.writelines(strftime("%Y-%m-%d %H:%M:%S")+ '\n')
    build_date.close()

    # aux
    utils.sprocessor('mkdir -p ' + temp['work']+'/initramfs-base-temp/lib/keymaps', verbose)
    utils.sprocessor('tar -zxf %s/defaults/keymaps.tar.gz -C %s/initramfs-base-temp/lib/keymaps' % (libdir, temp['work']), verbose)

    os.chdir(temp['work']+'/initramfs-base-temp')
    utils.sprocessor('ln -s init linuxrc', verbose)
    utils.sprocessor('cp %s/defaults/initrd.scripts %s/initramfs-base-temp/etc/initrd.scripts' % (libdir, temp['work']), verbose)
    utils.sprocessor('cp %s/defaults/initrd.defaults %s/initramfs-base-temp/etc/initrd.defaults' % (libdir, temp['work']), verbose)
    # what's the harm to have it harcoded? even if the group is commented out in the config file the variable is still empty
    # same thinking for coreboot it's already set in etc/initrd.defaults $HWOPTS
    utils.arprocessor("echo HWOPTS='$HWOPTS ataraid dmraid evms firewire fs iscsi lvm2 mdadm net pata pcmcia sata scsi usb waitscan' >> %s/initramfs-base-temp/etc/initrd.defaults" % temp['work'], verbose)
    utils.sprocessor('cp %s/defaults/modprobe %s/initramfs-base-temp/sbin/modprobe' % (libdir, temp['work']), verbose)

    os.chdir(temp['work']+'/initramfs-base-temp/sbin')
    utils.sprocessor('ln -s ../init init', verbose)
    utils.sprocessor('chmod +x %s/initramfs-base-temp/init' % temp['work'], verbose)
    utils.sprocessor('chmod +x %s/initramfs-base-temp/etc/initrd.scripts' % temp['work'], verbose)
    utils.sprocessor('chmod +x %s/initramfs-base-temp/etc/initrd.defaults' % temp['work'], verbose)
    utils.sprocessor('chmod +x %s/initramfs-base-temp/sbin/modprobe' % temp['work'], verbose)

    os.chdir(temp['work']+'/initramfs-base-temp/')
    return os.system(append_cpio(temp))

def append_busybox(arch, bbconf, master_config, libdir, temp, oldconfig, menuconfig, allyesconfig, mrproper, busyboxprogs, nocache, verbose):
    """
    Append the busybox compiled objects to the initramfs

    @arg arch           string
    @arg bbconf         string
    @arg master_config  dict
    @arg libdir         string
    @arg temp           dict
    @arg oldconfig      string
    @arg menuconfig     string
    @arg allyesconfig   string
    @arg mrproper       string
    @arg busyboxprogs   list
    @arg nocache        bool
    @arg verbose        dict

    @return: bool
    """
    import busybox
    ret = zero = int('0')
    logging.debug('initramfs.append_busybox')
    print green(' * ') + turquoise('initramfs.append_busybox ') + master_config['bb_ver'],

    if os.path.isfile(temp['cache']+'/busybox-bin-'+master_config['bb_ver']+'.tar.bz2') and nocache is False:
        # use cache
        print 'from ' + white('cache')
    else:
        print busyboxprogs
        # compile
        ret = busybox.build_sequence( arch, \
                    bbconf,                 \
                    master_config,          \
                    libdir,                 \
                    temp,                   \
                    oldconfig,              \
                    menuconfig,             \
                    allyesconfig,           \
                    mrproper,               \
                    verbose['std'])
    # append busybox to cpio
    utils.sprocessor('mkdir -p ' + temp['work']+'/initramfs-busybox-temp/bin', verbose)
    os.chdir(temp['work']+'/initramfs-busybox-temp')
    utils.sprocessor('tar -xjf %s/busybox-bin-%s.tar.bz2 -C %s busybox' % (temp['cache'], master_config['bb_ver'], temp['work']+'/initramfs-busybox-temp/bin'), verbose)
    utils.sprocessor('chmod +x %s/busybox' % (temp['work']+'/initramfs-busybox-temp/bin'), verbose)
    utils.sprocessor('mkdir -p  %s/usr/share/udhcpc/' % (temp['work']+'/initramfs-busybox-temp'), verbose)
    utils.sprocessor('cp %s/defaults/udhcpc.scripts %s/initramfs-busybox-temp/usr/share/udhcpc/default.script' % (libdir, temp['work']), verbose)
    utils.sprocessor('chmod +x %s/initramfs-busybox-temp/usr/share/udhcpc/default.script' % temp['work'], verbose)

    for i in busyboxprogs.split():
        utils.sprocessor('ln -s busybox %s/initramfs-busybox-temp/bin/%s' % (temp['work'], i), verbose)

    os.chdir(temp['work']+'/initramfs-busybox-temp')
    if ret is zero:
        return os.system(append_cpio(temp))

def append_luks(master_config, temp, nocache, verbose):
    """
    Append the LUKS static binary to the initramfs

    @arg temp       dict
    @arg verbose    dict

    @return: bool
    """
    ret = int('0')
    cryptsetup_bin  = '/bin/cryptsetup'
    cryptsetup_sbin = '/sbin/cryptsetup'

    utils.sprocessor('mkdir -p ' + temp['work']+'/initramfs-luks-temp/lib/luks', verbose)
    utils.sprocessor('mkdir -p ' + temp['work']+'/initramfs-luks-temp/sbin', verbose)

    if os.path.isfile(cryptsetup_bin):
        luks_host_version = commands.getoutput("cryptsetup --version | cut -d' ' -f2")
        logging.debug('initramfs.append_luks ' + luks_host_version + ' ' + cryptsetup_bin + ' from host')
        print green(' * ') + turquoise('initramfs.append_luks ') + luks_host_version + ' '  + white(cryptsetup_bin) + ' from host'
        utils.sprocessor('cp %s %s/initramfs-luks-temp/sbin' % (cryptsetup_bin, temp['work']), verbose)
        utils.sprocessor('chmod +x %s/initramfs-luks-temp/sbin/cryptsetup' % temp['work'], verbose)
    elif os.path.isfile(cryptsetup_sbin):
        luks_host_version = commands.getoutput("cryptsetup --version | cut -d' ' -f2")
        logging.debug('initramfs.append_luks ' + luks_host_version + ' ' + cryptsetup_sbin + ' from host')
        print green(' * ') + turquoise('initramfs.append_luks ') + luks_host_version + ' ' + white(cryptsetup_sbin) + ' from host'
        utils.sprocessor('cp %s %s/initramfs-luks-temp/sbin' % (cryptsetup_sbin, temp['work']), verbose)
        utils.sprocessor('chmod +x %s/initramfs-luks-temp/sbin/cryptsetup' % temp['work'], verbose)
    else:
        print green(' * ') + turquoise('initramfs.append_luks ') + master_config['luks-version'],
        logging.debug('initramfs.append_luks ' + master_config['luks-version'])
        if os.path.isfile(temp['cache']+'/cryptsetup-'+master_config['luks-version']+'.bz2') and nocache is False:
            # use cache
            print 'from ' + white('cache')
        else:
            # compile and cache
            print
            import luks
            luks.build_sequence(master_config, temp, verbose)

    # FIXME careful with the >
    os.system('/bin/bzip2 -dc %s/cryptsetup-%s.bz2 > %s/initramfs-luks-temp/sbin/cryptsetup' % (temp['cache'], master_config['luks-version'], temp['work']))
    utils.sprocessor('chmod a+x %s/initramfs-luks-temp/sbin/cryptsetup' % temp['work'], verbose)

    os.chdir(temp['work']+'/initramfs-luks-temp')
    return os.system(append_cpio(temp))

def build_device_mapper(master_config, temp, nocache, verbose):
    """
    Build the device-mapper and cache it for later use
    Only to be called if lvm2 or dmraid is compiled!

    @arg master_config  dict
    @arg temp           dict
    @arg nocache        bool
    @arg verbose        dict

    @return: bool
    """
    logging.debug('initramfs.build_device_mapper '+master_config['dm_ver'])
    print green(' * ') + turquoise('initramfs.build_device_mapper ') + master_config['dm_ver'],

    if os.path.isfile(temp['cache']+'/device-mapper-'+master_config['dm_ver']+'.tar.bz2') and nocache is False:
        # use cache
        print 'from ' + white('cache')
        return
    else:
        # compile and cache
        print
        import device_mapper
        return device_mapper.build_sequence(master_config, temp, verbose['std'])

def build_fuse(master_config, temp, nocache, verbose):
    """
    Build fuse and cache it for later use
    Only to be called for --unionfs!

    @arg master_config      dict
    @arg temp               dict
    @arg nocache            bool
    @arg verbose            dict

    @return: bool
    """
    logging.debug('initramfs.build_fuse ' + master_config['fuse_ver'])
    print green(' * ') + turquoise('initramfs.build_fuse ') +master_config['fuse_ver'],

    if os.path.isfile(temp['cache']+'/fuse-dircache-'+master_config['fuse_ver']+'.tar.bz2') and nocache is False:
        # use cache
        print 'from ' + white('cache')
    else:
        # compile and cache
        print
        import fuse
        fuse.build_sequence(master_config, temp, verbose)

    # extract
    os.system('tar xfj %s -C %s' % (temp['cache']+'/fuse-dircache-'+master_config['fuse_ver']+'.tar.bz2', temp['work']))

    return 

def append_lvm2(master_config, temp, nocache, verbose):
    """
    Append lvm2 static binary first to the initramfs

    @arg master_config  dict
    @arg temp           dict
    @arg nocache        bool
    @arg verbose        dict

    @return: bool
    """
    ret = int('0')
    lvm2_static_bin     = '/sbin/lvm.static'
    lvm2_bin        = '/sbin/lvm'

    utils.sprocessor('mkdir -p ' + temp['work']+'/initramfs-lvm2-temp/etc/lvm', verbose)
    utils.sprocessor('mkdir -p ' + temp['work']+'/initramfs-lvm2-temp/bin', verbose)

    if os.path.isfile(lvm2_static_bin):
        # TODO see if we can use something else than import commands
        #lvm2_static_version = commands.getoutput("lvm.static version | cut -d: -f2 | head -n1 | cut -d'(' -f1")
        logging.debug('initramfs.append_lvm2 ' + ' ' + lvm2_static_bin + ' from host')
        print green(' * ') + turquoise('initramfs.append_lvm2 ') + white(lvm2_static_bin) + ' from host'
        utils.sprocessor('cp %s %s/initramfs-lvm2-temp/bin/lvm' % (lvm2_static_bin, temp['work']), verbose)
    elif os.path.isfile(lvm2_bin):
        logging.debug('initramfs.append_lvm2 ' + lvm2_bin + ' from host')
        print green(' * ') + turquoise('initramfs.append_lvm2 ') + white(lvm2_bin) + ' from host'
        utils.sprocessor('cp %s %s/initramfs-lvm2-temp/bin/lvm' % (lvm2_bin, temp['work']), verbose)
    else:
        build_device_mapper(master_config, temp, nocache, verbose['std'])

        logging.debug('initramfs.append_lvm2 ')
        print green(' * ') + turquoise('initramfs.append_lvm2 ')

        import lvm2
        lvm2.build_sequence(master_config, temp, verbose['std'])

        utils.sprocessor('bzip2 -d %s' % temp['cache']+'/lvm.static-'+master_config['lvm_ver']+'.bz2', verbose)
        utils.sprocessor('cp %s/lvm.static-%s %s/initramfs-lvm2-temp/bin/lvm' % (temp['cache'], master_config['lvm_ver'], temp['work']), verbose)

    if os.path.isfile(lvm2_static_bin) or os.path.isfile(lvm2_bin):
        utils.sprocessor('cp /etc/lvm/lvm.conf %s/initramfs-lvm2-temp/etc/lvm/' % temp['work'], verbose)

    os.chdir(temp['work']+'/initramfs-lvm2-temp')
    return os.system(append_cpio(temp))

def append_modules(master_config, KV, libdir, temp, verbose, corebootset, corebootinitrd):
    """
    Find system modules and config modules
    Append modules to the initramfs

    @arg master_config  dict
    @arg KV             string
    @arg libdir         string
    @arg temp           dict
    @arg verbose        dict
    @arg corebootset    bool
    @arg corebootinitrd dict

    @return: bool
    """
    import kmodules
    ret = int('0')
    logging.debug('initramfs.append_modules ' + KV)
    print green(' * ') + turquoise('initramfs.append_modules ') + KV

    utils.sprocessor('mkdir -p ' + temp['work']+'/initramfs-modules-'+KV+'-temp/lib/modules/'+KV, verbose)
    
    # FIXME: ctrl c does not work during this function
    # TODO: rewrite (later)
    # TODO: maybe |uniq the list? in case the user sets 
    # multiple times the same module in different groups
    #
    # is it really a big deal? I don't think so

    # identify and copy kernel modules
    modsyslist  = kmodules.get_sys_modules_list(KV)
    modconflist = kmodules.get_config_modules_list(master_config) #.split()
    # TODO: add support for the 'probe' key

    # for each module in the list modconflist
    for i in modconflist.split():
        for j in modsyslist:
            k = i +'.ko'
            # check for a match
            if k == j:
                logging.debug('shipping ' + i)
                print green(' * ') + '... ' + white(i)
                # if the module is found copy it
                module = os.popen('find /lib/modules/'+KV+' -name '+k+' 2>/dev/null | head -n 1').read().strip()
                module_dirname = os.path.dirname(module)
                utils.sprocessor('mkdir -p %s%s%s'% (temp['work'],'/initramfs-modules-'+KV+'-temp',  module_dirname), verbose)
                utils.sprocessor('cp -ax %s %s/initramfs-modules-%s-temp/%s' % (module, temp['work'], KV, module_dirname), verbose)
    # for each module in /etc/boot.conf
    if "load-modules" in corebootinitrd:
        for i in corebootinitrd['load-modules'].split():
            for j in modsyslist:
                k = i +'.ko'
                if k == j:
                    logging.debug('shipping ' + i + ' from /etc/boot.conf')
                    print green(' * ') + '... ' + white(i) + ' from /etc/boot.conf'
                    module = os.popen('find /lib/modules/'+KV+' -name '+k+' 2>/dev/null | head -n 1').read().strip()
                    module_dirname = os.path.dirname(module)
                    utils.sprocessor('mkdir -p %s%s%s'% (temp['work'],'/initramfs-modules-'+KV+'-temp',  module_dirname), verbose)
                    utils.sprocessor('cp -ax %s %s/initramfs-modules-%s-temp/%s' % (module, temp['work'], KV, module_dirname), verbose)

    # TODO: make variable of /lib/modules in case of FAKEROOT export
    os.system('cp /lib/modules/%s/modules.* %s' % (KV, temp['work']+'/initramfs-modules-'+KV+'-temp/lib/modules/'+KV ))

    # create etc/modules/<group>
    utils.sprocessor('mkdir -p ' + temp['work']+'/initramfs-modules-'+KV+'-temp/etc/modules', verbose)
    modconfdict = kmodules.get_config_modules_dict(master_config)

    # Genkernel official boot module design
    # for each key value in the module config dictionary
    for k, v in modconfdict.iteritems():
        # match the group for which the module belongs
        k = k.lower()
        group = k.split('_')[1]
        # and add it etc/modules/
        f = open(temp['work']+'/initramfs-modules-'+KV+'-temp/etc/modules/'+group, 'w')
        f.write(v.replace(" ", "\n"))
        f.close

    # Funtoo coreboot initramfs module file config
    if "load-modules" in corebootinitrd:
        for o in corebootinitrd['load-modules'].split():
            # FIXME think about >> passed to sprocessor?
            utils.arprocessor('echo %s >> %s' % (o, temp['work']+'/initramfs-modules-'+KV+'-temp/etc/modules/bootupdate'), verbose)

    os.chdir(temp['work']+'/initramfs-modules-'+KV+'-temp')
    return os.system(append_cpio(temp))

def append_blkid(master_config, libdir, temp, nocache, verbose):
    """
    Append blkid binary to the initramfs
    after compiling e2fsprogs
    
    @arg master_config  dict
    @arg libdir         string
    @arg temp           dict
    @arg nocache        bool
    @arg verbose        dict
    
    @return: bool
    """
    logging.debug('initramfs.append_blkid ' + master_config['e2fsprogs-version'])
    print green(' * ') + turquoise('initramfs.append_blkid ') + master_config['e2fsprogs-version'],

    if os.path.isfile(temp['cache']+'/blkid-e2fsprogs-'+master_config['e2fsprogs-version']+'.bz2') and nocache is False:
        # use cache
        print 'from ' + white('cache')
    else:
        # compile
        print
        import e2fsprogs
        e2fsprogs.build_sequence(master_config, temp, verbose)

    utils.sprocessor('mkdir -p ' + temp['work']+'/initramfs-blkid-temp/bin', verbose)

    # FIXME careful with the >
    os.system('/bin/bzip2 -dc %s/blkid-e2fsprogs-%s.bz2 > %s/initramfs-blkid-temp/bin/blkid' % (temp['cache'], master_config['e2fsprogs-version'], temp['work']))
    #utils.srprocessor('/bin/bzip2 -dc %s/blkid-e2fsprogs-%s.bz2 > %s/initramfs-blkid-temp/bin/blkid' % (temp['cache'], master_config['e2fsprogs_ver'], temp['work']), verbose)
    utils.sprocessor('chmod a+x %s/initramfs-blkid-temp/bin/blkid' % temp['work'], verbose)
    
    os.chdir(temp['work']+'/initramfs-blkid-temp')
    return os.system(append_cpio(temp))

def append_evms(temp, verbose):
    """
    Append evms libraries to the initramfs

    @arg temp   dict

    @return: bool
    """
    logging.debug('initramfs.append_evms')
    print green(' * ') + turquoise('initramfs.append_evms'),

    if os.path.isfile('/sbin/evms'):
        print 'feeding' + ' from host'

        utils.sprocessor('mkdir -p ' + temp['work']+'/initramfs-evms-temp/lib/evms', verbose)
        utils.sprocessor('mkdir -p ' + temp['work']+'/initramfs-evms-temp/etc', verbose)
        utils.sprocessor('mkdir -p ' + temp['work']+'/initramfs-evms-temp/bin', verbose)
        utils.sprocessor('mkdir -p ' + temp['work']+'/initramfs-evms-temp/sbin', verbose)

    # FIXME broken due to *
    # utils.sprocessor('cp -a /lib/ld-* %s/initramfs-evms-temp/lib' % temp['work'], verbose)
    # utils.sprocessor('cp -a /lib/libgcc_s* %s/initramfs-evms-temp/lib' % temp['work'], verbose)
    # utils.sprocessor('cp -a /lib/libc-* /lib/libc.* %s/initramfs-evms-temp/lib' % temp['work'], verbose)
    # utils.sprocessor('cp -a /lib/libdl-* /lib/libdl.* %s/initramfs-evms-temp/lib' % temp['work'], verbose)
    # utils.sprocessor('cp -a /lib/libpthread* %s/initramfs-evms-temp/lib' % temp['work'], verbose)
    # utils.sprocessor('cp -a /lib/libuuid*so* %s/initramfs-evms-temp/lib' % temp['work'], verbose)
    # utils.sprocessor('cp -a /lib/libevms*so* %s/initramfs-evms-temp/lib' % temp['work'], verbose)
    # utils.sprocessor('cp -a /lib/evms %s/initramfs-evms-temp/lib' % temp['work'], verbose)
    # utils.sprocessor('cp -a /lib/evms/* %s/initramfs-evms-temp/lib/evms' % temp['work'], verbose)
    # utils.sprocessor('cp -a /etc/evms.conf %s/initramfs-evms-temp/etc' % temp['work'], verbose)
    # utils.sprocessor('cp /sbin/evms_activate %s/initramfs-evms-temp/sbin' % temp['work'], verbose)
    # utils.sprocessor('rm %s/initramfs-evms-temp/lib/evms/*/swap*.so' % temp['work'], verbose)
    else:
        logging.debug('ERR: evms must be emerged on the host')
        print
        print red('ERR: ') + "evms must be emerged on the host"
        sys.exit(2)

    os.chdir(temp['work']+'/initramfs-evms-temp')
    return os.system(append_cpio(temp))

def append_firmware(firmware, temp, verbose):
    """
    Append firmware to the initramfs

    @arg firmware   string
    @arg temp       dict

    @return: bool
    """
    logging.debug('initramfs.append_firmware ' + firmware + ' from host')
    print green(' * ') + turquoise('initramfs.append_firmware ') + white(firmware) + ' from host'

    utils.sprocessor('mkdir -p ' + temp['work']+'/initramfs-firmware-temp/lib/firmware', verbose)
    utils.sprocessor('cp -a %s %s/initramfs-firmware-temp/lib/' % (firmware, temp['work']), verbose)

    os.chdir(temp['work']+'/initramfs-firmware-temp')
    return os.system(append_cpio(temp))

def append_mdadm(temp, verbose):
    """
    Append mdadm to initramfs

    @arg temp   dict

    @return: bool
    """
    ret = int('0')
    logging.debug('initramfs.append_mdadm')
    print green(' * ') + turquoise('initramfs.append_mdadm')

    utils.sprocessor('mkdir -p ' + temp['work']+'/initramfs-dmadm-temp/etc', verbose)
    utils.sprocessor('cp -a /etc/mdadm.conf %s/initramfs-mdadm-temp/etc' % temp['work'], verbose)

    os.chdir(temp['work']+'/initramfs-mdadm-temp')
    return os.system(append_cpio(temp))

def append_dmraid(master_config, selinux, temp, nocache, verbose):
    """
    Append dmraid to initramfs

    @arg master_config  dict
    @arg selinux        bool
    @arg temp           dict
    @arg nocache        bool
    @arg verbose

    @return: bool
    """
    build_device_mapper(master_config, temp, nocache, verbose)

    logging.debug('initramfs.append_dmraid ' + master_config['dmraid_ver'])
    print green(' * ') + turquoise('initramfs.append_dmraid ') + master_config['dmraid_ver'],

    utils.sprocessor('mkdir -p ' + temp['work']+'/initramfs-dmraid-temp/bin', verbose)

    if os.path.isfile(temp['cache']+'/dmraid.static-'+master_config['dmraid_ver']+'.bz2') and nocache is False:
    # use cache
        print 'from ' + white('cache')
        pass
    else:
        # compile
        print
        import dmraid
        dmraid.build_sequence(master_config, selinux, temp, verbose['std'])

    # FIXME careful with the > 
    os.system('/bin/bzip2 -dc %s/dmraid.static-%s.bz2 > %s/initramfs-dmraid-temp/bin/dmraid.static' % (temp['cache'], master_config['dmraid_ver'], temp['work']))
    utils.sprocessor('cp %s/initramfs-dmraid-temp/bin/dmraid.static %s/initramfs-dmraid-temp/bin/dmraid' % (temp['work'],temp['work']), verbose)

    # TODO ln -sf raid456.ko raid45.ko ?
    # TODO is it ok to have no raid456.ko? if so shouldn't we check .config for inkernel feat?
    #   or should we raise an error and make the user enabling the module manually? warning?
    
    os.chdir(temp['work']+'/initramfs-dmraid-temp')
    return os.system(append_cpio(temp))

# TODO: make sure somehow the appropriate modules get loaded when using iscsi?
def append_iscsi(master_config, temp, nocache, verbose):
    """
    Append iscsi to initramfs

    @arg master_config  dict
    @arg temp           dict
    @arg nocache        bool
    @arg verbose        dict

    @return: bool
    """
    logging.debug('initramfs.append_iscsi ' + master_config['iscsi_ver'])
    print green(' * ') + turquoise('initramfs.append_iscsi ') + master_config['iscsi_ver'],

    utils.sprocessor('mkdir -p ' + temp['work']+'/initramfs-iscsi-temp/bin', verbose)

    if os.path.isfile(temp['cache']+'/iscsistart-'+master_config['iscsi_ver']+'.bz2') and nocache is False:
        # use cache
        print 'from ' + white('cache')
    else:
        # compile
        print
        import iscsi
        iscsi.build_sequence(master_config, temp, verbose['std'])

    os.system('/bin/bzip2 -dc %s/iscsistart-%s.bz2 > %s/initramfs-iscsi-temp/bin/iscsistart' % (temp['cache'], master_config['iscsi_ver'], temp['work']))
    utils.sprocessor('chmod +x %s/initramfs-iscsi-temp/bin/iscsistart' % temp['work'], verbose)

    os.chdir(temp['work']+'/initramfs-iscsi-temp')
    return os.system(append_cpio(temp))

def append_splash(stheme, sres, master_config, temp, verbose):
    """
    Append splash framebuffer to initramfs

    @arg stheme         string
    @arg sres           string
    @arg master_config  dict
    @arg temp           dict
    @arg verbose        dict

    @return: bool
    """
    splash_geninitramfs_bin = '/usr/sbin/splash_geninitramfs'

    utils.sprocessor('mkdir -p ' + temp['work']+'/initramfs-splash-temp/', verbose)

    if os.path.isfile(splash_geninitramfs_bin):
        if stheme is '':
            # set default theme to gentoo
            stheme = 'gentoo'
            if os.path.isfile('/etc/conf.d/splash'):
                os.system('source /etc/conf.d/splash')
        if sres is not '':
            sres = '-r %s' % sres

        logging.debug('initramfs.append_splash ' + stheme + ' ' + sres)
        print green(' * ') + turquoise('initramfs.append_splash ') + white(stheme) + ' ' + white(sres)
        utils.sprocessor('splash_geninitramfs -c %s/initramfs-splash-temp %s %s' % (temp['work'], sres, stheme), verbose)

        if os.path.isfile('/usr/share/splashutils/initrd.splash'):
            utils.sprocessor('cp -f /usr/share/splashutils/initrd.splash %s/initramfs-splash-temp/etc' % temp['work'], verbose)
    else:
        logging.debug('ERR: media-gfx/splashutils is not emerged')
        print red('ERR')+ ': ' + "media-gfx/splashutils is not emerged"
        sys.exit(2)

    os.chdir(temp['work']+'/initramfs-splash-temp')
    return os.system(append_cpio(temp))

def append_unionfs_fuse(master_config, temp, nocache, verbose):
    """
    Append unionfs-fuse to initramfs
    
    @arg master_config  dict
    @arg temp       dict
    @arg nocache        bool
    @arg verbose        dict
    
    @return: bool
    """
    build_fuse(master_config, temp, nocache, verbose['std'])
    
    logging.debug('initramfs.append_unionfs_fuse ' + master_config['unionfs_fuse_ver'])
    print green(' * ') + turquoise('initramfs.append_unionfs_fuse ') + master_config['unionfs_fuse_ver'],

    if os.path.isfile(temp['cache']+'/unionfs-fuse.static-'+master_config['unionfs_fuse_ver']+'.bz2') and nocache is False:
        # use cache
        print 'from ' + white('cache')
    else:
        print
        # TODO: find a better check for fuse
        if os.path.isfile('/usr/include/fuse.h'):
            # compile
            import unionfs_fuse
            unionfs_fuse.build_sequence(master_config, temp, verbose['std'])
        else:
            logging.debug('ERR: sys-fs/fuse is not emerged')
            print red('ERR') + ': ' + "sys-fs/fuse is not emerged"
            print red('ERR') + ': ' + "we need libfuse"
            sys.exit(2)

    utils.sprocessor('mkdir -p ' + temp['work']+'/initramfs-unionfs-fuse-temp/sbin', verbose)
    # FIXME careful with the > passed to sprocessor()
    os.system('/bin/bzip2 -dc %s/unionfs-fuse.static-%s.bz2 > %s/initramfs-unionfs-fuse-temp/sbin/unionfs' % (temp['cache'], master_config['unionfs_fuse_ver'], temp['work']))
    os.system('chmod +x %s/initramfs-unionfs-fuse-temp/sbin/unionfs' % temp['work'])

    os.chdir(temp['work']+'/initramfs-unionfs-fuse-temp')
    return os.system(append_cpio(temp))

def append_aufs(master_config, temp, nocache, verbose):
    """
    Append aufs to initramfs
    """
    logging.debug('initramfs.append_aufs')
    print green(' * ') + turquoise('initramfs.append_aufs ')

    os.mkdir(temp['work']+'/initramfs-aufs-temp')

# TODO
# aufs is tricky: gotta patch the kernel sources
# then build aufs 
# then pack initrd
# then rebuild kernel not just bzImage

    os.chdir(temp['work']+'/initramfs-aufs-temp')
    return os.system(append_cpio(temp))

def append_ssh(master_config, libdir, temp, nocache, verbose):
    """
    Append ssh tools and daemon to initramfs
    """
    logging.debug('initramfs.append_ssh')
    print green(' * ') + turquoise('initramfs.append_ssh ') + master_config['ssh-version'],

    if os.path.isfile(temp['cache']+'/ssh-'+master_config['ssh-version']+'.tar') and nocache is False:
        # use cache
        print 'from ' + white('cache')
        pass
    else:
        # compile
        print
        import ssh
        ssh.build_sequence(master_config, temp, verbose)

    utils.sprocessor('mkdir -p ' + temp['work']+'/initramfs-ssh-temp/bin', verbose)
    utils.sprocessor('mkdir -p ' + temp['work']+'/initramfs-ssh-temp/sbin', verbose)
    os.chdir(temp['cache'])
    os.system('tar xf %s -C %s' % ('ssh-'+master_config['ssh-version']+'.tar', temp['work']+'/initramfs-ssh-temp'))
#    utils.sprocessor('chmod a+x %s/initramfs-ssh-temp/bin/sftp' % temp['work'], verbose)
#    utils.sprocessor('chmod a+x %s/initramfs-ssh-temp/bin/scp' % temp['work'], verbose)
#    utils.sprocessor('chmod a+x %s/initramfs-ssh-temp/sbin/sshd' % temp['work'], verbose)

    os.chdir(temp['work']+'/initramfs-ssh-temp')
    return os.system(append_cpio(temp))

