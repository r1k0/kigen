import os
import sys
import logging
import commands
from stdout import *
from utils.shell import *
from utils.misc import *

class append:

    def __init__(self,              \
                temp,               \
                KV,                 \
                linuxrc,            \
                kernel_dir_opt,     \
                arch,               \
                master_config,      \
                libdir,             \
                defconfig,          \
                oldconfig,          \
                menuconfig,         \
                mrproper,           \
                verbose,            \
                bbconf,             \
                busyboxprogs,       \
                bootupdateset,      \
                bootupdateinitrd,   \
                stheme,             \
                sres,               \
                sinitrd,            \
                firmware,           \
                selinux,            \
                nocache,            \
                hostbin,            \
                rootpasswd):
        """
        init class variables
        """
        self.temp               = temp
        self.KV                 = KV
        self.linuxrc            = linuxrc # list
        self.kernel_dir_opt     = kernel_dir_opt
        self.arch               = arch
        self.master_config      = master_config
        self.libdir             = libdir
        self.defconfig          = defconfig
        self.oldconfig          = oldconfig
        self.menuconfig         = menuconfig
        self.mrproper           = mrproper
        self.verbose            = verbose
        self.bbconf             = bbconf
        self.busyboxprogs       = busyboxprogs
        self.bootupdateset      = bootupdateset
        self.bootupdateinitrd   = bootupdateinitrd
        self.stheme             = stheme
        self.sres               = sres
        self.sinitrd            = sinitrd
        self.nocache            = nocache
        self.firmware           = firmware
        self.selinux            = selinux
        self.hostbin            = hostbin
        self.rootpasswd         = rootpasswd

    def cpio(self):
        """
        Builds command with correct path
    
        @return: string
        """
        cmd = 'find . -print | cpio --quiet -o -H newc --append -F %s/initramfs-cpio' % self.temp['cache']

        return cmd

    def fail(self, msg):
        """
        @arg step   string

        @return     exit
        """
        logging.debug('error'+msg)
        print red('error')+': '+msg
        sys.exit(2)

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
            print 'Gentoo linuxrc 3.4.10.907-r2'
            # this is Gentoo official linuxrc suite (see genkernel)
            process('cp %s/defaults/linuxrc %s/initramfs-base-temp/init' % (self.libdir, self.temp['work']), self.verbose)
            process('cp %s/defaults/initrd.scripts %s/initramfs-base-temp/etc/' % (self.libdir, self.temp['work']), self.verbose)
            process('cp %s/defaults/initrd.defaults %s/initramfs-base-temp/etc/' % (self.libdir, self.temp['work']), self.verbose)
            process('chmod +x %s/initramfs-base-temp/etc/initrd.scripts' % self.temp['work'], self.verbose)
            process('chmod +x %s/initramfs-base-temp/etc/initrd.defaults' % self.temp['work'], self.verbose)
        else:
            linuxrclist = self.linuxrc.split(',')
            print str(linuxrclist) + ' from ' + white('host')
            # copy first the linuxrc to /init
            if os.path.isfile(linuxrclist[0]):
                process('cp %s %s/initramfs-base-temp/init' % (linuxrclist[0], self.temp['work']), self.verbose)
            else:
                self.fail('%s does not exist.')
            # then all possible files
            for i in linuxrclist[1:]:
                if os.path.isfile(i):
                    process('cp %s %s/initramfs-base-temp/etc' % (i, self.temp['work']), self.verbose)
                    process('chmod +x %s/initramfs-base-temp/etc/%s' % (self.temp['work'], os.path.basename(i)), self.verbose)
                else:
                    self.fail('%s does not exist.' % i)
    
        # make init executable
        process('chmod 0755 %s/initramfs-base-temp/init' % self.temp['work'], self.verbose)
    
        # link lib to lib64
        process('ln -s lib %s/initramfs-base-temp/lib64' % self.temp['work'], self.verbose)
    
        # create fstab
        process_redir('echo /dev/ram0 / ext2 defaults 0 0\n > ' + self.temp['work']+'/initramfs-base-temp/etc/fstab', self.verbose)
        process_append('echo proc /proc proc defaults 0 0\n >> ' + self.temp['work']+'/initramfs-base-temp/etc/fstab', self.verbose)
    
        os.chdir(self.temp['work']+'/initramfs-base-temp/dev')
    
        # create nodes
        process('mknod -m 660 console c 5 1', self.verbose)
        process('mknod -m 660 null    c 1 3', self.verbose)
        process('mknod -m 600 tty1    c 4 1', self.verbose)
    
        # timestamp the build
        from time import strftime
        build_date = open(self.temp['work']+'/initramfs-base-temp/etc/build_date', 'w')
        build_date.writelines(strftime("%Y-%m-%d %H:%M:%S")+ '\n')
        build_date.close()
    
        # aux
        os.makedirs(self.temp['work']+'/initramfs-base-temp/lib/keymaps')
        process('tar -zxf %s/defaults/keymaps.tar.gz -C %s/initramfs-base-temp/lib/keymaps' % (self.libdir, self.temp['work']), self.verbose)
    
        os.chdir(self.temp['work']+'/initramfs-base-temp')

        # link linuxrc to /init
        process('ln -s init linuxrc', self.verbose)

        # what's the harm to have it harcoded? even if the group is commented out in the config file the variable is still empty
        # same thinking for bootupdate it's already set in etc/initrd.defaults $HWOPTS
        process_append("echo HWOPTS='$HWOPTS ataraid dmraid evms firewire fs iscsi lvm2 mdadm net pata pcmcia sata scsi usb waitscan' >> %s/initramfs-base-temp/etc/initrd.defaults" % self.temp['work'], self.verbose)

        process('cp %s/defaults/modprobe %s/initramfs-base-temp/sbin/modprobe' % (self.libdir, self.temp['work']), self.verbose)
        process('chmod +x %s/initramfs-base-temp/sbin/modprobe' % self.temp['work'], self.verbose)

        os.chdir(self.temp['work']+'/initramfs-base-temp/sbin')
        process('ln -s ../init init', self.verbose)
        process('chmod +x %s/initramfs-base-temp/init' % self.temp['work'], self.verbose)

        os.chdir(self.temp['work']+'/initramfs-base-temp/')
        return os.system(self.cpio())
   
    def busybox(self):
        """
        Append the busybox compiled objects to the initramfs
    
        @return: bool
        """
        ret = zero = int('0')
        logging.debug('initramfs.append.busybox')
        print green(' * ') + turquoise('initramfs.append.busybox ') + self.master_config['busybox-version'],
    
        if os.path.isfile(self.temp['cache']+'/busybox-bin-'+self.master_config['busybox-version']+'.tar.bz2') and self.nocache is False:
            # use cache
            print 'from ' + white('cache')
        else:
            print self.busyboxprogs
            # compile
            from busybox import busybox
            bbobj = busybox( self.arch, \
                        self.bbconf,                 \
                        self.master_config,          \
                        self.libdir,                 \
                        self.temp,                   \
                        self.defconfig,              \
                        self.oldconfig,              \
                        self.menuconfig,             \
                        self.mrproper,               \
                        self.verbose)
            bbobj.build()

        # append busybox to cpio
        os.makedirs(self.temp['work']+'/initramfs-busybox-temp/bin')
        os.makedirs(self.temp['work']+'/initramfs-busybox-temp/usr/share/udhcpc/')

        os.chdir(self.temp['work']+'/initramfs-busybox-temp')
        process('tar -xjf %s/busybox-bin-%s.tar.bz2 -C %s busybox' % (self.temp['cache'], self.master_config['busybox-version'], self.temp['work']+'/initramfs-busybox-temp/bin'), self.verbose)
        process('chmod +x %s/busybox' % (self.temp['work']+'/initramfs-busybox-temp/bin'), self.verbose)
        process('cp %s/defaults/udhcpc.scripts %s/initramfs-busybox-temp/usr/share/udhcpc/default.script' % (self.libdir, self.temp['work']), self.verbose)
        process('chmod +x %s/initramfs-busybox-temp/usr/share/udhcpc/default.script' % self.temp['work'], self.verbose)

        # FIXME: should be removed but wait!
        # we don't need it due to busybox --install -s from the /linuxrc
        # testcase: i see them auto symlinked on boot because /linuxrc is called
        # and then I ctrl+C luks auth to gain a shell
        # but so far, /linuxrc has run and busybox --install -s is called
        # problem: what if /linuxrc is not called and I get a shell? will i miss my symlinks?
        # answer: yes!
        for i in self.busyboxprogs.split():
            process('ln -s busybox %s/initramfs-busybox-temp/bin/%s' % (self.temp['work'], i), self.verbose)
    
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
    
        os.makedirs(self.temp['work']+'/initramfs-modules-'+self.KV+'-temp/lib/modules/'+self.KV)
    
        # FIXME: ctrl c does not work during this function
        # TODO: rewrite (later)
        # TODO: maybe |uniq the list? in case the user sets 
        # multiple times the same module in different groups
        #
        # is it really a big deal? I don't think so
    
        # identify and copy kernel modules
        modsyslist  = get_sys_modules_list(self.KV)
        modconflist = get_config_modules_list(self.master_config) #.split()
        # TODO: add support for the 'probe' key
    
        # for each module in the list modconflist
        for i in modconflist.split():
            for j in modsyslist:
                k = i +'.ko'
                # check for a match
                if k == j:
                    logging.debug('shipping ' + i)
                    print green(' * ') + '... ' + i
                    # if the module is found copy it
                    module = os.popen('find /lib/modules/'+self.KV+' -name '+k+' 2>/dev/null | head -n 1').read().strip()
                    module_dirname = os.path.dirname(module)
                    process('mkdir -p %s' % self.temp['work'] + '/initramfs-modules-' + self.KV + '-temp' + module_dirname, self.verbose)
                    process('cp -ax %s %s/initramfs-modules-%s-temp/%s' % (module, self.temp['work'], self.KV, module_dirname), self.verbose)
   
        # FUNTOO: for each module in /etc/boot.conf
        if "load-modules" in self.bootupdateinitrd:
            for i in self.bootupdateinitrd['load-modules'].split():
                for j in modsyslist:
                    k = i +'.ko'
                    if k == j:
                        logging.debug('shipping ' + i + ' from /etc/boot.conf')
                        print green(' * ') + '... ' + white(i) + ' from /etc/boot.conf'
                        module = os.popen('find /lib/modules/'+self.KV+' -name '+k+' 2>/dev/null | head -n 1').read().strip()
                        module_dirname = os.path.dirname(module)
                        process('mkdir -p %s' % self.temp['work'] + '/initramfs-modules-' + self.KV + '-temp' + module_dirname, self.verbose)
                        process('cp -ax %s %s/initramfs-modules-%s-temp/%s' % (module, self.temp['work'], self.KV, module_dirname), self.verbose)
    
        # TODO: make variable of /lib/modules in case of FAKEROOT export
        os.system('cp /lib/modules/%s/modules.* %s' % (self.KV, self.temp['work']+'/initramfs-modules-'+self.KV+'-temp/lib/modules/'+self.KV ))
    
        # create etc/modules/<group>
        os.makedirs(self.temp['work']+'/initramfs-modules-'+self.KV+'-temp/etc/modules')
        modconfdict = get_config_modules_dict(self.master_config)
    
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
                process_append('echo %s >> %s' % (o, self.temp['work']+'/initramfs-modules-'+self.KV+'-temp/etc/modules/bootupdate'), self.verbose)
    
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
    
        os.makedirs(self.temp['work']+'/initramfs-luks-temp/lib/luks')
        os.makedirs(self.temp['work']+'/initramfs-luks-temp/sbin')
    
        if os.path.isfile(cryptsetup_bin) and self.hostbin is True:
            luks_host_version = commands.getoutput("cryptsetup --version | cut -d' ' -f2")
            logging.debug('initramfs.append.luks ' + luks_host_version + ' ' + cryptsetup_bin + ' from host')
            print green(' * ') + turquoise('initramfs.append.luks ') + luks_host_version + ' '  + cryptsetup_bin + ' from ' + white('host')
            process('cp %s %s/initramfs-luks-temp/sbin' % (cryptsetup_bin, self.temp['work']), self.verbose)
            process('chmod +x %s/initramfs-luks-temp/sbin/cryptsetup' % self.temp['work'], self.verbose)
        elif os.path.isfile(cryptsetup_sbin) and self.hostbin is True:
            luks_host_version = commands.getoutput("cryptsetup --version | cut -d' ' -f2")
            logging.debug('initramfs.append.luks ' + luks_host_version + ' ' + cryptsetup_sbin + ' from host')
            print green(' * ') + turquoise('initramfs.append.luks ') + luks_host_version + ' ' + cryptsetup_sbin + ' from ' + white('host')
            process('cp %s %s/initramfs-luks-temp/sbin' % (cryptsetup_sbin, self.temp['work']), self.verbose)
            process('chmod +x %s/initramfs-luks-temp/sbin/cryptsetup' % self.temp['work'], self.verbose)
        else:
            print green(' * ') + turquoise('initramfs.append.luks ') + self.master_config['luks-version'],
            logging.debug('initramfs.append.luks ' + self.master_config['luks-version'])

            if os.path.isfile(self.temp['cache']+'/cryptsetup-'+self.master_config['luks-version']+'.bz2') and self.nocache is False:
                # use cache
                print 'from ' + white('cache')

                # extract cache
                os.system('/bin/bzip2 -dc %s/cryptsetup-%s.bz2 > %s/initramfs-luks-temp/sbin/cryptsetup' % (self.temp['cache'], self.master_config['luks-version'], self.temp['work']))
                process('chmod a+x %s/initramfs-luks-temp/sbin/cryptsetup' % self.temp['work'], self.verbose)

            else:
                # compile and cache
                print
                from luks import luks
                luksobj = luks(self.master_config, self.temp, self.verbose)
                luksobj.build()

                # extract cache
                os.system('/bin/bzip2 -dc %s/cryptsetup-%s.bz2 > %s/initramfs-luks-temp/sbin/cryptsetup' % (self.temp['cache'], self.master_config['luks-version'], self.temp['work']))
                process('chmod a+x %s/initramfs-luks-temp/sbin/cryptsetup' % self.temp['work'], self.verbose)

        os.chdir(self.temp['work']+'/initramfs-luks-temp')
        return os.system(self.cpio())

    def glibc(self):
        """
        Append GNU C libraries from host to the initramfs

        @return: bool
        """
        os.makedirs(self.temp['work']+'/initramfs-glibc-temp/')
        os.makedirs(self.temp['work']+'/initramfs-glibc-temp/etc')
        os.makedirs(self.temp['work']+'/initramfs-glibc-temp/lib')

        print green(' * ') + turquoise('initramfs.append.glibc')
        # for shell
        print green(' * ') + '... ' + '/lib/libm.so.6'
        process('cp /lib/libm.so.6           %s' % self.temp['work']+'/initramfs-glibc-temp/lib', self.verbose)
        # mostly for authentication
        print green(' * ') + '... ' + '/lib/libnss_files.so.2'
        process('cp /lib/libnss_files.so.2   %s' % self.temp['work']+'/initramfs-glibc-temp/lib', self.verbose)
        print green(' * ') + '... ' + '/lib/libnss_dns.so.2'
        process('cp /lib/libnss_dns.so.2     %s' % self.temp['work']+'/initramfs-glibc-temp/lib', self.verbose)
        print green(' * ') + '... ' + '/lib/libnss_nis.so.2'
        process('cp /lib/libnss_nis.so.2     %s' % self.temp['work']+'/initramfs-glibc-temp/lib', self.verbose)
        print green(' * ') + '... ' + '/lib/libnsl.so.1'
        process('cp /lib/libnsl.so.1         %s' % self.temp['work']+'/initramfs-glibc-temp/lib', self.verbose)
        # resolves dns->ip
        print green(' * ') + '... ' + '/lib/libresolv.so.2'
        process('cp /lib/libresolv.so.2      %s' % self.temp['work']+'/initramfs-glibc-temp/lib', self.verbose)
        print green(' * ') + '... ' + '/lib/ld-linux.so.2'
        process('cp /lib/ld-linux.so.2       %s' % self.temp['work']+'/initramfs-glibc-temp/lib', self.verbose)
        print green(' * ') + '... ' + '/lib/libc.so.6'
        process('cp /lib/libc.so.6           %s' % self.temp['work']+'/initramfs-glibc-temp/lib', self.verbose)
        # for dropbear
        print green(' * ') + '... ' + '/lib/libnss_compat.so.2'
        process('cp /lib/libnss_compat.so.2  %s' % self.temp['work']+'/initramfs-glibc-temp/lib', self.verbose)
        print green(' * ') + '... ' + '/lib/libutil.so.1'
        process('cp /lib/libutil.so.1        %s' % self.temp['work']+'/initramfs-glibc-temp/lib', self.verbose)
        print green(' * ') + '... ' + '/etc/ld.so.cache'
        process('cp /etc/ld.so.cache         %s' % self.temp['work']+'/initramfs-glibc-temp/etc', self.verbose)
        print green(' * ') + '... ' + '/lib/libcrypt.so.1'
        process('cp /lib/libcrypt.so.1       %s' % self.temp['work']+'/initramfs-glibc-temp/lib', self.verbose)

        os.chdir(self.temp['work']+'/initramfs-glibc-temp')
        return os.system(self.cpio())

    def libncurses(self):
        """
        Append host libncurses libraries to the initramfs

        @return: bool
        """
        print green(' * ') + turquoise('initramfs.append.libncurses')
        os.makedirs(self.temp['work']+'/initramfs-libncurses-temp/lib')

        print green(' * ') + '... ' + '/lib/libncurses.so.5'
        process('cp /lib/libncurses.so.5     %s' % self.temp['work']+'/initramfs-libncurses-temp/lib', self.verbose)

        os.chdir(self.temp['work']+'/initramfs-libncurses-temp')
        return os.system(self.cpio())

    def zlib(self):
        """
        Append host zlib libraries to the initramfs

        @return: bool
        """
        print green(' * ') + turquoise('initramfs.append.zlib')
        os.makedirs(self.temp['work']+'/initramfs-zlib-temp/lib')

        print green(' * ') + '... ' + '/lib/libz.so.1'
        process('cp /lib/libz.so.1      %s' % self.temp['work']+'/initramfs-zlib-temp/lib', self.verbose)

        os.chdir(self.temp['work']+'/initramfs-zlib-temp')
        return os.system(self.cpio())
        
    def dropbear(self):
        """
        Append dropbear support to the initramfs
    
        @return: bool
        """
        for i in ['bin', 'sbin', 'dev', 'usr/bin', 'usr/sbin', 'lib', 'etc', 'var/log', 'var/run']:
            os.makedirs(self.temp['work']+'/initramfs-dropbear-temp/%s' % i)

        dropbear_sbin       = '/usr/sbin/dropbear'

        # FIXME: check if dropbear is merged with USE=static if not fail
        if os.path.isfile(dropbear_sbin) and self.hostbin is True:

            dbscp_bin           = '/usr/bin/dbscp'  # assumes host version is patched w/ scp->dbscp because of openssh.
                                                    # compilation of dropbear sources are not patched hence
                                                    # FIXME if --dropbear --hostbin
                                                    # FIXME then /usr/bin/scp
                                                    # FIXME else /usr/bin/dbscp
            dbclient_bin        = '/usr/bin/dbclient'
            dropbearkey_bin     = '/usr/bin/dropbearkey'
            dropbearconvert_bin = '/usr/bin/dropbearconvert'

            print green(' * ') + turquoise('initramfs.append.dropbear ')+dbscp_bin+' '+dbclient_bin+' '+dropbearkey_bin+' '+dropbearconvert_bin+' '+dropbear_sbin +' from ' + white('host')
            process('cp %s %s/initramfs-dropbear-temp/bin' % (dbscp_bin, self.temp['work']), self.verbose)
            process('cp %s %s/initramfs-dropbear-temp/bin' % (dbclient_bin, self.temp['work']), self.verbose)
            process('cp %s %s/initramfs-dropbear-temp/bin' % (dropbearkey_bin, self.temp['work']), self.verbose)
            process('cp %s %s/initramfs-dropbear-temp/bin' % (dropbearconvert_bin, self.temp['work']), self.verbose)
            process('cp %s %s/initramfs-dropbear-temp/sbin' % (dropbear_sbin, self.temp['work']), self.verbose)
            process('chmod +x %s/initramfs-dropbear-temp/bin/dbscp' % self.temp['work'], self.verbose)
            process('chmod +x %s/initramfs-dropbear-temp/bin/dbclient' % self.temp['work'], self.verbose)
            process('chmod +x %s/initramfs-dropbear-temp/bin/dropbearkey' % self.temp['work'], self.verbose)
            process('chmod +x %s/initramfs-dropbear-temp/bin/dropbearconvert' % self.temp['work'], self.verbose)
            process('chmod +x %s/initramfs-dropbear-temp/sbin/dropbear' % self.temp['work'], self.verbose)
        else:
            print green(' * ') + turquoise('initramfs.append.dropbear ') + self.master_config['dropbear-version'],
            logging.debug('initramfs.append.dropbear ' + self.master_config['dropbear-version'])
            if os.path.isfile(self.temp['cache']+'/dropbear-'+self.master_config['dropbear-version']+'.tar') and self.nocache is False:
                # use cache
                print 'from ' + white('cache')

                # extract cache
                os.system('tar xpf %s/dropbear-%s.tar -C %s/initramfs-dropbear-temp ' % (self.temp['cache'], self.master_config['dropbear-version'], self.temp['work']))

            else:
                # compile and cache
                print
                from dropbear import dropbear
                dropbearobj = dropbear(self.master_config, self.temp, self.verbose)
                dropbearobj.build()

                # extract cache
                os.system('tar xpf %s/dropbear-%s.tar -C %s/initramfs-dropbear-temp ' % (self.temp['cache'], self.master_config['dropbear-version'], self.temp['work']))

        process('cp /etc/localtime %s'          % self.temp['work']+'/initramfs-dropbear-temp/etc', self.verbose)
        process('cp /etc/nsswitch.conf %s'      % self.temp['work']+'/initramfs-dropbear-temp/etc', self.verbose)
        process('cp /etc/hosts %s'              % self.temp['work']+'/initramfs-dropbear-temp/etc', self.verbose)
        process('touch %s'                      % self.temp['work']+'/initramfs-dropbear-temp/var/log/lastlog', self.verbose)
        process('touch %s'                      % self.temp['work']+'/initramfs-dropbear-temp/var/log/wtmp', self.verbose)
        process('touch %s'                      % self.temp['work']+'/initramfs-dropbear-temp/var/run/utmp', self.verbose)

        os.chdir(self.temp['work']+'/initramfs-dropbear-temp/dev')
        process('mknod urandom c 1 9', self.verbose)
        process('mknod ptmx c 5 2', self.verbose)
        process('mknod tty c 5 0', self.verbose)
        process('chmod 0666 urandom', self.verbose)
        process('chmod 0666 ptmx', self.verbose)
        process('chmod 0666 tty', self.verbose)

        os.chdir(self.temp['work']+'/initramfs-dropbear-temp')
        return os.system(self.cpio())

    def set_rootpasswd(self):
        """
        Set root password of the initramfs
        """
        print green(' * ') + turquoise('initramfs.append.rootpasswd')

        os.makedirs(self.temp['work']+'/initramfs-rootpasswd-temp')
        os.makedirs(self.temp['work']+'/initramfs-rootpasswd-temp/etc')
        os.makedirs(self.temp['work']+'/initramfs-rootpasswd-temp/root')
        process('cp /etc/shells %s' % self.temp['work']+'/initramfs-rootpasswd-temp/etc', self.verbose)
        process('chown root:root %s'% self.temp['work']+'/initramfs-rootpasswd-temp/root', self.verbose)

        # TODO use a python API instead of openssl
        # TODO deal with /etc/shadow eventually, then use openssl passwd -1 mypass for proper type/salt/hash $1$salt$hash
        print green(' * ') + '... ' + '/etc/passwd'
        os.system('echo "root:$(openssl passwd %s):0:0:root:/root:/bin/sh" > %s'% (self.rootpasswd, self.temp['work']+'/initramfs-rootpasswd-temp/etc/passwd'))
        print green(' * ') + '... ' + '/etc/group'
        os.system('echo "root:x:0:root" > %s' % self.temp['work']+'/initramfs-rootpasswd-temp/etc/group')

