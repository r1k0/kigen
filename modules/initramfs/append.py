import os
import sys
import logging
import subprocess
import crypt
from stdout import *
from utils.process import *
from utils.misc import *
from utils.isstatic import isstatic
from utils.listdynamiclibs import *

class append:

    def __init__(self,              \
                temp,               \
                KV,                 \
                linuxrc,            \
                kernel_dir_opt,     \
                arch,               \
                master_conf,        \
                modules_conf,       \
                initramfs_conf,     \
                version_conf,       \
                url_conf,           \
                libdir,             \
                defconfig,          \
                oldconfig,          \
                menuconfig,         \
                verbose,            \
                bbconf,             \
                busyboxprogs,       \
                bootupdateset,      \
                bootupdateinitrd,   \
                plymouth,           \
                stheme,             \
                sres,               \
                sinitrd,            \
#                firmware,           \
                selinux,            \
                dbdebugflag,        \
                keymaplist,         \
                nocache,            \
                hostbin,            \
                rootpasswd,         \
                hostsshkeys,        \
                ssh_pubkeys,        \
                ssh_pubkeys_file):
        """
        init class variables
        """
        self.temp               = temp
        self.KV                 = KV
        self.linuxrc            = linuxrc # list
        self.kernel_dir_opt     = kernel_dir_opt
        self.arch               = arch
        self.master_conf        = master_conf
        self.modules_conf       = modules_conf
        self.initramfs_conf     = initramfs_conf
        self.version_conf       = version_conf
        self.url_conf           = url_conf
        self.libdir             = libdir
        self.defconfig          = defconfig
        self.oldconfig          = oldconfig
        self.menuconfig         = menuconfig
        self.verbose            = verbose
        self.bbconf             = bbconf
        self.busyboxprogs       = busyboxprogs
        self.bootupdateset      = bootupdateset
        self.bootupdateinitrd   = bootupdateinitrd
        self.stheme             = stheme
        self.sres               = sres
        self.sinitrd            = sinitrd
        self.nocache            = nocache
#        self.firmware           = firmware
        self.selinux            = selinux
        self.hostbin            = hostbin
        self.rootpasswd         = rootpasswd
        self.hostsshkeys        = hostsshkeys
        self.ssh_pubkeys        = ssh_pubkeys
        self.ssh_pubkeys_file   = ssh_pubkeys_file
        self.dbdebugflag        = dbdebugflag
        self.keymaplist         = keymaplist
        self.plymouth           = plymouth

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
        logging.debug('error: '+msg)
        print(red('error')+': '+msg)
        sys.exit(2)

    def base(self):
        """
        Append baselayout to the initramfs

        @return: bool
        """
        logging.debug('>>> entering initramfs.append.base')
        # create the baselayout
        for i in ['dev', 'bin', 'etc', 'home', 'usr', 'proc', 'tmp', 'sys', 'var/lock/dmraid', 'sbin', 'usr/bin', 'usr/sbin']:
            os.makedirs(self.temp['work']+'/initramfs-base-temp/%s' % i)

        os.chdir(self.kernel_dir_opt) # WHY? # FIXME: change os.chdir by subprocess.popen(..., cwd=kernel_dir_opt

        # init
        if self.linuxrc is '':
        # FIXME: copy linuxrc depending on arch
        # if netboot is True:
        #       cp "${GK_SHARE}/netboot/linuxrc.x" "${TEMP}/initramfs-aux-temp/init"
        # elif arch is 'x86':
        #       os.system('cp %s/arch/linuxrc %s/initramfs-base-temp/init' % (libdir, temp['work']))
        # elif arch is 'amd64':
        #       blablabla
#            print(green(' * ')+'... Gentoo linuxrc'+ white(' 3.4.30') + ' patched')
            # this is Gentoo official linuxrc suite (see genkernel and genkernel-next)
            print(green(' * ')+'... /init')
            process('cp %s/defaults/linuxrc %s/initramfs-base-temp/init' % (self.libdir, self.temp['work']), self.verbose)
            print(green(' * ')+'... /etc/initrd.scripts')
            process('cp %s/defaults/initrd.scripts %s/initramfs-base-temp/etc/' % (self.libdir, self.temp['work']), self.verbose)
            print(green(' * ')+'... /etc/initrd.d/*')
# for genkernel-next
            process('cp -r %s/defaults/initrd.d %s/initramfs-base-temp/etc/' % (self.libdir, self.temp['work']), self.verbose)
            print(green(' * ')+'... /etc/initrd.defaults')
            process('cp %s/defaults/initrd.defaults %s/initramfs-base-temp/etc/' % (self.libdir, self.temp['work']), self.verbose)

            process('chmod +x %s/initramfs-base-temp/etc/initrd.scripts' % self.temp['work'], self.verbose)
