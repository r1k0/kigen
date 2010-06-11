import os
import sys
from stdout import white, green, turquoise
import error
import warning
import utils
import logging
import commands

class append:

    def __init__(self,          \
                temp,           \
                KV,             \
                linuxrc,        \
                kernel_dir_opt, \
                arch,           \
                master_config,  \
                libdir,         \
                oldconfig,      \
                menuconfig,     \
                allyesconfig,   \
                mrproper,       \
                verbose,        \
                bbconf,         \
                busyboxprogs,   \
                bootupdateset,    \
                bootupdateinitrd, \
                stheme,         \
                sres,           \
                firmware,       \
                selinux,        \
                nocache,        \
                nohostbin):
        """
        init class variables
        """
        self.temp           = temp
        self.KV             = KV
        self.linuxrc        = linuxrc
        self.kernel_dir_opt = kernel_dir_opt
        self.arch           = arch
        self.master_config  = master_config
        self.libdir         = libdir
        self.oldconfig      = oldconfig
        self.menuconfig     = menuconfig
        self.allyesconfig   = allyesconfig
        self.mrproper       = mrproper
        self.verbose        = verbose
        self.bbconf         = bbconf
        self.busyboxprogs   = busyboxprogs
        self.bootupdateset    = bootupdateset
        self.bootupdateinitrd = bootupdateinitrd
        self.stheme         = stheme
        self.sres           = sres
        self.nocache        = nocache
        self.firmware       = firmware
        self.selinux        = selinux
        self.nohostbin      = nohostbin

    def cpio(self):
        """
        Builds command with correct path
    
        @return: string
        """
        cmd = 'find . -print | cpio --quiet -o -H newc --append -F %s/initramfs-cpio' % self.temp['cache']

        return cmd

    def base(self):
        """
        Append baselayout to the initramfs
    
        @return: bool
        """
        ret = int('0')
        logging.debug('initramfs.append.base')
        print green(' * ') + turquoise('initramfs.append.base'),
    
        # create the baselayout
        for i in ['dev', 'bin', 'etc', 'usr', 'proc', 'temp', 'sys', 'var/lock/dmraid', 'sbin', 'usr/bin', 'usr/sbin']:
            os.makedirs(self.temp['work']+'/initramfs-base-temp/%s' % i)
    
        os.chdir(self.kernel_dir_opt) # WHY? # TODO: change os.chdir by subprocess.popen(..., cwd=kernel_dir_opt
    
        # init
        if self.linuxrc is '':
        # TODO: copy linuxrc depending on arch
        # if netboot is True:
        #       cp "${GK_SHARE}/netboot/linuxrc.x" "${TEMP}/initramfs-aux-temp/init"
        # elif arch is 'x86':
        #       os.system('cp %s/arch/linuxrc %s/initramfs-base-temp/init' % (libdir, temp['work']))
        # elif arch is 'amd64':
        #       blablabla
            print
            utils.sprocessor('cp %s/defaults/linuxrc %s/initramfs-base-temp/init' % (self.libdir, self.temp['work']), self.verbose)
        else:
            # cp custom linuxrc to initramfs
            print white(self.linuxrc) + ' from host'
            utils.sprocessor('cp %s %s/initramfs-base-temp/init' % (self.linuxrc, self.temp['work']), self.verbose)
    
        # make init executable
        utils.sprocessor('chmod 0755 %s/initramfs-base-temp/init' % self.temp['work'], self.verbose)
    
        # link lib to lib64
        utils.sprocessor('ln -s lib %s/initramfs-base-temp/lib64' % self.temp['work'], self.verbose)
    
        # create fstab
        utils.srprocessor('echo /dev/ram0 / ext2 defaults 0 0\n > ' + self.temp['work']+'/initramfs-base-temp/etc/fstab', self.verbose)
        utils.arprocessor('echo proc /proc proc defaults 0 0\n >> ' + self.temp['work']+'/initramfs-base-temp/etc/fstab', self.verbose)
    
        os.chdir(self.temp['work']+'/initramfs-base-temp/dev')
    
        # create nodes
        utils.sprocessor('mknod -m 660 console c 5 1', self.verbose)
        utils.sprocessor('mknod -m 660 null    c 1 3', self.verbose)
        utils.sprocessor('mknod -m 660 tty1    c 4 1', self.verbose)
    
        # timestamp the build
        from time import strftime
        build_date = open(self.temp['work']+'/initramfs-base-temp/etc/build_date', 'w')
        build_date.writelines(strftime("%Y-%m-%d %H:%M:%S")+ '\n')
        build_date.close()
    
        # aux
        utils.sprocessor('mkdir -p ' + self.temp['work']+'/initramfs-base-temp/lib/keymaps', self.verbose)
        utils.sprocessor('tar -zxf %s/defaults/keymaps.tar.gz -C %s/initramfs-base-temp/lib/keymaps' % (self.libdir, self.temp['work']), self.verbose)
    
        os.chdir(self.temp['work']+'/initramfs-base-temp')
        utils.sprocessor('ln -s init linuxrc', self.verbose)
        utils.sprocessor('cp %s/defaults/initrd.scripts %s/initramfs-base-temp/etc/initrd.scripts' % (self.libdir, self.temp['work']), self.verbose)
        utils.sprocessor('cp %s/defaults/initrd.defaults %s/initramfs-base-temp/etc/initrd.defaults' % (self.libdir, self.temp['work']), self.verbose)
        # what's the harm to have it harcoded? even if the group is commented out in the config file the variable is still empty
        # same thinking for bootupdate it's already set in etc/initrd.defaults $HWOPTS
        utils.arprocessor("echo HWOPTS='$HWOPTS ataraid dmraid evms firewire fs iscsi lvm2 mdadm net pata pcmcia sata scsi usb waitscan' >> %s/initramfs-base-temp/etc/initrd.defaults" % self.temp['work'], self.verbose)
        utils.sprocessor('cp %s/defaults/modprobe %s/initramfs-base-temp/sbin/modprobe' % (self.libdir, self.temp['work']), self.verbose)
    
        os.chdir(self.temp['work']+'/initramfs-base-temp/sbin')
        utils.sprocessor('ln -s ../init init', self.verbose)
        utils.sprocessor('chmod +x %s/initramfs-base-temp/init' % self.temp['work'], self.verbose)
        utils.sprocessor('chmod +x %s/initramfs-base-temp/etc/initrd.scripts' % self.temp['work'], self.verbose)
        utils.sprocessor('chmod +x %s/initramfs-base-temp/etc/initrd.defaults' % self.temp['work'], self.verbose)
        utils.sprocessor('chmod +x %s/initramfs-base-temp/sbin/modprobe' % self.temp['work'], self.verbose)
    
        os.chdir(self.temp['work']+'/initramfs-base-temp/')
        return os.system(self.cpio())
   
    def busybox(self):
        """
        Append the busybox compiled objects to the initramfs
    
        @return: bool
        """
        import busybox
        ret = zero = int('0')
        logging.debug('initramfs.append.busybox')
        print green(' * ') + turquoise('initramfs.append.busybox ') + self.master_config['bb_ver'],
    
        if os.path.isfile(self.temp['cache']+'/busybox-bin-'+self.master_config['bb_ver']+'.tar.bz2') and self.nocache is False:
            # use cache
            print 'from ' + white('cache')
        else:
            print self.busyboxprogs
            # compile
            ret = busybox.build_sequence( self.arch, \
                        self.bbconf,                 \
                        self.master_config,          \
                        self.libdir,                 \
                        self.temp,                   \
                        self.oldconfig,              \
                        self.menuconfig,             \
                        self.allyesconfig,           \
                        self.mrproper,               \
                        self.verbose['std'])
        # append busybox to cpio
        utils.sprocessor('mkdir -p ' + self.temp['work']+'/initramfs-busybox-temp/bin', self.verbose)
        os.chdir(self.temp['work']+'/initramfs-busybox-temp')
        utils.sprocessor('tar -xjf %s/busybox-bin-%s.tar.bz2 -C %s busybox' % (self.temp['cache'], self.master_config['bb_ver'], self.temp['work']+'/initramfs-busybox-temp/bin'), self.verbose)
        utils.sprocessor('chmod +x %s/busybox' % (self.temp['work']+'/initramfs-busybox-temp/bin'), self.verbose)
        utils.sprocessor('mkdir -p  %s/usr/share/udhcpc/' % (self.temp['work']+'/initramfs-busybox-temp'), self.verbose)
        utils.sprocessor('cp %s/defaults/udhcpc.scripts %s/initramfs-busybox-temp/usr/share/udhcpc/default.script' % (self.libdir, self.temp['work']), self.verbose)
        utils.sprocessor('chmod +x %s/initramfs-busybox-temp/usr/share/udhcpc/default.script' % self.temp['work'], self.verbose)
    
        for i in self.busyboxprogs.split():
            utils.sprocessor('ln -s busybox %s/initramfs-busybox-temp/bin/%s' % (self.temp['work'], i), self.verbose)
    
        os.chdir(self.temp['work']+'/initramfs-busybox-temp')
        if ret is zero:
            return os.system(self.cpio())

    def modules(self):
        """
        Find system modules and config modules
        Append modules to the initramfs
    
        @return: bool
        """
        ret = int('0')
        logging.debug('initramfs.append_modules ' + self.KV)
        print green(' * ') + turquoise('initramfs.append.modules ') + self.KV
    
        utils.sprocessor('mkdir -p ' + self.temp['work']+'/initramfs-modules-'+self.KV+'-temp/lib/modules/'+self.KV, self.verbose)
    
        # FIXME: ctrl c does not work during this function
        # TODO: rewrite (later)
        # TODO: maybe |uniq the list? in case the user sets 
        # multiple times the same module in different groups
        #
        # is it really a big deal? I don't think so
    
        # identify and copy kernel modules
        modsyslist  = utils.get_sys_modules_list(self.KV)
        modconflist = utils.get_config_modules_list(self.master_config) #.split()
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
                    module = os.popen('find /lib/modules/'+self.KV+' -name '+k+' 2>/dev/null | head -n 1').read().strip()
                    module_dirname = os.path.dirname(module)
                    utils.sprocessor('mkdir -p %s%s%s'% (self.temp['work'],'/initramfs-modules-'+self.KV+'-temp',  module_dirname), self.verbose)
                    utils.sprocessor('cp -ax %s %s/initramfs-modules-%s-temp/%s' % (module, self.temp['work'], self.KV, module_dirname), self.verbose)
    
        # for each module in /etc/boot.conf
        if "load-modules" in self.bootupdateinitrd:
            for i in self.bootupdateinitrd['load-modules'].split():
                for j in modsyslist:
                    k = i +'.ko'
                    if k == j:
                        logging.debug('shipping ' + i + ' from /etc/boot.conf')
                        print green(' * ') + '... ' + white(i) + ' from /etc/boot.conf'
                        module = os.popen('find /lib/modules/'+self.KV+' -name '+k+' 2>/dev/null | head -n 1').read().strip()
                        module_dirname = os.path.dirname(module)
                        utils.sprocessor('mkdir -p %s%s%s'% (self.temp['work'],'/initramfs-modules-'+self.KV+'-temp',  module_dirname), self.verbose)
                        utils.sprocessor('cp -ax %s %s/initramfs-modules-%s-temp/%s' % (module, self.temp['work'], self.KV, module_dirname), self.verbose)
    
        # TODO: make variable of /lib/modules in case of FAKEROOT export
        os.system('cp /lib/modules/%s/modules.* %s' % (self.KV, self.temp['work']+'/initramfs-modules-'+self.KV+'-temp/lib/modules/'+self.KV ))
    
        # create etc/modules/<group>
        utils.sprocessor('mkdir -p ' + self.temp['work']+'/initramfs-modules-'+self.KV+'-temp/etc/modules', self.verbose)
        modconfdict = utils.get_config_modules_dict(self.master_config)
    
        # Genkernel official boot module design
        # for each key value in the module config dictionary
        for k, v in modconfdict.iteritems():
            # match the group for which the module belongs
            k = k.lower()
            group = k.split('_')[1]
            # and add it etc/modules/
            f = open(self.temp['work']+'/initramfs-modules-'+self.KV+'-temp/etc/modules/'+group, 'w')
            f.write(v.replace(" ", "\n"))
            f.close
    
        # Funtoo bootupdate initramfs module file config
        if "load-modules" in self.bootupdateinitrd:
            for o in self.bootupdateinitrd['load-modules'].split():
                # FIXME think about >> passed to sprocessor?
                utils.arprocessor('echo %s >> %s' % (o, self.temp['work']+'/initramfs-modules-'+self.KV+'-temp/etc/modules/bootupdate'), self.verbose)
    
        os.chdir(self.temp['work']+'/initramfs-modules-'+self.KV+'-temp')
        return os.system(self.cpio())
 
    def luks(self):
        """
        Append the LUKS static binary to the initramfs
    
        @return: bool
        """
        ret = int('0')
        cryptsetup_bin  = '/bin/cryptsetup'
        cryptsetup_sbin = '/sbin/cryptsetup'
    
        utils.sprocessor('mkdir -p ' + self.temp['work']+'/initramfs-luks-temp/lib/luks', self.verbose)
        utils.sprocessor('mkdir -p ' + self.temp['work']+'/initramfs-luks-temp/sbin', self.verbose)
    
        if os.path.isfile(cryptsetup_bin) and self.nohostbin is False:
            luks_host_version = commands.getoutput("cryptsetup --version | cut -d' ' -f2")
            logging.debug('initramfs.append.luks ' + luks_host_version + ' ' + cryptsetup_bin + ' from host')
            print green(' * ') + turquoise('initramfs.append.luks ') + luks_host_version + ' '  + white(cryptsetup_bin) + ' from host'
            utils.sprocessor('cp %s %s/initramfs-luks-temp/sbin' % (cryptsetup_bin, self.temp['work']), self.verbose)
            utils.sprocessor('chmod +x %s/initramfs-luks-temp/sbin/cryptsetup' % self.temp['work'], self.verbose)
        elif os.path.isfile(cryptsetup_sbin) and self.nohostbin is False:
            luks_host_version = commands.getoutput("cryptsetup --version | cut -d' ' -f2")
            logging.debug('initramfs.append.luks ' + luks_host_version + ' ' + cryptsetup_sbin + ' from host')
            print green(' * ') + turquoise('initramfs.append.luks ') + luks_host_version + ' ' + white(cryptsetup_sbin) + ' from host'
            utils.sprocessor('cp %s %s/initramfs-luks-temp/sbin' % (cryptsetup_sbin, self.temp['work']), self.verbose)
            utils.sprocessor('chmod +x %s/initramfs-luks-temp/sbin/cryptsetup' % self.temp['work'], self.verbose)
        elif self.nohostbin is True:
            print green(' * ') + turquoise('initramfs.append.luks ') + self.master_config['luks-version'],
            logging.debug('initramfs.append_luks ' + self.master_config['luks-version'])
            if os.path.isfile(self.temp['cache']+'/cryptsetup-'+self.master_config['luks-version']+'.bz2') and self.nocache is False:
                # use cache
                print 'from ' + white('cache')

                # extract cache
                # FIXME careful with the >
                os.system('/bin/bzip2 -dc %s/cryptsetup-%s.bz2 > %s/initramfs-luks-temp/sbin/cryptsetup' % (self.temp['cache'], self.master_config['luks-version'], self.temp['work']))
                utils.sprocessor('chmod a+x %s/initramfs-luks-temp/sbin/cryptsetup' % self.temp['work'], self.verbose)

            else:
                # compile and cache
                print
                from luks import luks
                luksobj = luks(self.master_config, self.temp, self.verbose)
                luksobj.build()

                # extract cache
                # FIXME careful with the >
                os.system('/bin/bzip2 -dc %s/cryptsetup-%s.bz2 > %s/initramfs-luks-temp/sbin/cryptsetup' % (self.temp['cache'], self.master_config['luks-version'], self.temp['work']))
                utils.sprocessor('chmod a+x %s/initramfs-luks-temp/sbin/cryptsetup' % self.temp['work'], self.verbose)

        os.chdir(self.temp['work']+'/initramfs-luks-temp')
        return os.system(self.cpio())
     
    def e2fsprogs(self):
        """
        Append blkid binary to the initramfs
        after compiling e2fsprogs
        
        @return: bool
        """
        logging.debug('initramfs.append.e2fsprogs ' + self.master_config['e2fsprogs-version'])
        print green(' * ') + turquoise('initramfs.append.e2fsprogs ') + self.master_config['e2fsprogs-version'],
    
        if os.path.isfile(self.temp['cache'] + '/blkid-e2fsprogs-' + self.master_config['e2fsprogs-version']+'.bz2') and self.nocache is False:
            # use cache
            print 'from ' + white('cache')
        else:
            # compile
            print
            import e2fsprogs
            e2fsprogs.build_sequence(self.master_config, self.temp, self.verbose)
    
        utils.sprocessor('mkdir -p ' + self.temp['work']+'/initramfs-blkid-temp/bin', self.verbose)
    
        # FIXME careful with the >
        os.system('/bin/bzip2 -dc %s/blkid-e2fsprogs-%s.bz2 > %s/initramfs-blkid-temp/bin/blkid' % (self.temp['cache'], self.master_config['e2fsprogs-version'], self.temp['work']))
        #utils.srprocessor('/bin/bzip2 -dc %s/blkid-e2fsprogs-%s.bz2 > %s/initramfs-blkid-temp/bin/blkid' % (temp['cache'], master_config['e2fsprogs_ver'], temp['work']), verbose)
        utils.sprocessor('chmod a+x %s/initramfs-blkid-temp/bin/blkid' % self.temp['work'], self.verbose)
    
        os.chdir(self.temp['work']+'/initramfs-blkid-temp')
        return os.system(self.cpio())

    def splash(self):
        """
        Append splash framebuffer to initramfs
    
        @return: bool
        """
        splash_geninitramfs_bin = '/usr/sbin/splash_geninitramfs'
    
        utils.sprocessor('mkdir -p ' + self.temp['work']+'/initramfs-splash-temp/', self.verbose)
    
        if os.path.isfile(splash_geninitramfs_bin):
            if self.stheme is '':
                # set default theme to gentoo
                self.stheme = 'gentoo'
                if os.path.isfile('/etc/conf.d/splash'):
                    os.system('source /etc/conf.d/splash')
            if self.sres is not '':
                self.sres = '-r %s' % self.sres
    
            logging.debug('initramfs.append.splash ' + self.stheme + ' ' + self.sres)
            print green(' * ') + turquoise('initramfs.append.splash ') + white(self.stheme) + ' ' + white(self.sres)
            utils.sprocessor('splash_geninitramfs -c %s/initramfs-splash-temp %s %s' % (self.temp['work'], self.sres, self.stheme), self.verbose)

            if os.path.isfile('/usr/share/splashutils/initrd.splash'):
                utils.sprocessor('cp -f /usr/share/splashutils/initrd.splash %s/initramfs-splash-temp/etc' % self.temp['work'], self.verbose)
        else:
            logging.debug('ERR: media-gfx/splashutils is not emerged')
            print red('ERR')+ ': ' + "media-gfx/splashutils is not emerged"
            sys.exit(2)
    
        os.chdir(self.temp['work']+'/initramfs-splash-temp')
        return os.system(self.cpio())
     
    def lvm2(self):
        """
        Append lvm2 static binary first to the initramfs
    
        @return: bool
        """
        ret = int('0')
        lvm2_static_bin = '/sbin/lvm.statica'
        lvm2_bin        = '/sbin/lvma'
    
        utils.sprocessor('mkdir -p ' + self.temp['work']+'/initramfs-lvm2-temp/etc/lvm', self.verbose)
        utils.sprocessor('mkdir -p ' + self.temp['work']+'/initramfs-lvm2-temp/bin', self.verbose)
    
        if os.path.isfile(lvm2_static_bin):
            # TODO see if we can use something else than import commands
            #lvm2_static_version = commands.getoutput("lvm.static version | cut -d: -f2 | head -n1 | cut -d'(' -f1")
            logging.debug('initramfs.append.lvm2 ' + ' ' + lvm2_static_bin + ' from host')
            print green(' * ') + turquoise('initramfs.append.lvm2 ') + white(lvm2_static_bin) + ' from host'
            utils.sprocessor('cp %s %s/initramfs-lvm2-temp/bin/lvm' % (lvm2_static_bin, self.temp['work']), self.verbose)
        elif os.path.isfile(lvm2_bin):
            logging.debug('initramfs.append.lvm2 ' + lvm2_bin + ' from host')
            print green(' * ') + turquoise('initramfs.append.lvm2 ') + white(lvm2_bin) + ' from host'
            utils.sprocessor('cp %s %s/initramfs-lvm2-temp/bin/lvm' % (lvm2_bin, self.temp['work']), self.verbose)
        else:
            self.build_device_mapper()
    
            logging.debug('initramfs.append.lvm2 ')
            print green(' * ') + turquoise('initramfs.append.lvm2 ')
    
            import lvm2
            lvm2.build_sequence(self.master_config, self.temp, self.verbose)
    
            utils.sprocessor('bzip2 -d %s' % self.temp['cache']+'/lvm.static-'+self.master_config['lvm2-version']+'.bz2', self.verbose)
            utils.sprocessor('cp %s/lvm.static-%s %s/initramfs-lvm2-temp/bin/lvm' % (self.temp['cache'], self.master_config['lvm2-version'], self.temp['work']), self.verbose)
    
        if os.path.isfile(lvm2_static_bin) or os.path.isfile(lvm2_bin):
            utils.sprocessor('cp /etc/lvm/lvm.conf %s/initramfs-lvm2-temp/etc/lvm/' % self.temp['work'], self.verbose)
    
        os.chdir(self.temp['work']+'/initramfs-lvm2-temp')
        return os.system(self.cpio())

    def build_device_mapper(self):
        """
        Build the device-mapper and cache it for later use
        Only to be called if lvm2 or dmraid is compiled!
    
        @return: bool
        """
        logging.debug('initramfs.append.build_device_mapper '+self.master_config['dm_ver'])
        print green(' * ') + turquoise('initramfs.append.build_device_mapper ') + self.master_config['dm_ver'],
    
        if os.path.isfile(self.temp['cache']+'/device-mapper-'+self.master_config['dm_ver']+'.tar.bz2') and self.nocache is False:
            # use cache
            print 'from ' + white('cache')
            return
        else:
            # compile and cache
            print
            import device_mapper
            return device_mapper.build_sequence(self.master_config, self.temp, self.verbose['std'])
     
    def evms(self):
        """
        Append evms libraries to the initramfs
    
        @return: bool
        """
        logging.debug('initramfs.append.evms')
        print green(' * ') + turquoise('initramfs.append.evms'),
    
        if os.path.isfile('/sbin/evms'):
            print 'feeding' + ' from host'
    
            utils.sprocessor('mkdir -p ' + self.temp['work']+'/initramfs-evms-temp/lib/evms', self.verbose)
            utils.sprocessor('mkdir -p ' + self.temp['work']+'/initramfs-evms-temp/etc', self.verbose)
            utils.sprocessor('mkdir -p ' + self.temp['work']+'/initramfs-evms-temp/bin', self.verbose)
            utils.sprocessor('mkdir -p ' + self.temp['work']+'/initramfs-evms-temp/sbin', self.verbose)
    
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
    
        os.chdir(self.temp['work']+'/initramfs-evms-temp')
        return os.system(self.cpio())
    
    def firmware(self):
        """
        Append firmware to the initramfs
    
        @return: bool
        """
        logging.debug('initramfs.append_firmware ' + self.firmware + ' from host')
        print green(' * ') + turquoise('initramfs.append_firmware ') + white(self.firmware) + ' from host'
    
        utils.sprocessor('mkdir -p ' + temp['work']+'/initramfs-firmware-temp/lib/firmware', self.verbose)
        utils.sprocessor('cp -a %s %s/initramfs-firmware-temp/lib/' % (self.firmware, self.temp['work']), self.verbose)
    
        os.chdir(temp['work']+'/initramfs-firmware-temp')
        return os.system(self.cpio())
    
    def mdadm(self):
        """
        Append mdadm to initramfs
    
        @return: bool
        """
        ret = int('0')
        logging.debug('initramfs.append.mdadm')
        print green(' * ') + turquoise('initramfs.append.mdadm')
    
        utils.sprocessor('mkdir -p ' + self.temp['work']+'/initramfs-dmadm-temp/etc', self.verbose)
        utils.sprocessor('cp -a /etc/mdadm.conf %s/initramfs-mdadm-temp/etc' % self.temp['work'], self.verbose)
    
        os.chdir(self.temp['work']+'/initramfs-mdadm-temp')
        return os.system(self.cpio())

    def dmraid(self):
        """
        Append dmraid to initramfs
    
        @return: bool
        """
        self.build_device_mapper()
    
        logging.debug('initramfs.append.dmraid ' + self.master_config['dmraid_ver'])
        print green(' * ') + turquoise('initramfs.append.dmraid ') + self.master_config['dmraid_ver'],
    
        utils.sprocessor('mkdir -p ' + self.temp['work']+'/initramfs-dmraid-temp/bin', self.verbose)
    
        if os.path.isfile(self.temp['cache']+'/dmraid.static-'+self.master_config['dmraid_ver']+'.bz2') and self.nocache is False:
        # use cache
            print 'from ' + white('cache')
            pass
        else:
            # compile
            print
            import dmraid
            dmraid.build_sequence(self.master_config, self.selinux, self.temp, self.verbose['std'])
    
        # FIXME careful with the > 
        os.system('/bin/bzip2 -dc %s/dmraid.static-%s.bz2 > %s/initramfs-dmraid-temp/bin/dmraid.static' % (self.temp['cache'], self.master_config['dmraid_ver'], self.temp['work']))
        utils.sprocessor('cp %s/initramfs-dmraid-temp/bin/dmraid.static %s/initramfs-dmraid-temp/bin/dmraid' % (self.temp['work'],self.temp['work']), self.verbose)
    
        # TODO ln -sf raid456.ko raid45.ko ?
        # TODO is it ok to have no raid456.ko? if so shouldn't we check .config for inkernel feat?
        #   or should we raise an error and make the user enabling the module manually? warning?
    
        os.chdir(self.temp['work']+'/initramfs-dmraid-temp')
        return os.system(self.cpio())

    # TODO: make sure somehow the appropriate modules get loaded when using iscsi?
    def iscsi(self):
        """
        Append iscsi to initramfs
    
        @return: bool
        """
        logging.debug('initramfs.append.iscsi ' + self.master_config['iscsi_ver'])
        print green(' * ') + turquoise('initramfs.append.iscsi ') + self.master_config['iscsi_ver'],
    
        utils.sprocessor('mkdir -p ' + self.temp['work']+'/initramfs-iscsi-temp/bin', self.verbose)
    
        if os.path.isfile(self.temp['cache']+'/iscsistart-'+self.master_config['iscsi_ver']+'.bz2') and self.nocache is False:
            # use cache
            print 'from ' + white('cache')
        else:
            # compile
            print
            import iscsi
            iscsi.build_sequence(self.master_config, self.temp, self.verbose['std'])
    
        os.system('/bin/bzip2 -dc %s/iscsistart-%s.bz2 > %s/initramfs-iscsi-temp/bin/iscsistart' % (self.temp['cache'], self.master_config['iscsi_ver'], self.temp['work']))
        utils.sprocessor('chmod +x %s/initramfs-iscsi-temp/bin/iscsistart' % self.temp['work'], self.verbose)
    
        os.chdir(self.temp['work']+'/initramfs-iscsi-temp')
        return os.system(self.cpio())
    
    def unionfs_fuse(self):
        """
        Append unionfs-fuse to initramfs
        
        @return: bool
        """
        self.build_fuse()
    
        logging.debug('initramfs.append.unionfs_fuse ' + self.master_config['unionfs_fuse_ver'])
        print green(' * ') + turquoise('initramfs.append.unionfs_fuse ') + self.master_config['unionfs_fuse_ver'],
    
        if os.path.isfile(self.temp['cache']+'/unionfs-fuse.static-'+self.master_config['unionfs_fuse_ver']+'.bz2') and self.nocache is False:
            # use cache
            print 'from ' + white('cache')
        else:
            print
            # TODO: find a better check for fuse
            if os.path.isfile('/usr/include/fuse.h'):
                # compile
                import unionfs_fuse
                unionfs_fuse.build_sequence(self.master_config, self.temp, self.verbose)
            else:
                logging.debug('ERR: sys-fs/fuse is not emerged')
                print red('ERR') + ': ' + "sys-fs/fuse is not emerged"
                print red('ERR') + ': ' + "we need libfuse"
                sys.exit(2)
    
        utils.sprocessor('mkdir -p ' + self.temp['work']+'/initramfs-unionfs-fuse-temp/sbin', self.verbose)
        # FIXME careful with the > passed to sprocessor()
        os.system('/bin/bzip2 -dc %s/unionfs-fuse.static-%s.bz2 > %s/initramfs-unionfs-fuse-temp/sbin/unionfs' % (self.temp['cache'], self.master_config['unionfs_fuse_ver'], self.temp['work']))
        os.system('chmod +x %s/initramfs-unionfs-fuse-temp/sbin/unionfs' % self.temp['work'])
    
        os.chdir(self.temp['work']+'/initramfs-unionfs-fuse-temp')
        return os.system(self.cpio())
     
    def build_fuse(self):
        """
        Build fuse and cache it for later use
        Only to be called for --unionfs!
    
        @return: bool
        """
        logging.debug('initramfs.build_fuse ' + self.master_config['fuse_ver'])
        print green(' * ') + turquoise('initramfs.build_fuse ') +self.master_config['fuse_ver'],
    
        if os.path.isfile(self.temp['cache']+'/fuse-dircache-'+self.master_config['fuse_ver']+'.tar.bz2') and self.nocache is False:
            # use cache
            print 'from ' + white('cache')
        else:
            # compile and cache
            print
            import fuse
            fuse.build_sequence(self.master_config, self.temp, self.verbose)
    
        # extract
        os.system('tar xfj %s -C %s' % (self.temp['cache']+'/fuse-dircache-'+self.master_config['fuse_ver']+'.tar.bz2', self.temp['work']))
    
        return
    
    def aufs(self):
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
    
        os.chdir(self.temp['work']+'/initramfs-aufs-temp')
        return os.system(self.cpio())
    
    def ssh(self):
        """
        Append ssh tools and daemon to initramfs
        """
        logging.debug('initramfs.append.ssh')
        print green(' * ') + turquoise('initramfs.append.ssh ') + self.master_config['ssh-version'],
    
        if os.path.isfile(self.temp['cache']+'/ssh-'+self.master_config['ssh-version']+'.tar') and self.nocache is False:
            # use cache
            print 'from ' + white('cache')
            pass
        else:
            # compile
            print
            import ssh
            ssh.build_sequence(self.master_config, self.temp, self.verbose)
    
        utils.sprocessor('mkdir -p ' + self.temp['work']+'/initramfs-ssh-temp/bin', self.verbose)
        utils.sprocessor('mkdir -p ' + self.temp['work']+'/initramfs-ssh-temp/sbin', self.verbose)
        os.chdir(self.temp['cache'])
        os.system('tar xf %s -C %s' % ('ssh-'+self.master_config['ssh-version']+'.tar', self.temp['work']+'/initramfs-ssh-temp'))
    #    utils.sprocessor('chmod a+x %s/initramfs-ssh-temp/bin/sftp' % temp['work'], verbose)
    #    utils.sprocessor('chmod a+x %s/initramfs-ssh-temp/bin/scp' % temp['work'], verbose)
    #    utils.sprocessor('chmod a+x %s/initramfs-ssh-temp/sbin/sshd' % temp['work'], verbose)
    
        os.chdir(self.temp['work']+'/initramfs-ssh-temp')
        return os.system(self.cpio())
    