#        # HACK quick ninja chroot to set password
#        slash = os.open('/', os.O_RDONLY)
#        os.chroot(self.temp['work']+'/initramfs-rootpasswd-temp/') # dive in # PROBLEM we don't have the FULL initramfs, hence no /bin/sh to chroot in
#        os.system('echo "root:%s" | busybox chpasswd' % self.rootpasswd)
#
#        # HACK break out of chroot
#        os.fchdir(slash)
#        for i in range(100): # assume we haven't gone deeper than 100
#            os.chdir('..')
#        os.chroot('.')

        os.chdir(self.temp['work']+'/initramfs-rootpasswd-temp')
        return os.system(self.cpio())

    def e2fsprogs(self):
        """
        Append blkid binary to the initramfs
        after compiling e2fsprogs
        
        @return: bool
        """
        blkid_sbin = '/sbin/blkid'

        os.makedirs(self.temp['work']+'/initramfs-blkid-temp/bin')

        if os.path.isfile(blkid_sbin) and self.hostbin is True:
            # use from host
            logging.debug('initramfs.append.e2fsprogs from %s' % white('host'))
            print green(' * ') + turquoise('initramfs.append.e2fsprogs ')+ blkid_sbin +' from ' + white('host')
            process('cp %s %s/initramfs-blkid-temp/bin' % (blkid_sbin, self.temp['work']), self.verbose)
            process('chmod +x %s/initramfs-blkid-temp/bin/blkid' % self.temp['work'], self.verbose)

        else:
            logging.debug('initramfs.append.e2fsprogs ' + self.master_config['e2fsprogs-version'])
            print green(' * ') + turquoise('initramfs.append.e2fsprogs ') + self.master_config['e2fsprogs-version'],
            if os.path.isfile(self.temp['cache'] + '/blkid-e2fsprogs-' + self.master_config['e2fsprogs-version']+'.bz2') and self.nocache is False:
                # use cache
                print 'from ' + white('cache')
            else:
                # compile
                print
                from e2fsprogs import e2fsprogs
                e2obj = e2fsprogs(self.master_config, self.temp, self.verbose)
                e2obj.build()
    
            # FIXME careful with the >
            os.system('/bin/bzip2 -dc %s/blkid-e2fsprogs-%s.bz2 > %s/initramfs-blkid-temp/bin/blkid' % (self.temp['cache'], self.master_config['e2fsprogs-version'], self.temp['work']))
            process('chmod +x %s/initramfs-blkid-temp/bin/blkid' % self.temp['work'], self.verbose)
    
        os.chdir(self.temp['work']+'/initramfs-blkid-temp')
        return os.system(self.cpio())

    def splash(self):
        """
        Append splash framebuffer to initramfs
    
        @return: bool
        """
        ret = zero = int('0')
        splash_geninitramfs_bin = '/usr/sbin/splash_geninitramfs'
   
        process('mkdir -p ' + self.temp['work']+'/initramfs-splash-temp/', self.verbose)
    
        if os.path.isfile(splash_geninitramfs_bin):
            # if splashutils is merged
            if self.stheme is not '':
                if os.path.isfile('/etc/conf.d/splash'):
                    os.system('source /etc/conf.d/splash')
            if self.sres is not '':
                self.sres = '-r %s' % self.sres
    
            logging.debug('initramfs.append.splash ' + self.stheme + ' ' + self.sres)
            print green(' * ') + turquoise('initramfs.append.splash ') + self.stheme + ' ' + self.sres

            # because splash_geninitramfs fails and exits with success when you provide a broken theme path
            # we need to check if the dir exists first, can't hurt
            if os.path.isdir('/etc/splash/'+self.stheme):
                process('splash_geninitramfs -c %s/initramfs-splash-temp %s %s' % (self.temp['work'], self.sres, self.stheme), self.verbose)
            else:
                self.fail('/etc/splash/'+self.stheme+' does not exist')
                # FIXME 2 ways
                # we either fail and die
                # or remove splash support and still continue

            if os.path.isfile('/usr/share/splashutils/initrd.splash'):
                process('cp -f /usr/share/splashutils/initrd.splash %s/initramfs-splash-temp/etc' % self.temp['work'], self.verbose)
            else:
                self.fail('/usr/share/splashutils/initrd.splash missing')
        else:
            # if splashutils is not merged
            # FIXME write the splash routine from scratch?
            self.fail('media-gfx/splashutils must be merged')
            