# for genkernel-next
            process('chmod +x %s/initramfs-base-temp/etc/initrd.d/*' % self.temp['work'], self.verbose)
            process('chmod +x %s/initramfs-base-temp/etc/initrd.defaults' % self.temp['work'], self.verbose)
            print(green(' * ')+'... /sbin/ldconfig')
            process('cp /sbin/ldconfig  %s/initramfs-base-temp/sbin' % self.temp['work'], self.verbose)
            process('cp /etc/ld.so.conf %s/initramfs-base-temp/etc' % self.temp['work'], self.verbose)
            process('chmod +x %s/initramfs-base-temp/sbin/ldconfig' % self.temp['work'], self.verbose)
        else:
            linuxrclist = self.linuxrc.split(',')
            print(str(linuxrclist) + ' from ' + white('host'))
            # copy first the linuxrc to /init
            if os.path.isfile(linuxrclist[0]):
                process('cp %s %s/initramfs-base-temp/init' % (linuxrclist[0], self.temp['work']), self.verbose)
                print(green(' * ')+'... /init')
            else:
                self.fail('%s does not exist.')
            # then all possible following files
            for i in linuxrclist[1:]:
                if os.path.isfile(i):
                    process('cp %s %s/initramfs-base-temp/etc' % (i, self.temp['work']), self.verbose)
                    print(green(' * ')+'... /etc/%s' + os.path.basename(i))
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
        print(green(' * ')+'... /etc/fstab')

        os.chdir(self.temp['work']+'/initramfs-base-temp/dev')

        # create nodes
        process('mknod -m 660 console c 5 1', self.verbose)
        print(green(' * ')+'... /dev/console')
        process('mknod -m 660 null    c 1 3', self.verbose)
        print(green(' * ')+'... /dev/null')
        process('mknod -m 600 tty1    c 4 1', self.verbose)
        print(green(' * ')+'... /dev/tty1')

        # timestamp the build
        from time import strftime
        build_date = open(self.temp['work']+'/initramfs-base-temp/etc/build_date', 'w')
        build_date.writelines(strftime("%Y-%m-%d %H:%M:%S")+ '\n')
        build_date.close()

        os.chdir(self.temp['work']+'/initramfs-base-temp')

        # link linuxrc to /init
        process('ln -s init linuxrc', self.verbose)

        # what's the harm to have it harcoded? even if the group is commented out in the config file the variable is still empty
        # same thinking for bootupdate it's already set in etc/initrd.defaults $HWOPTS
        process_append("echo HWOPTS='$HWOPTS ataraid dmraid evms firewire fs iscsi lvm2 mdadm net pata pcmcia sata scsi usb waitscan' >> %s/initramfs-base-temp/etc/initrd.defaults" % self.temp['work'], self.verbose)

        process('cp %s/defaults/modprobe %s/initramfs-base-temp/sbin/modprobe' % (self.libdir, self.temp['work']), self.verbose)
        print(green(' * ')+'... /sbin/modprobe')
        process('chmod +x %s/initramfs-base-temp/sbin/modprobe' % self.temp['work'], self.verbose)

        os.chdir(self.temp['work']+'/initramfs-base-temp/sbin')
        process('ln -s ../init init', self.verbose)
        process('chmod +x %s/initramfs-base-temp/init' % self.temp['work'], self.verbose)

        os.chdir(self.temp['work']+'/initramfs-base-temp/')
        return os.system(self.cpio())

    def modules(self):
        """
        Find system modules and config modules
        Append modules to the initramfs

        @return: bool
        """
        logging.debug('>>> entering initramfs.append.modules')
        process('mkdir -p %s' % self.temp['work']+'/initramfs-modules-'+self.KV+'-temp/lib/modules/'+self.KV, self.verbose)

        # FIXME: ctrl c does not work during this function
        # FIXME: rewrite (later)
        # FIXME: maybe |uniq the list? in case the user sets
        # multiple times the same module in different groups
        #
        # is it really a big deal? I don't think so

        # identify and copy host kernel modules
        if not os.path.isdir('/lib/modules/'+self.KV):
            self.fail('/lib/modules/'+self.KV+" doesn't exist: have you run 'kigen kernel'?")

        modsyslist  = get_sys_modules_list(self.KV)

        if not modsyslist:
            self.fail('Host modules list is empty: have you run "kigen kernel"?')

        # identify and copy config kernel modules
        modconfdict = get_config_modules_dict(self.modules_conf)

        # compare host list and config list and ship the ones that both match
        for k, v in modconfdict.items():
            print(green(' * ') + '... ' + k + '\t ', end='')
            vlist = v.split()
            for j in modsyslist:
                j = j.replace('.ko', '') # easier to just remove it and add it later
                for e in vlist:
                    if e == j:
                        print(e , end=' ')
                        module = os.popen('find /lib/modules/'+self.KV+' -name '+e+'.ko 2>/dev/null | head -n 1').read().strip()
                        module_dirname = os.path.dirname(module)
                        process('\nmkdir -p %s' % self.temp['work'] + '/initramfs-modules-' + self.KV + '-temp' + module_dirname, self.verbose) # \n is for -d display
                        process('cp -ax %s %s/initramfs-modules-%s-temp/%s' % (module, self.temp['work'], self.KV, module_dirname), self.verbose)
                        break
            print()

        # FUNTOO: for each module in /etc/boot.conf
        if "load-modules" in self.bootupdateinitrd:
            for i in self.bootupdateinitrd['load-modules'].split():
                for j in modsyslist:
                    k = i +'.ko'
                    if k == j:
                        logging.debug('shipping ' + i + ' from /etc/boot.conf')
                        print(green(' * ') + '... ' + white(i) + ' from /etc/boot.conf')
                        module = os.popen('find /lib/modules/'+self.KV+' -name '+k+' 2>/dev/null | head -n 1').read().strip()
                        module_dirname = os.path.dirname(module)
                        process('mkdir -p %s' % self.temp['work'] + '/initramfs-modules-' + self.KV + '-temp' + module_dirname, self.verbose)
                        process('cp -ax %s %s/initramfs-modules-%s-temp/%s' % (module, self.temp['work'], self.KV, module_dirname), self.verbose)

        # FIXME: make variable of /lib/modules in case of FAKEROOT export
