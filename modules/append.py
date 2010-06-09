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
                nocache):
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
        import kmodules
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
        modsyslist  = kmodules.get_sys_modules_list(self.KV)
        modconflist = kmodules.get_config_modules_list(self.master_config) #.split()
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
        modconfdict = kmodules.get_config_modules_dict(self.master_config)
    
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
        cryptsetup_bin  = '/bin/cryptsetupa'
        cryptsetup_sbin = '/sbin/cryptsetupa'
    
        utils.sprocessor('mkdir -p ' + self.temp['work']+'/initramfs-luks-temp/lib/luks', self.verbose)
        utils.sprocessor('mkdir -p ' + self.temp['work']+'/initramfs-luks-temp/sbin', self.verbose)
    
        if os.path.isfile(cryptsetup_bin):
            luks_host_version = commands.getoutput("cryptsetup --version | cut -d' ' -f2")
            logging.debug('initramfs.append.luks ' + luks_host_version + ' ' + cryptsetup_bin + ' from host')
            print green(' * ') + turquoise('initramfs.append.luks ') + luks_host_version + ' '  + white(cryptsetup_bin) + ' from host'
            utils.sprocessor('cp %s %s/initramfs-luks-temp/sbin' % (cryptsetup_bin, self.temp['work']), self.verbose)
            utils.sprocessor('chmod +x %s/initramfs-luks-temp/sbin/cryptsetup' % self.temp['work'], self.verbose)
        elif os.path.isfile(cryptsetup_sbin):
            luks_host_version = commands.getoutput("cryptsetup --version | cut -d' ' -f2")
            logging.debug('initramfs.append.luks ' + luks_host_version + ' ' + cryptsetup_sbin + ' from host')
            print green(' * ') + turquoise('initramfs.append.luks ') + luks_host_version + ' ' + white(cryptsetup_sbin) + ' from host'
            utils.sprocessor('cp %s %s/initramfs-luks-temp/sbin' % (cryptsetup_sbin, self.temp['work']), self.verbose)
            utils.sprocessor('chmod +x %s/initramfs-luks-temp/sbin/cryptsetup' % self.temp['work'], self.verbose)
        else:
            print green(' * ') + turquoise('initramfs.append.luks ') + self.master_config['luks-version'],
            logging.debug('initramfs.append_luks ' + self.master_config['luks-version'])
            if os.path.isfile(self.temp['cache']+'/cryptsetup-'+self.master_config['luks-version']+'.bz2') and self.nocache is False:
                # use cache
                print 'from ' + white('cache')
                # FIXME careful with the >
                os.system('/bin/bzip2 -dc %s/cryptsetup-%s.bz2 > %s/initramfs-luks-temp/sbin/cryptsetup' % (self.temp['cache'], self.master_config['luks-version'], self.temp['work']))
                utils.sprocessor('chmod a+x %s/initramfs-luks-temp/sbin/cryptsetup' % self.temp['work'], self.verbose)
            else:
                # compile and cache
                print
                import luks
                luks.build_sequence(self.master_config, self.temp, self.verbose)
    
        # FIXME careful with the >
#        os.system('/bin/bzip2 -dc %s/cryptsetup-%s.bz2 > %s/initramfs-luks-temp/sbin/cryptsetup' % (self.temp['cache'], self.master_config['luks-version'], self.temp['work']))
#        utils.sprocessor('chmod a+x %s/initramfs-luks-temp/sbin/cryptsetup' % self.temp['work'], self.verbose)
    
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
            print green(' * ') + turquoise('initramfs.append_splash ') + white(self.stheme) + ' ' + white(self.sres)
            utils.sprocessor('splash_geninitramfs -c %s/initramfs-splash-temp %s %s' % (self.temp['work'], self.sres, self.stheme), self.verbose)

            if os.path.isfile('/usr/share/splashutils/initrd.splash'):
                utils.sprocessor('cp -f /usr/share/splashutils/initrd.splash %s/initramfs-splash-temp/etc' % self.temp['work'], self.verbose)
        else:
            logging.debug('ERR: media-gfx/splashutils is not emerged')
            print red('ERR')+ ': ' + "media-gfx/splashutils is not emerged"
            sys.exit(2)
    
        os.chdir(self.temp['work']+'/initramfs-splash-temp')
        return os.system(self.cpio())
     