#            from splash import splash
#            splashobj = splash(self.master_config, self.theme, self.sres, self.sinitrd, self.temp, self.verbose)
#            splashobj.build()
    
        os.chdir(self.temp['work']+'/initramfs-splash-temp')
        return os.system(self.cpio())
     
    def lvm2(self):
        """
        Append lvm2 static binary first to the initramfs
    
        @return: bool
        """
        ret = int('0')
        lvm2_static_bin = '/sbin/lvm.static'
        lvm2_bin        = '/sbin/lvm'
    
        process('mkdir -p ' + self.temp['work']+'/initramfs-lvm2-temp/etc/lvm', self.verbose)
        process('mkdir -p ' + self.temp['work']+'/initramfs-lvm2-temp/bin', self.verbose)
    
        if os.path.isfile(lvm2_static_bin) and self.hostbin is True:
            # TODO see if we can use something else than import commands
            # lvm2_static_version = commands.getoutput("lvm.static version | cut -d: -f2 | head -n1 | cut -d'(' -f1")
            logging.debug('initramfs.append.lvm2 ' + ' ' + lvm2_static_bin + ' from host')
            print green(' * ') + turquoise('initramfs.append.lvm2 ') + lvm2_static_bin + ' from ' + white('host')
            process('cp %s %s/initramfs-lvm2-temp/bin/lvm' % (lvm2_static_bin, self.temp['work']), self.verbose)
        elif os.path.isfile(lvm2_bin) and self.hostbin is True:
            logging.debug('initramfs.append.lvm2 ' + lvm2_bin + ' from host')
            print green(' * ') + turquoise('initramfs.append.lvm2 ') + lvm2_bin + ' from ' + white('host')
            process('cp %s %s/initramfs-lvm2-temp/bin/lvm' % (lvm2_bin, self.temp['work']), self.verbose)
        else:
            logging.debug('initramfs.append.lvm2 ' + self.master_config['lvm2-version'])
            if os.path.isfile(self.temp['cache']+'/lvm.static-'+self.master_config['lvm2-version']+'.bz2') and self.nocache is False:
                print green(' * ') + turquoise('initramfs.append.lvm2 ') + self.master_config['lvm2-version'],
                # use cache
                print 'from ' + white('cache')

                # extract cache
                os.system('bzip2 -dc %s > %s/initramfs-lvm2-temp/bin/lvm' % (self.temp['cache']+'/lvm.static-'+self.master_config['lvm2-version']+'.bz2', self.temp['work']))
                process('chmod a+x %s/initramfs-lvm2-temp/bin/lvm' % self.temp['work'], self.verbose)
            else: 
                # compile and cache
                print green(' * ') + turquoise('initramfs.append.lvm2 ') + self.master_config['lvm2-version']
                from lvm2 import lvm2
                lvm2obj = lvm2(self.master_config, self.temp, self.verbose)
                lvm2obj.build()

                # extract cache
                os.system('bzip2 -dc %s > %s/initramfs-lvm2-temp/bin/lvm' % (self.temp['cache']+'/lvm.static-'+self.master_config['lvm2-version']+'.bz2', self.temp['work']))
                process('chmod a+x %s/initramfs-lvm2-temp/bin/lvm' % self.temp['work'], self.verbose)

        if os.path.isfile(lvm2_static_bin) or os.path.isfile(lvm2_bin):
            process('cp /etc/lvm/lvm.conf %s/initramfs-lvm2-temp/etc/lvm/' % self.temp['work'], self.verbose)
    
        os.chdir(self.temp['work']+'/initramfs-lvm2-temp')
        return os.system(self.cpio())