#        process_star('cp /lib/modules/%s/modules.* %s' % (self.KV, self.temp['work']+'/initramfs-modules-'+self.KV+'-temp/lib/modules/'+self.KV ), self.verbose)
        process('cp /lib/modules/%s/modules.* %s' % (self.KV, self.temp['work']+'/initramfs-modules-'+self.KV+'-temp/lib/modules/'+self.KV ), self.verbose)

        # create etc/modules/<group>
        process('mkdir -p %s' % self.temp['work']+'/initramfs-modules-'+self.KV+'-temp/etc/modules', self.verbose)

        # Genkernel official boot module design
        # for each key value in the module config dictionary
        for k, v in modconfdict.items():
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

    def plugin(self, dir):
        """
        Append user generated file structure

        @return: bool
        """
        logging.debug('>>> entering initramfs.append.plugin')
        print(green(' * ') + turquoise('initramfs.append.plugin ') + dir)
        print(yellow(' * ') + '... ' + yellow('warning') +': plugin may overwrite kigen files')

        process('mkdir -p ' + self.temp['work']+'/initramfs-plugin-temp/', self.verbose)

        process('cp -ar %s/* %s' % (dir, self.temp['work']+'/initramfs-plugin-temp/'), self.verbose)

        os.chdir(self.temp['work']+'/initramfs-plugin-temp')
        return os.system(self.cpio())

    def set_rootcredentials(self):
        """
        Set root password and ssh public key of the initramfs
        """
        logging.debug('>>> entering initramfs.append.set_rootcredentials')

        process('mkdir -p %s' % self.temp['work']+'/initramfs-rootcredentials-temp/etc', self.verbose)
        process('mkdir -p %s' % self.temp['work']+'/initramfs-rootcredentials-temp/root', self.verbose)

        process('cp /etc/shells %s' % self.temp['work']+'/initramfs-rootcredentials-temp/etc', self.verbose)
        process('chown root:root %s'% self.temp['work']+'/initramfs-rootcredentials-temp/root', self.verbose)

        # If we are called only for ssh pubkeys and don't have a pass configured  we use * as a pass
        if self.rootpasswd is '':
            password_hash="*"
        else:
            password_hash=crypt.crypt(self.rootpasswd, crypt.mksalt())

        #create the user and group files
        print(green(' * ') + '... ' + '/etc/passwd')
        process('echo "root:x:0:0:root:/root:/bin/sh" > %s'% self.temp['work']+'/initramfs-rootcredentials-temp/etc/passwd', self.verbose)
        print(green(' * ') + '... ' + '/etc/shadow')
        process("echo 'root:%s:::::::' > %s"% (password_hash, self.temp['work']+'/initramfs-rootcredentials-temp/etc/shadow'), self.verbose)
        process('chmod 640 %s'% self.temp['work']+'/initramfs-rootcredentials-temp/etc/shadow', self.verbose)
        print(green(' * ') + '... ' + '/etc/group')
        process('echo "root:x:0:root" > %s' % self.temp['work']+'/initramfs-rootcredentials-temp/etc/group', self.verbose)

        # Add the ssh pubkeys if required
        if self.ssh_pubkeys is True:
            print(green(' * ') + '... ' + '/root/.ssh/authorized_keys')
            process('mkdir -p %s' % self.temp['work']+'/initramfs-rootcredentials-temp/root/.ssh', self.verbose)
            process('cp %s %s' % (self.ssh_pubkeys_file, self.temp['work']+'/initramfs-rootcredentials-temp/root/.ssh/authorized_keys'), self.verbose)

#        # HACK quick ninja chroot to set password - leave for history museum of horror coding - actually send the whole project ;)
#        slash = os.open('/', os.O_RDONLY)
#        os.chroot(self.temp['work']+'/initramfs-rootpasswd-temp/') # dive in # PROBLEM we don't have the FULL initramfs, hence no /bin/sh to chroot in
#        os.system('echo "root:%s" | busybox chpasswd' % self.rootpasswd)
#        # HACK break out of chroot
#        os.fchdir(slash)
#        for i in range(100): # assume we haven't gone deeper than 100
#            os.chdir('..')
#        os.chroot('.')

        os.chdir(self.temp['work']+'/initramfs-rootcredentials-temp')
        return os.system(self.cpio())

    def splash(self):
        """
        Append splash framebuffer to initramfs

        @return: bool
        """
        logging.debug('>>> entering initramfs.append.splash')
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
            print(green(' * ') + turquoise('initramfs.append.splash ') + self.stheme + ' ' + self.sres)

            # make sure media-gfx/splashutils has fbcondecor use flag enabled
            if not pkg_has_useflag('media-gfx', 'splashutils', 'fbcondecor'):
                print(red('error')+': utils.pkg_has_useflag("media-gfx", "splashutils", "fbcondecor") failed, remerge splashutils with +fbcondecor')
                sys.exit(2)

            # because splash_geninitramfs fails and exits with success when you provide a broken theme path
            # we need to check if the dir exists first, can't hurt
            if os.path.isdir('/etc/splash/'+self.stheme):
                process('splash_geninitramfs -c %s/initramfs-splash-temp %s %s' % (self.temp['work'], self.sres, self.stheme), self.verbose)
            else:
                self.fail('/etc/splash/'+self.stheme+' does not exist')
                # FIXME we either fail and die or remove splash support and still continue

            if os.path.isfile('/usr/share/splashutils/initrd.splash'):
                process('cp -f /usr/share/splashutils/initrd.splash %s/initramfs-splash-temp/etc' % self.temp['work'], self.verbose)
            else:
                self.fail('/usr/share/splashutils/initrd.splash missing')
        else:
            # if splashutils is not merged
            self.fail('media-gfx/splashutils must be merged')

            # FIXME write the splash routine from scratch?
#            from sources.splash import splash
#            splashobj = splash(self.master_conf, self.version_conf, self.url, self.theme, self.sres, self.sinitrd, self.temp, self.verbose)
#            splashobj.build()

        os.chdir(self.temp['work']+'/initramfs-splash-temp')
        return os.system(self.cpio())

    # INFO: don't name this function plymouth() or it'll fail
    def ply(self):