#    def evms(self):
#        """
#        Append evms libraries to the initramfs
#    
#        @return: bool
#        """
#        logging.debug('initramfs.append.evms')
#        print green(' * ') + turquoise('initramfs.append.evms'),
#    
#        if os.path.isfile('/sbin/evms'):
#            print 'feeding' + ' from host'
#    
#            process('mkdir -p ' + self.temp['work']+'/initramfs-evms-temp/lib/evms', self.verbose)
#            process('mkdir -p ' + self.temp['work']+'/initramfs-evms-temp/etc', self.verbose)
#            process('mkdir -p ' + self.temp['work']+'/initramfs-evms-temp/bin', self.verbose)
#            process('mkdir -p ' + self.temp['work']+'/initramfs-evms-temp/sbin', self.verbose)
#    
#        # FIXME broken due to *
#        # process('cp -a /lib/ld-* %s/initramfs-evms-temp/lib' % temp['work'], verbose)
#        # process('cp -a /lib/libgcc_s* %s/initramfs-evms-temp/lib' % temp['work'], verbose)
#        # process('cp -a /lib/libc-* /lib/libc.* %s/initramfs-evms-temp/lib' % temp['work'], verbose)
#        # process('cp -a /lib/libdl-* /lib/libdl.* %s/initramfs-evms-temp/lib' % temp['work'], verbose)
#        # process('cp -a /lib/libpthread* %s/initramfs-evms-temp/lib' % temp['work'], verbose)
#        # process('cp -a /lib/libuuid*so* %s/initramfs-evms-temp/lib' % temp['work'], verbose)
#        # process('cp -a /lib/libevms*so* %s/initramfs-evms-temp/lib' % temp['work'], verbose)
#        # process('cp -a /lib/evms %s/initramfs-evms-temp/lib' % temp['work'], verbose)
#        # process('cp -a /lib/evms/* %s/initramfs-evms-temp/lib/evms' % temp['work'], verbose)
#        # process('cp -a /etc/evms.conf %s/initramfs-evms-temp/etc' % temp['work'], verbose)
#        # process('cp /sbin/evms_activate %s/initramfs-evms-temp/sbin' % temp['work'], verbose)
#        # process('rm %s/initramfs-evms-temp/lib/evms/*/swap*.so' % temp['work'], verbose)
#        else:
#            print
#            self.fail('sys-fs/evms must be merged')
#    
#        os.chdir(self.temp['work']+'/initramfs-evms-temp')
#        return os.system(self.cpio())
#    
#    def firmware(self):
#        """
#        Append firmware to the initramfs
#    
#        @return: bool
#        """
#        logging.debug('initramfs.append_firmware ' + self.firmware + ' from host')
#        print green(' * ') + turquoise('initramfs.append_firmware ') + white(self.firmware) + ' from host'
#    
#        process('mkdir -p ' + temp['work']+'/initramfs-firmware-temp/lib/firmware', self.verbose)
#        process('cp -a %s %s/initramfs-firmware-temp/lib/' % (self.firmware, self.temp['work']), self.verbose)
#    
#        os.chdir(temp['work']+'/initramfs-firmware-temp')
#        return os.system(self.cpio())
#    
#    def mdadm(self):
#        """
#        Append mdadm to initramfs
#    
#        @return: bool
#        """
#        ret = int('0')
#        logging.debug('initramfs.append.mdadm')
#        print green(' * ') + turquoise('initramfs.append.mdadm')
#    
#        process('mkdir -p ' + self.temp['work']+'/initramfs-dmadm-temp/etc', self.verbose)
#        process('cp -a /etc/mdadm.conf %s/initramfs-mdadm-temp/etc' % self.temp['work'], self.verbose)
#    
#        os.chdir(self.temp['work']+'/initramfs-mdadm-temp')
#        return os.system(self.cpio())
#
#    def dmraid(self):
#        """
#        Append dmraid to initramfs
#    
#        @return: bool
#        """
#        logging.debug('initramfs.append.dmraid ' + self.master_config['dmraid_ver'])
#        print green(' * ') + turquoise('initramfs.append.dmraid ') + self.master_config['dmraid_ver'],
#    
#        process('mkdir -p ' + self.temp['work']+'/initramfs-dmraid-temp/bin', self.verbose)
#    
#        if os.path.isfile(self.temp['cache']+'/dmraid.static-'+self.master_config['dmraid_ver']+'.bz2') and self.nocache is False:
#            # use cache
#            print 'from ' + white('cache')
#            pass
#        else:
#            # compile
#            print
#            import dmraid
#            dmraid.build_sequence(self.master_config, self.selinux, self.temp, self.verbose['std'])
#    
#        # FIXME careful with the > 
#        os.system('/bin/bzip2 -dc %s/dmraid.static-%s.bz2 > %s/initramfs-dmraid-temp/bin/dmraid.static' % (self.temp['cache'], self.master_config['dmraid_ver'], self.temp['work']))
#        process('cp %s/initramfs-dmraid-temp/bin/dmraid.static %s/initramfs-dmraid-temp/bin/dmraid' % (self.temp['work'],self.temp['work']), self.verbose)
#    
#        # TODO ln -sf raid456.ko raid45.ko ?
#        # TODO is it ok to have no raid456.ko? if so shouldn't we check .config for inkernel feat?
#        #   or should we raise an error and make the user enabling the module manually? warning?
#    
#        os.chdir(self.temp['work']+'/initramfs-dmraid-temp')
#        return os.system(self.cpio())
#
#    # TODO: make sure somehow the appropriate modules get loaded when using iscsi?
#    def iscsi(self):
#        """
#        Append iscsi to initramfs
#    
#        @return: bool
#        """
#        logging.debug('initramfs.append.iscsi ' + self.master_config['iscsi_ver'])
#        print green(' * ') + turquoise('initramfs.append.iscsi ') + self.master_config['iscsi_ver'],
#    
#        process('mkdir -p ' + self.temp['work']+'/initramfs-iscsi-temp/bin', self.verbose)
#    
#        if os.path.isfile(self.temp['cache']+'/iscsistart-'+self.master_config['iscsi_ver']+'.bz2') and self.nocache is False:
#            # use cache
#            print 'from ' + white('cache')
#        else:
#            # compile
#            print
#            import iscsi
#            iscsi.build_sequence(self.master_config, self.temp, self.verbose['std'])
#    
#        os.system('/bin/bzip2 -dc %s/iscsistart-%s.bz2 > %s/initramfs-iscsi-temp/bin/iscsistart' % (self.temp['cache'], self.master_config['iscsi_ver'], self.temp['work']))
#        process('chmod +x %s/initramfs-iscsi-temp/bin/iscsistart' % self.temp['work'], self.verbose)
#    
#        os.chdir(self.temp['work']+'/initramfs-iscsi-temp')
#        return os.system(self.cpio())
#    
#    def unionfs_fuse(self):
#        """
#        Append unionfs-fuse to initramfs
#        
#        @return: bool
#        """
#        self.build_fuse()
#    
#        logging.debug('initramfs.append.unionfs_fuse ' + self.master_config['unionfs_fuse_ver'])
#        print green(' * ') + turquoise('initramfs.append.unionfs_fuse ') + self.master_config['unionfs_fuse_ver'],
#    
#        if os.path.isfile(self.temp['cache']+'/unionfs-fuse.static-'+self.master_config['unionfs_fuse_ver']+'.bz2') and self.nocache is False:
#            # use cache
#            print 'from ' + white('cache')
#        else:
#            print
#            # TODO: find a better check for fuse
#            if os.path.isfile('/usr/include/fuse.h'):
#                # compile
#                import unionfs_fuse
#                unionfs_fuse.build_sequence(self.master_config, self.temp, self.verbose)
#            else:
#                self.fail('we need libfuse: sys-fs/fuse must be merged')
#    
#        process('mkdir -p ' + self.temp['work']+'/initramfs-unionfs-fuse-temp/sbin', self.verbose)
#        # FIXME careful with the > passed to process()
#        os.system('/bin/bzip2 -dc %s/unionfs-fuse.static-%s.bz2 > %s/initramfs-unionfs-fuse-temp/sbin/unionfs' % (self.temp['cache'], self.master_config['unionfs_fuse_ver'], self.temp['work']))
#        os.system('chmod +x %s/initramfs-unionfs-fuse-temp/sbin/unionfs' % self.temp['work'])
#    
#        os.chdir(self.temp['work']+'/initramfs-unionfs-fuse-temp')
#        return os.system(self.cpio())
#     
#    def build_fuse(self):
#        """
#        Build fuse and cache it for later use
#        Only to be called for --unionfs!
#    
#        @return: bool
#        """
#        logging.debug('initramfs.build_fuse ' + self.master_config['fuse_ver'])
#        print green(' * ') + turquoise('initramfs.build_fuse ') +self.master_config['fuse_ver'],
#    
#        if os.path.isfile(self.temp['cache']+'/fuse-dircache-'+self.master_config['fuse_ver']+'.tar.bz2') and self.nocache is False:
#            # use cache
#            print 'from ' + white('cache')
#        else:
#            # compile and cache
#            print
#            import fuse
#            fuse.build_sequence(self.master_config, self.temp, self.verbose)
#    
#        # extract
#        os.system('tar xfj %s -C %s' % (self.temp['cache']+'/fuse-dircache-'+self.master_config['fuse_ver']+'.tar.bz2', self.temp['work']))
#    
#        return
#    
#    def aufs(self):
#        """
#        Append aufs to initramfs
#        """
#        logging.debug('initramfs.append_aufs')
#        print green(' * ') + turquoise('initramfs.append_aufs ')
#    
#        os.mkdir(temp['work']+'/initramfs-aufs-temp')
#    
#    # TODO
#    # aufs is tricky: gotta patch the kernel sources
#    # then build aufs 
#    # then pack initrd
#    # then rebuild kernel not just bzImage
#    
#        os.chdir(self.temp['work']+'/initramfs-aufs-temp')
#        return os.system(self.cpio())

    def ttyecho(self):
        """
        """
        print green(' * ') + turquoise('initramfs.append.ttyecho')

        process('mkdir -p ' + self.temp['work']+'/initramfs-ttyecho-temp/sbin', self.verbose)

        print green(' * ') + '... ' + 'gcc %s/tools/ttyecho.c -o %s' % (self.libdir, self.temp['work']+'/initramfs-ttyecho-temp/sbin/ttyecho')
        process('gcc %s/tools/ttyecho.c -o %s' % (self.libdir, self.temp['work']+'/initramfs-ttyecho-temp/sbin/ttyecho'), self.verbose)
        process('chmod +x %s' % self.temp['work']+'/initramfs-ttyecho-temp/sbin/ttyecho', self.verbose)

        os.chdir(self.temp['work']+'/initramfs-ttyecho-temp')
        return os.system(self.cpio())

    def plugin(self, dir):
        """
        Append user generated file structure

        @return: bool
        """
        print green(' * ') + turquoise('initramfs.append.plugin ') + dir
        logging.debug('initramfs.append.plugin')

        process('mkdir -p ' + self.temp['work']+'/initramfs-plugin-temp/', self.verbose)

        os.system('cp -a %s/* %s' % (dir, self.temp['work']+'/initramfs-plugin-temp/'))

        os.chdir(self.temp['work']+'/initramfs-plugin-temp')
        return os.system(self.cpio())