#[ -z "${PLYMOUTH_THEME}" ] && \
#    PLYMOUTH_THEME=$(plymouth-set-default-theme)
#[ -z "${PLYMOUTH_THEME}" ] && PLYMOUTH_THEME=text
#
#if [ -d "${TEMP}/initramfs-ply-temp" ]
#then
#    rm -r "${TEMP}/initramfs-ply-temp"
#fi
#
#mkdir -p "${TEMP}/initramfs-ply-temp/usr/share/plymouth/themes"
#mkdir -p "${TEMP}/initramfs-ply-temp/etc/plymouth"
#mkdir -p "${TEMP}/initramfs-ply-temp/"{bin,sbin}
#mkdir -p "${TEMP}/initramfs-ply-temp/usr/"{bin,sbin}
#
#cd "${TEMP}/initramfs-ply-temp"
#
#local theme_dir="/usr/share/plymouth/themes"
#local t=
#
#local p=
#local ply="${theme_dir}/${PLYMOUTH_THEME}/${PLYMOUTH_THEME}.plymouth"
#local plugin=$(grep "^ModuleName=" "${ply}" | cut -d= -f2-)
#local plugin_binary=
#if [ -n "${plugin}" ]
#then
#    plugin_binary="$(plymouth --get-splash-plugin-path)/${plugin}.so"
#fi
#
#print_info 1 "  >> Installing plymouth [ using the ${PLYMOUTH_THEME} theme and plugin: \"${plugin}\" ]..."
#
#for t in text details ${PLYMOUTH_THEME}; do
#    cp -R "${theme_dir}/${t}" \
#        "${TEMP}/initramfs-ply-temp${theme_dir}/" || \
#        gen_die "cannot copy ${theme_dir}/details"
#done
#cp /usr/share/plymouth/{bizcom.png,plymouthd.defaults} \
#    "${TEMP}/initramfs-ply-temp/usr/share/plymouth/" || \
#        gen_die "cannot copy bizcom.png and plymouthd.defaults"
#
## Do both config setup
#echo -en "[Daemon]\nTheme=${PLYMOUTH_THEME}\n" > \
#    "${TEMP}/initramfs-ply-temp/etc/plymouth/plymouthd.conf" || \
#    gen_die "Cannot create /etc/plymouth/plymouthd.conf"
#ln -sf "${PLYMOUTH_THEME}/${PLYMOUTH_THEME}.plymouth" \
#    "${TEMP}/initramfs-ply-temp${theme_dir}/default.plymouth" || \
#    gen_die "cannot setup the default plymouth theme"
#
## plymouth may have placed the libs into /usr/
#local libply_core="/lib*/libply-splash-core.so.*"
#if ! ls -1 ${libply_core} 2>/dev/null >/dev/null; then
#    libply_core="/usr/lib*/libply-splash-core.so.*"
#fi
#
#local libs=(
#    "${libply_core}"
#    "/usr/lib*/libply-splash-graphics.so.*"
#    "/usr/lib*/plymouth/text.so"
#    "/usr/lib*/plymouth/details.so"
#    "/usr/lib*/plymouth/renderers/frame-buffer.so"
#    "/usr/lib*/plymouth/renderers/drm.so"
#    "${plugin_binary}"
#)
## lib64 must take the precedence or all the cpio archive
## symlinks will be fubared
#local slib= lib= final_lib= final_libs=()
#for slib in "${libs[@]}"; do
#    lib=( ${slib} )
#    final_lib="${lib[0]}"
#    final_libs+=( "${final_lib}" )
#done
#
#local plymouthd_bin="/sbin/plymouthd"
#[ ! -e "${plymouthd_bin}" ] && \
#    plymouthd_bin="/usr/sbin/plymouthd"
#
#local plymouth_bin="/bin/plymouth"
#[ ! -e "${plymouth_bin}" ] && \
#    plymouth_bin="/usr/bin/plymouth"
#
#copy_binaries "${TEMP}/initramfs-ply-temp" \
#    "${plymouthd_bin}" "${plymouth_bin}" \
#    "${final_libs[@]}" || gen_die "cannot copy plymouth"
#
#log_future_cpio_content
#find . -print | cpio ${CPIO_ARGS} --append -F "${CPIO}" \
#    || gen_die "appending plymouth to cpio"
#
#cd "${TEMP}"
#rm -r "${TEMP}/initramfs-ply-temp/"

        logging.debug('>>> entering initramfs.append.plymouth')
        process('mkdir -p ' + self.temp['work']+'/initramfs-plymouth-temp/', self.verbose)
        process('mkdir -p ' + self.temp['work']+'/initramfs-plymouth-temp/usr/share/plymouth/themes', self.verbose)
        process('mkdir -p ' + self.temp['work']+'/initramfs-plymouth-temp/etc/plymouth', self.verbose)
        process('mkdir -p ' + self.temp['work']+'/initramfs-plymouth-temp/{bin,sbin}', self.verbose)
        process('mkdir -p ' + self.temp['work']+'/initramfs-plymouth-temp/usr/{bin,sbin}', self.verbose)

        process('cp -r /usr/share/plymouth/themes/* ' + self.temp['work']+'/initramfs-plymouth-temp/usr/share/plymouth/themes', self.verbose)
        process('cp /usr/share/plymouth/{bizcom.png,plymouthd.defaults} ' + self.temp['work']+'/initramfs-plymouth-temp/usr/share/plymouth/', self.verbose)

        print(green(' * ') + turquoise('initramfs.append.plymouth ') + self.plymouth)

        os.chdir(self.temp['work']+'/initramfs-plymouth-temp')
        return os.system(self.cpio())

    def keymaps(self):
        """
        Ship all keymaps within initramfs
        It's up to the user to provide the correct kernel cmdline parameter

        @return bool
        """
        logging.debug('>>> entering initramfs.append.keymaps')
        print(green(' * ') + turquoise('initramfs.append.keymaps ')+self.keymaplist)

        process('mkdir -p %s' % self.temp['work']+'/initramfs-keymaps-temp/lib/keymaps', self.verbose)
        process('mkdir -p %s' % self.temp['work']+'/keymaplist', self.verbose) # temp keymap dir

        # make keymaplist a real list
        self.keymaplist = self.keymaplist.split(',')
        if 'all' in self.keymaplist:
#            process('tar zxf %s/defaults/keymaps.tar.gz -C %s/initramfs-keymaps-temp/lib/keymaps' % (self.libdir, self.temp['work']), self.verbose)
            process('cp -r %s/defaults/keymaps %s/initramfs-keymaps-temp/lib/' % (self.libdir, self.temp['work']), self.verbose)
            f = os.popen("ls %s/initramfs-keymaps-temp/lib/keymaps/"%self.temp['work'])

            print(green(' * ') + '... ', end='')
            z = int('0')
            for i in f.readlines():
                # filter out item with numbers
                if re.match("^[a-z]", i):
                    i = i.replace('.map', '')
                    i = i.replace('\n', '')
                    z = z+1
                    if (z % 6 == 0):
                        print()
                        print(green(' * ') + '... ', end='')
                    print(i, end=' ')
            print()

        else:
#            process('tar zxf %s/defaults/keymaps.tar.gz -C %s/keymaplist' % (self.libdir, self.temp['work']), self.verbose)
            process('cp -r %s/defaults/keymaps/* %s/keymaplist' % (self.libdir, self.temp['work']), self.verbose)
            print(green(' * ') + '... ', end='')
            z = int('0')
            for i in self.keymaplist:
                if os.path.isfile('%s/keymaplist/%s.map'%(self.temp['work'],i)):
                    if re.match("^[a-z]", i):
                        process('cp %s/keymaplist/%s.map %s/initramfs-keymaps-temp/lib/keymaps'%(self.temp['work'], i, self.temp['work']), self.verbose)
                        i = i.replace('\n', '')
                        z = z+1
                        if (z % 6 == 0):
                            print()
                            print(green(' * ') + '... ', end='')
                        print(i, end=' ')
                else:
                    print(yellow(' * ') + '... ' + yellow('warning')+' %s.map does not exist, skipping'%i)
            print()

            # still copy keymapList: linuxrc expects it
            process('cp %s/keymaplist/keymapList %s/initramfs-keymaps-temp/lib/keymaps'%(self.temp['work'], self.temp['work']), self.verbose)

        os.chdir(self.temp['work']+'/initramfs-keymaps-temp')
        return os.system(self.cpio())

########################
# source based features
########################

    def source_lvm2(self):
        """
        Append lvm2 compiled binary to the initramfs

        @return: bool
        """
        logging.debug('>>> entering initramfs.append.source_lvm2')
        lvm2_static_bin = '/sbin/lvm.static'
        lvm2_bin        = '/sbin/lvm'

        process('mkdir -p ' + self.temp['work']+'/initramfs-source-lvm2-temp/etc/lvm', self.verbose)
        process('mkdir -p ' + self.temp['work']+'/initramfs-source-lvm2-temp/bin', self.verbose)

        logging.debug('initramfs.append.source_lvm2 ' + self.version_conf['lvm2-version'])

        if os.path.isfile(self.temp['cache']+'/lvm.static-'+self.version_conf['lvm2-version']+'.bz2') and self.nocache is False:
            # use cache
            print(green(' * ') + '... '+'cache found: importing')

        else:
            # compile and cache
            from .sources.lvm2 import lvm2
            lvm2obj = lvm2(self.master_conf, self.version_conf, self.url_conf, self.temp, self.verbose)
            lvm2obj.build()

        # extract cache
        os.system('bzip2 -dc %s > %s/initramfs-source-lvm2-temp/bin/lvm' % (self.temp['cache']+'/lvm.static-'+self.version_conf['lvm2-version']+'.bz2', self.temp['work']))
        process('chmod a+x %s/initramfs-source-lvm2-temp/bin/lvm' % self.temp['work'], self.verbose)

        # FIXME print something to the user about it so he knows and can tweak it before
        if os.path.isfile(lvm2_static_bin) or os.path.isfile(lvm2_bin):
            process('cp /etc/lvm/lvm.conf %s/initramfs-source-lvm2-temp/etc/lvm/' % self.temp['work'], self.verbose)

        os.chdir(self.temp['work']+'/initramfs-source-lvm2-temp')
        return os.system(self.cpio())

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
#        logging.debug('initramfs.append.mdadm')
#        print green(' * ') + turquoise('initramfs.append.mdadm')
#
#        process('mkdir -p ' + self.temp['work']+'/initramfs-dmadm-temp/etc', self.verbose)
#        process('cp -a /etc/mdadm.conf %s/initramfs-mdadm-temp/etc' % self.temp['work'], self.verbose)
#
#        os.chdir(self.temp['work']+'/initramfs-mdadm-temp')
#        return os.system(self.cpio())

    def source_dmraid(self):
        """
        Append dmraid to initramfs from sources

        @return: bool
        """
        logging.debug('>>> entering initramfs.append.source_dmraid')

        dmraid_bin = '/usr/sbin/dmraid'

        process('mkdir -p ' + self.temp['work']+'/initramfs-source-dmraid-temp/bin', self.verbose)

        logging.debug('initramfs.append.source_dmraid '+ self.version_conf['dmraid-version']),
        if os.path.isfile(self.temp['cache']+'/dmraid.static-'+self.version_conf['dmraid-version']+'.bz2') and self.nocache is False:
            # use cache
            print(green(' * ') + '... '+'cache found: importing')
        else:
            # compile
            from .sources.dmraid import dmraid
            dmraidobj = dmraid(self.master_conf, self.version_conf, self.url_conf, self.selinux, self.temp, self.verbose)
            dmraidobj.build()

        # extract cache
        # FIXME careful with the >
        logging.debug('/bin/bzip2 -dc %s/dmraid.static-%s.bz2 > %s/initramfs-source-dmraid-temp/bin/dmraid.static' % (self.temp['cache'], self.version_conf['dmraid-version'], self.temp['work']))
        os.system('/bin/bzip2 -dc %s/dmraid.static-%s.bz2 > %s/initramfs-source-dmraid-temp/bin/dmraid.static' % (self.temp['cache'], self.version_conf['dmraid-version'], self.temp['work']))
        # FIXME make symlink rather than cp
        process('cp %s/initramfs-source-dmraid-temp/bin/dmraid.static %s/initramfs-source-dmraid-temp/bin/dmraid' % (self.temp['work'],self.temp['work']), self.verbose)

        # FIXME ln -sf raid456.ko raid45.ko ?
        # FIXME is it ok to have no raid456.ko? if so shouldn't we check .config for inkernel feat?
        #   or should we raise an error and make the user enabling the module manually? warning?

        os.chdir(self.temp['work']+'/initramfs-source-dmraid-temp')
        return os.system(self.cpio())

#    # FIXME: make sure somehow the appropriate modules get loaded when using iscsi?
#    def iscsi(self):
#        """
#        Append iscsi to initramfs
#
#        @return: bool
#        """
#        logging.debug('initramfs.append.iscsi ' + self.master_conf['iscsi_ver'])
#        print green(' * ') + turquoise('initramfs.append.iscsi ') + self.master_conf['iscsi_ver'],
#
#        process('mkdir -p ' + self.temp['work']+'/initramfs-iscsi-temp/bin', self.verbose)
#
#        if os.path.isfile(self.temp['cache']+'/iscsistart-'+self.master_conf['iscsi_ver']+'.bz2') and self.nocache is False:
#            # use cache
#            print 'from ' + white('cache')
#        else:
#            # compile
#            print
#            import iscsi
#            iscsi.build_sequence(self.master_conf, self.temp, self.verbose['std'])
#
#        os.system('/bin/bzip2 -dc %s/iscsistart-%s.bz2 > %s/initramfs-iscsi-temp/bin/iscsistart' % (self.temp['cache'], self.master_conf['iscsi_ver'], self.temp['work']))
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
#        logging.debug('initramfs.append.unionfs_fuse ' + self.master_conf['unionfs_fuse_ver'])
#        print green(' * ') + turquoise('initramfs.append.unionfs_fuse ') + self.master_conf['unionfs_fuse_ver'],
#
#        if os.path.isfile(self.temp['cache']+'/unionfs-fuse.static-'+self.master_conf['unionfs_fuse_ver']+'.bz2') and self.nocache is False:
#            # use cache
#            print 'from ' + white('cache')
#        else:
#            print
#            # FIXME: find a better check for fuse
#            if os.path.isfile('/usr/include/fuse.h'):
#                # compile
#                import unionfs_fuse
#                unionfs_fuse.build_sequence(self.master_conf, self.temp, self.verbose)
#            else:
#                self.fail('we need libfuse: sys-fs/fuse must be merged')
#
#        process('mkdir -p ' + self.temp['work']+'/initramfs-unionfs-fuse-temp/sbin', self.verbose)
#        # FIXME careful with the > passed to process()
#        os.system('/bin/bzip2 -dc %s/unionfs-fuse.static-%s.bz2 > %s/initramfs-unionfs-fuse-temp/sbin/unionfs' % (self.temp['cache'], self.master_conf['unionfs_fuse_ver'], self.temp['work']))
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
#        logging.debug('initramfs.build_fuse ' + self.master_conf['fuse_ver'])
#        print green(' * ') + turquoise('initramfs.build_fuse ') +self.master_conf['fuse_ver'],
#
#        if os.path.isfile(self.temp['cache']+'/fuse-dircache-'+self.master_conf['fuse_ver']+'.tar.bz2') and self.nocache is False:
#            # use cache
#            print 'from ' + white('cache')
#        else:
#            # compile and cache
#            print
#            import fuse
#            fuse.build_sequence(self.master_conf, self.temp, self.verbose)
#
#        # extract
#        os.system('tar xfj %s -C %s' % (self.temp['cache']+'/fuse-dircache-'+self.master_conf['fuse_ver']+'.tar.bz2', self.temp['work']))
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
#    # FIXME aufs is tricky: gotta patch the kernel sources
#    # then build aufs
#    # then pack initrd
#    # then rebuild kernel not just bzImage
#
#        os.chdir(self.temp['work']+'/initramfs-aufs-temp')
#        return os.system(self.cpio())

    def source_ttyecho(self):
        """
        ttyecho is piece of code found on the net to copy/paste commands to /dev/console
        it is very handy when it comes to run commands that requires current session
        to be /dev/console
        REQUIRED for booting remote luks system through a dropbear session

        @return bool
        """
        logging.debug('>>> entering initramfs.append.source_ttyecho')
        process('mkdir -p ' + self.temp['work']+'/initramfs-source-ttyecho-temp/sbin', self.verbose)

        print(green(' * ') + '... ' + 'gcc -static %s/tools/ttyecho.c' % self.libdir)
        print(green(' * ') + '...     -o %s' % (self.temp['work']+'/initramfs-source-ttyecho-temp/sbin/ttyecho'))
        process('gcc -static %s/tools/ttyecho.c -o %s' % (self.libdir, self.temp['work']+'/initramfs-source-ttyecho-temp/sbin/ttyecho'), self.verbose)
        process('chmod +x %s' % self.temp['work']+'/initramfs-source-ttyecho-temp/sbin/ttyecho', self.verbose)

        os.chdir(self.temp['work']+'/initramfs-source-ttyecho-temp')
        return os.system(self.cpio())

    def source_strace(self):
        """
        Append strace from sources to the initramfs
        for debugging purposes

        @return: bool
        """
        logging.debug('>>> entering initramfs.append.source_strace')
        strace_bin = '/usr/bin/strace'

        process('mkdir -p %s' % self.temp['work']+'/initramfs-source-strace-temp/bin', self.verbose)

        logging.debug('initramfs.append.source_strace ' + self.version_conf['strace-version'])
        if os.path.isfile(self.temp['cache'] + '/strace-' + self.version_conf['strace-version']+'.bz2') and self.nocache is False:
            # use cache
            print(green(' * ') + '... ' + 'cache found: importing')
        else:
            # compile
            from .sources.strace import strace
            strobj = strace(self.master_conf, self.version_conf, self.url_conf, self.temp, self.verbose)
            strobj.build()

        # extract cache
        # FIXME careful with the >
        logging.debug('/bin/bzip2 -dc %s/strace-%s.bz2 > %s/initramfs-source-strace-temp/bin/strace' % (self.temp['cache'], self.version_conf['strace-version'], self.temp['work']))
        os.system('/bin/bzip2 -dc %s/strace-%s.bz2 > %s/initramfs-source-strace-temp/bin/strace' % (self.temp['cache'], self.version_conf['strace-version'], self.temp['work']))
        process('chmod +x %s/initramfs-source-strace-temp/bin/strace' % self.temp['work'], self.verbose)

        os.chdir(self.temp['work']+'/initramfs-source-strace-temp')
        return os.system(self.cpio())

    def source_screen(self):
        """
        Append screen binary to the initramfs

        @return: bool
        """
        logging.debug('>>> entering initramfs.append.source_screen')
        screen_bin = '/usr/bin/screen'

        process('mkdir -p %s' % self.temp['work']+'/initramfs-source-screen-temp/bin', self.verbose)

        logging.debug('initramfs.append.source_screen ' + self.version_conf['screen-version'])
        if os.path.isfile(self.temp['cache'] + '/screen-' + self.version_conf['screen-version']+'.bz2') and self.nocache is False:
            # use cache
            print(green(' * ') + '... '+'cache found: importing')
        else:
            # compile
            from .sources.screen import screen
            strobj = screen(self.master_conf, self.version_conf, self.url_conf, self.temp, self.verbose)
            strobj.build()

        # extract cache
        # FIXME careful with the >
        logging.debug('/bin/bzip2 -dc %s/screen-%s.bz2 > %s/initramfs-source-screen-temp/bin/screen' % (self.temp['cache'], self.version_conf['screen-version'], self.temp['work']))
        os.system('/bin/bzip2 -dc %s/screen-%s.bz2 > %s/initramfs-source-screen-temp/bin/screen' % (self.temp['cache'], self.version_conf['screen-version'], self.temp['work']))
        process('chmod +x %s/initramfs-source-screen-temp/bin/screen' % self.temp['work'], self.verbose)

        # add required /usr/share/terminfo/l/linux for screen
        # FIXME: to support other arch copy accordingly
        os.makedirs(self.temp['work']+'/initramfs-source-screen-temp/usr/share/terminfo/l')
        process('cp /usr/share/terminfo/l/linux %s' % self.temp['work']+'/initramfs-source-screen-temp/usr/share/terminfo/l', self.verbose)

        os.chdir(self.temp['work']+'/initramfs-source-screen-temp')
        return os.system(self.cpio())

    def source_busybox(self):
        """
        Append the busybox compiled objects to the initramfs

        @return: bool
        """
        logging.debug('>>> entering initramfs.append.source_busybox')
        if os.path.isfile(self.temp['cache']+'/busybox-bin-'+self.version_conf['busybox-version']+'.tar.bz2') and self.nocache is False:
            # use cache
            print(green(' * ') + '... '+'cache found: importing')
        else:
            # compile
            from .sources.busybox import busybox
            bbobj = busybox( self.arch,             \
                        self.bbconf,                \
                        self.master_conf,           \
                        self.version_conf,          \
                        self.url_conf,              \
                        self.libdir,                \
                        self.temp,                  \
                        self.defconfig,             \
                        self.oldconfig,             \
                        self.menuconfig,            \
                        self.verbose)
            bbobj.build()

        # append busybox to cpio
        process('mkdir -p %s' % self.temp['work']+'/initramfs-source-busybox-temp/bin', self.verbose)
        process('mkdir -p %s' % self.temp['work']+'/initramfs-source-busybox-temp/usr/share/udhcpc/', self.verbose)

        os.chdir(self.temp['work']+'/initramfs-source-busybox-temp')
        process('tar -xjf %s/busybox-bin-%s.tar.bz2 -C %s busybox' % (self.temp['cache'], self.version_conf['busybox-version'], self.temp['work']+'/initramfs-source-busybox-temp/bin'), self.verbose)
        process('chmod +x %s/busybox' % (self.temp['work']+'/initramfs-source-busybox-temp/bin'), self.verbose)
        process('cp %s/defaults/udhcpc.scripts %s/initramfs-source-busybox-temp/usr/share/udhcpc/default.script' % (self.libdir, self.temp['work']), self.verbose)
        process('chmod +x %s/initramfs-source-busybox-temp/usr/share/udhcpc/default.script' % self.temp['work'], self.verbose)

        # TO BE REMOVED : linuxrc's bb --install -s takes care of it
        # FIXME if busybox not exist then ln the default set -> [ ash sh mount uname echo cut cat
        for i in self.busyboxprogs.split():
            process('ln -s busybox %s/initramfs-source-busybox-temp/bin/%s' % (self.temp['work'], i), self.verbose)

        os.chdir(self.temp['work']+'/initramfs-source-busybox-temp')
        return os.system(self.cpio())

    def source_luks(self):
        """
        Append the LUKS static binary to the initramfs

        @return: bool
        """
        logging.debug('>>> entering initramfs.append.source_luks')
        cryptsetup_bin  = '/bin/cryptsetup'
        cryptsetup_sbin = '/sbin/cryptsetup'

        process('mkdir -p %s' % self.temp['work']+'/initramfs-source-luks-temp/lib/luks', self.verbose)
        process('mkdir -p %s' % self.temp['work']+'/initramfs-source-luks-temp/sbin', self.verbose)

        logging.debug('initramfs.append.source_luks ' + self.version_conf['luks-version'])

        if os.path.isfile(self.temp['cache']+'/cryptsetup-'+self.version_conf['luks-version']+'.bz2') and self.nocache is False:
            # use cache
            print(green(' * ') + '... '+'cache found: importing')

            # extract cache
            logging.debug('/bin/bzip2 -dc %s/cryptsetup-%s.bz2 > %s/initramfs-source-luks-temp/sbin/cryptsetup' % (self.temp['cache'], self.version_conf['luks-version'], self.temp['work']))
            os.system('/bin/bzip2 -dc %s/cryptsetup-%s.bz2 > %s/initramfs-source-luks-temp/sbin/cryptsetup' % (self.temp['cache'], self.version_conf['luks-version'], self.temp['work']))
            process('chmod a+x %s/initramfs-source-luks-temp/sbin/cryptsetup' % self.temp['work'], self.verbose)

        else:
            # compile and cache
            from .sources.luks import luks
            luksobj = luks(self.master_conf, self.version_conf, self.url_conf, self.temp, self.verbose)
            luksobj.build()

            # extract cache
            # FIXME careful with the >
            logging.debug('/bin/bzip2 -dc '+self.temp['cache']+'/cryptsetup-'+self.version_conf['luks-version']+'.bz2 > '+self.temp['work']+'/initramfs-source-luks-temp/sbin/cryptsetup')
            os.system('/bin/bzip2 -dc %s/cryptsetup-%s.bz2 > %s/initramfs-source-luks-temp/sbin/cryptsetup' % (self.temp['cache'], self.version_conf['luks-version'], self.temp['work']))
            process('chmod a+x %s/initramfs-source-luks-temp/sbin/cryptsetup' % self.temp['work'], self.verbose)

        os.chdir(self.temp['work']+'/initramfs-source-luks-temp')
        return os.system(self.cpio())

    def source_dropbear(self):
        """
        Append dropbear support to the initramfs

        @return: bool
        """
        logging.debug('>>> entering initramfs.append.source.dropbear')
        for i in ['bin', 'sbin', 'dev', 'usr/bin', 'usr/sbin', 'lib', 'etc', 'var/log', 'var/run', 'root']:
            process('mkdir -p %s/%s' % (self.temp['work']+'/initramfs-source-dropbear-temp/', i), self.verbose)

        dropbear_sbin       = '/usr/sbin/dropbear'

        logging.debug('initramfs.append.source.dropbear ' + self.version_conf['dropbear-version'])
        if os.path.isfile(self.temp['cache']+'/dropbear-'+self.version_conf['dropbear-version']+'.tar') and self.nocache is False:
            # use cache
            print(green(' * ') + '... '+'cache found: importing')

            # extract cache
            process('tar xpf %s/dropbear-%s.tar -C %s/initramfs-source-dropbear-temp ' % (self.temp['cache'], self.version_conf['dropbear-version'], self.temp['work']), self.verbose)

        else:
            # compile and cache
            from .sources.dropbear import dropbear
            dropbearobj = dropbear(self.master_conf, self.version_conf, self.url_conf, self.hostsshkeys, self.dbdebugflag, self.temp, self.verbose)
            dropbearobj.build()

            # extract cache
            process('tar xpf %s/dropbear-%s.tar -C %s/initramfs-source-dropbear-temp ' % (self.temp['cache'], self.version_conf['dropbear-version'], self.temp['work']), self.verbose)

        process('cp /etc/localtime %s'          % self.temp['work']+'/initramfs-source-dropbear-temp/etc', self.verbose)
        process('cp /etc/nsswitch.conf %s'      % self.temp['work']+'/initramfs-source-dropbear-temp/etc', self.verbose)
        process('cp /etc/gai.conf %s'           % self.temp['work']+'/initramfs-source-dropbear-temp/etc', self.verbose)
        process('cp /etc/hosts %s'              % self.temp['work']+'/initramfs-source-dropbear-temp/etc', self.verbose)
        process('touch %s'                      % self.temp['work']+'/initramfs-source-dropbear-temp/var/log/lastlog', self.verbose)
        process('touch %s'                      % self.temp['work']+'/initramfs-source-dropbear-temp/var/log/wtmp', self.verbose)
        process('touch %s'                      % self.temp['work']+'/initramfs-source-dropbear-temp/var/run/utmp', self.verbose)

        # ship the boot* scripts too
#        process('cp %s/scripts/boot-luks-lvm.sh %s' % (self.libdir, self.temp['work']+'/initramfs-source-dropbear-temp/root'), self.verbose)
#        process('chmod +x %s' % self.temp['work']+'/initramfs-source-dropbear-temp/root/boot-luks-lvm.sh', self.verbose)
#        process('cp %s/scripts/boot-luks.sh %s' % (self.libdir, self.temp['work']+'/initramfs-source-dropbear-temp/root'), self.verbose)
#        process('chmod +x %s' % self.temp['work']+'/initramfs-source-dropbear-temp/root/boot-luks.sh', self.verbose)
        process('cp %s/scripts/boot.sh %s' % (self.libdir, self.temp['work']+'/initramfs-source-dropbear-temp/root'), self.verbose)
        process('chmod +x %s' % self.temp['work']+'/initramfs-source-dropbear-temp/root/boot.sh', self.verbose)

        os.chdir(self.temp['work']+'/initramfs-source-dropbear-temp/dev')
        process('mknod urandom c 1 9', self.verbose)
        process('mknod ptmx c 5 2', self.verbose)
        process('mknod tty c 5 0', self.verbose)
        process('chmod 0666 urandom', self.verbose)
        process('chmod 0666 ptmx', self.verbose)
        process('chmod 0666 tty', self.verbose)

        os.chdir(self.temp['work']+'/initramfs-source-dropbear-temp')
        return os.system(self.cpio())

    def source_disklabel(self):
        """
        Append blkid binary to the initramfs
        after compiling e2fsprogs

        @return: bool
        """
        logging.debug('>>> entering initramfs.append.source_disklabel')
        blkid_sbin = '/sbin/blkid'

        process('mkdir -p %s' % self.temp['work']+'/initramfs-source-disklabel-temp/bin', self.verbose)

        logging.debug('initramfs.append.source_disklabel ' + self.version_conf['e2fsprogs-version'])

        if os.path.isfile(self.temp['cache'] + '/blkid-e2fsprogs-' + self.version_conf['e2fsprogs-version']+'.bz2') and self.nocache is False:
            # use cache
            print(green(' * ') + '... '+'cache found: importing')
        else:
            # compile
            from .sources.e2fsprogs import e2fsprogs
            e2obj = e2fsprogs(self.master_conf, self.version_conf, self.url_conf, self.temp, self.verbose)
            e2obj.build()

        # extract cache
        # FIXME careful with the >
        os.system('/bin/bzip2 -dc %s/blkid-e2fsprogs-%s.bz2 > %s/initramfs-source-disklabel-temp/bin/blkid' % (self.temp['cache'], self.version_conf['e2fsprogs-version'], self.temp['work']))
        process('chmod +x %s/initramfs-source-disklabel-temp/bin/blkid' % self.temp['work'], self.verbose)

        os.chdir(self.temp['work']+'/initramfs-source-disklabel-temp')
        return os.system(self.cpio())
