=======
General
=======

.. sectnum::

.. contents:: Table of contents

Introduction
~~~~~~~~~~~~

**KIGen now only supports Python3.**

**KIGen uses Genkernel linuxrc and provides the same boot interface as Genkernel does.**

KIGen for Linux aims at providing first an equal set of features (in Python)
as Genkernel does for Gentoo as well as a python interface to sys-boot/boot-update for Funtoo.
Genkernel being a bash script, interfacing it with boot-update is 'tricky' if not insane.

KIGen tries to provide a flexible approach to shipping binaries in an initramfs. In theory,
one can ship any binary, statically or dynamically linked. If it's linked the appropriated 
libraries need to be shipped as well. 
KIGen tries to provide a host and source binary for each feature in case one breaks. This way
one can use Portage binaries or the sources from KIGen. It does not matter as long as it works.
KIGen attempts to detect and ship dynamically linked binaries. It does not matter any more as long as it works ;P

KIGen provides a more visible configuration file than genkernel in terms of kernel modules,
custom URLs or versions.
KIGen will automagically detect if you are running boot-update (we support Gentoo and
Sabayon too) then read your /etc/boot.conf and overwrite your /etc/kigen.conf
configuration in terms of kernel modules only.

Features
~~~~~~~~

- LUKS
- LVM2
- UUID
- DMRAID
- EVMS
- splash decorator
- customizable busybox toolbox
  - system/network stack tools
  - alot more
- SSH daemon (dropbear)
- strace (for troubleshoot)
- screen (for convenience)
- keymaps (imported from genkernel)
- ttyecho binary (handy for ssh tty->console)
- GLibC libraries (auth, dns)
- libncurses (required for dropbear)
- zlib (required for dropbear)

Supported OS
~~~~~~~~~~~~

KIGen supports Portage and works on the following linux based flavors:

- Funtoo  and its boot-update interface,
- Gentoo  (no boot-update interface),
- Sabayon (no boot-update interface),
- VLOS    (no boot-update interface).

Portage and Funtoo boot-update support
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In Funtoo, sys-boot/boot-update is now responsible for managing a unified boot
configuration file known as /etc/boot.conf.
It ships all kernel/initramfs boot information and autogenerates /boot/grub/grub.conf
or /boot/grub/grub.cfg depending on your GRUB version (in Funtoo, grub-0.97 is
known as sys-boot/grub-legacy and grub-1.97 as sys-boot/grub).

KIGen imports colors from Portage itself. It keeps the code simpler.
If Portage API cannot be found color are disabled, hence non Portage systems
don't and won't have any color support.

KIGen will detect /etc/boot.conf and will append the modules configuration from /etc/kigen.conf
with the content of the load-modules variable set in Coreboot.

/etc/boot.conf sample::

  initrd {
    load-modules ext4
  }

/etc/kigen.conf sample::

  MODULES_FS = ext3

This will result in shipping 'ext3 ext4' as modules in the initramfs if you have them built as modules.
You can simply ignore either one or the other or both configuration files.

Non Portage support
~~~~~~~~~~~~~~~~~~~

KIgen could in theory work on non Portage Linux systems but does not.
Here is the list of items that depend on Portage.
::
 - Python3 version depends on 
 pyv = os.popen('eselect python show --python3').read().strip()
 sys.path.append("/usr/lib/"+pyv+"/site-packages/kigen/modules")
 - --splash uses media-gfx/splashutils
 - --evms uses sys-fs/evms
 - /usr/bin/portageq used in modules/utils/misc.py def get_distdir(temp):

Portage systems kernel boot options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

KIGen's linuxrc is the same as Genkernel's one except a couple of lines (bug using splash and luks for silent splash).
Some GRUB examples of kernel command line boot options (haven't used LiLo for years).
::
 - LUKS

 - LUKS + DROPBEAR

 - LVM

 - LVM + LUKS

  GRUB 0.97 style

  title KIGen Gentoo Linux 2.6.36-gentoo-r5
  root (hd0,0)
  kernel /boot/kernel-kigen-x86_64-2.6.36-gentoo-r5 root=/dev/ram0 real_root=/dev/mapper/root crypt_root=/dev/sda2 docrypt dokeymap keymap=be vga=791
  initrd /boot/initramfs-kigen-x86_64-2.6.36-gentoo-r5

 - LVM + LUKS + DROPBEAR 

  GRUB 1.98 style

  menuentry "KIGen Sabayon GNU/Linux, with Linux x86_64-2.6.35-sabayon" --class sabayon --class gnu-linux --class gnu --class os {
        insmod ext2
        set root='(hd0,1)'
        search --no-floppy --fs-uuid --set 90527f58-e0d9-4b21-817d-49b223161071
        echo    Loading Linux x86_64-2.6.35-sabayon ...
        linux   /kernel-kigen-x86_64-2.6.35-sabayon ro init=/linuxrc splash=verbose,theme:sabayon vga=791 console=tty1 quiet resume=swap:/dev/mapper/vg_hogbarn-swap real_resume=/dev/mapper/vg_hogbarn-swap dolvm root=/dev/ram0 ramdisk=8192 real_root=/dev/mapper/vg_hogbarn-lv_root crypt_root=/dev/sda2 docrypt dokeymap keymap=be dodropbear ip=dhcp
        echo    Loading initial ramdisk ...
        initrd  /initramfs-kigen-x86_64-2.6.35-sabayon
  }

 - DMRAID

 - DMRAID + LVM + LUKS

Source code notes
~~~~~~~~~~~~~~~~~

KIGen has to make bash calls: no python interface for the kernel Makefile or to compress
a cpio initramfs.

I found no decent python cpio libraries (one is read-only). If you know one that could handle
the job, please mail me to let me know.
Therefore, you shoud understand why I made some choices from the source code point of
view.
As long as we have to make bash calls, we'll have to have to control the return value
of that call. Hence the return 0 logic you can find here and there in KIGen.

**KIGen is on purpose using simple syntax: it's a relaxing project, a drink a smoke some music
and let's geek around, that's the spirit.
It's not rocket science but I do enjoy a lot writing code.** ;P

==============================
Howto build a kernel/initramfs 
==============================

Portage (Gentoo/Sabayon/Funtoo)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Add to local overlay

Download an ebuild of your choice at http://www.github.com/r1k0/kigen/downloads.
If you're not familiar with creating your own overlay, refer to http://www.gentoo.org/proj/en/overlays/userguide.xml.
::
  z13 ~ # mkdir -p /usr/local/portage/sys-kernel/kigen/
  z13 ~ # cd /usr/local/portage/sys-kernel/kigen/
  z13 ~ # wget http://github.com/downloads/r1k0/kigen/kigen-9999.ebuild
  z13 ~ # ebuild kigen-9999.ebuild digest

- Merge KIGen

Optionally set the +doc USE flag or the +module-rebuild one to allow passing 'kigen k --module-rebuild'.
::
  z13 ~ # echo "sys-kernel/kigen doc mdoule-rebuild" >> /etc/portage/package.use

emerge it.
::
  z13 ~ # emerge kigen -av
  
  These are the packages that would be merged, in order:
  
  Calculating dependencies           ... done!
  [ebuild  N     ] sys-kernel/module-rebuild-0.7  0 kB [0]
  [ebuild  N     ] sys-kernel/kigen-9999  USE="doc module-rebuild" 0 kB [1]
  
  Total: 2 packages (2 new), Size of downloads: 0 kB
  Portage tree and overlays:
   [0] /usr/portage
   [1] /usr/local/portage
  
  Would you like to merge these packages? [Yes/No] 
  
  >>> Verifying ebuild manifests
  
  >>> Starting parallel fetch
  
  >>> Emerging (1 of 2) sys-kernel/module-rebuild-0.7
   * Package:    sys-kernel/module-rebuild-0.7
   * Repository: gentoo
   * Maintainer: kernel-misc@gentoo.org
   * USE:        amd64 elibc_glibc kernel_linux multilib userland_GNU
   * FEATURES:   preserve-libs sandbox
  >>> Unpacking source...
  >>> Source unpacked in /var/tmp/portage/sys-kernel/module-rebuild-0.7/work
  >>> Compiling source in /var/tmp/portage/sys-kernel/module-rebuild-0.7/work ...
  >>> Source compiled.
  >>> Test phase [not enabled]: sys-kernel/module-rebuild-0.7
  
  >>> Install module-rebuild-0.7 into /var/tmp/portage/sys-kernel/module-rebuild-0.7/image/ category sys-kernel
  >>> Completed installing module-rebuild-0.7 into /var/tmp/portage/sys-kernel/module-rebuild-0.7/image/
  
  
  >>> Installing (1 of 2) sys-kernel/module-rebuild-0.7
   * checking 1 files for package collisions
  >>> Merging sys-kernel/module-rebuild-0.7 to /
  --- /usr/
  --- /usr/sbin/
  >>> /usr/sbin/module-rebuild
  >>> sys-kernel/module-rebuild-0.7 merged.
  
  >>> Emerging (2 of 2) sys-kernel/kigen-9999 from r1k0
   * Package:    sys-kernel/kigen-9999
   * Repository: r1k0
   * USE:        amd64 doc elibc_glibc kernel_linux module-rebuild multilib userland_GNU
   * FEATURES:   preserve-libs sandbox
  >>> Unpacking source...
   * GIT update -->
   *    repository:       git://github.com/r1k0/kigen.git
   *    at the commit:        61e647ed54180ef7cb49f3178e3bf9b33e94ec55
   *    branch:           master
   *    storage directory:    "/usr/portage/distfiles/git-src/kigen"
  Cloning into /var/tmp/portage/sys-kernel/kigen-9999/work/kigen-9999...
  done.
  >>> Unpacked to /var/tmp/portage/sys-kernel/kigen-9999/work/kigen-9999
  >>> Source unpacked in /var/tmp/portage/sys-kernel/kigen-9999/work
  >>> Preparing source in /var/tmp/portage/sys-kernel/kigen-9999/work/kigen-9999 ...
  >>> Source prepared.
  >>> Configuring source in /var/tmp/portage/sys-kernel/kigen-9999/work/kigen-9999 ...
  >>> Source configured.
  >>> Compiling source in /var/tmp/portage/sys-kernel/kigen-9999/work/kigen-9999 ...
  >>> Source compiled.
  >>> Test phase [not enabled]: sys-kernel/kigen-9999
  
  >>> Install kigen-9999 into /var/tmp/portage/sys-kernel/kigen-9999/image/ category sys-kernel
  >>> Completed installing kigen-9999 into /var/tmp/portage/sys-kernel/kigen-9999/image/
  
  ecompressdir: bzip2 -9 /usr/share/man
  
  >>> Installing (2 of 2) sys-kernel/kigen-9999
   * checking 77 files for package collisions
  >>> Merging sys-kernel/kigen-9999 to /
  --- /usr/
  --- /usr/lib/
  --- /usr/lib/python3.2/
  --- /usr/lib/python3.2/site-packages/
  --- /usr/lib/python3.2/site-packages/kigen/
  --- /usr/lib/python3.2/site-packages/kigen/modules/
  --- /usr/lib/python3.2/site-packages/kigen/modules/initramfs/
  --- /usr/lib/python3.2/site-packages/kigen/modules/initramfs/bin/
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/bin/__init__.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/bin/busybox.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/bin/disklabel.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/bin/dmraid.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/bin/dropbear.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/bin/evms.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/bin/glibc.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/bin/libncurses.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/bin/luks.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/bin/lvm2.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/bin/screen.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/bin/strace.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/bin/zlib.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/dev/
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/dev/__init__.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/dev/aufs.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/dev/device_mapper.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/dev/fuse.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/dev/gnupg.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/dev/iscsi.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/dev/multipath.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/dev/splash.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/dev/unionfs_fuse.py
  --- /usr/lib/python3.2/site-packages/kigen/modules/initramfs/sources/
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/sources/__init__.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/sources/busybox.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/sources/dmraid.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/sources/dropbear.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/sources/e2fsprogs.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/sources/luks.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/sources/lvm2.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/sources/screen.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/sources/strace.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/__init__.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/append.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/bootupdate.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/compress.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/extract.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/initramfs/initramfs.py
  --- /usr/lib/python3.2/site-packages/kigen/modules/kernel/
  >>> /usr/lib/python3.2/site-packages/kigen/modules/kernel/__init__.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/kernel/extract.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/kernel/kernel.py
  --- /usr/lib/python3.2/site-packages/kigen/modules/utils/
  >>> /usr/lib/python3.2/site-packages/kigen/modules/utils/__init__.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/utils/fstab.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/utils/isstatic.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/utils/listdynamiclibs.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/utils/misc.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/utils/process.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/__init__.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/cliparser.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/credits.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/default.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/etcparser.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/nocolor.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/stdout.py
  >>> /usr/lib/python3.2/site-packages/kigen/modules/usage.py
  --- /usr/share/
  --- /usr/share/kigen/
  >>> /usr/share/kigen/arch/
  >>> /usr/share/kigen/arch/x86/
  >>> /usr/share/kigen/arch/x86/busybox.config
  >>> /usr/share/kigen/arch/x86/kernel.config
  >>> /usr/share/kigen/arch/x86_64/
  >>> /usr/share/kigen/arch/x86_64/busybox.config
  >>> /usr/share/kigen/arch/x86_64/kernel.config
  >>> /usr/share/kigen/defaults/
  >>> /usr/share/kigen/defaults/initrd.defaults
  >>> /usr/share/kigen/defaults/initrd.scripts
  >>> /usr/share/kigen/defaults/keymaps.tar.gz
  >>> /usr/share/kigen/defaults/linuxrc
  >>> /usr/share/kigen/defaults/modprobe
  >>> /usr/share/kigen/defaults/udhcpc.scripts
  >>> /usr/share/kigen/tools/
  >>> /usr/share/kigen/tools/ttyecho.c
  >>> /usr/share/kigen/scripts/
  >>> /usr/share/kigen/scripts/boot-luks-lvm.sh
  >>> /usr/share/kigen/scripts/boot-luks.sh
  --- /usr/share/man/
  --- /usr/share/man/man8/
  >>> /usr/share/man/man8/kigen.8.bz2
  --- /usr/share/doc/
  >>> /usr/share/doc/kigen-9999/
  >>> /usr/share/doc/kigen-9999/README.rst.bz2
  >>> /usr/share/doc/kigen-9999/TODO.bz2
  --- /usr/sbin/
  >>> /usr/sbin/kigen
  --- /etc/
  >>> /etc/kigen/
  >>> /etc/kigen/initramfs/
  >>> /etc/kigen/initramfs/default.conf
  >>> /etc/kigen/initramfs/modules.conf
  >>> /etc/kigen/initramfs/url.conf
  >>> /etc/kigen/initramfs/version.conf
  >>> /etc/kigen/kernel/
  >>> /etc/kigen/kernel/default.conf
  >>> /etc/kigen/master.conf
   * 
   * This is still experimental software, be cautious.
   * 
   * Tell me what works and breaks for you by dropping a comment at
   * http://www.openchill.org/?cat=11
   * 
  >>> sys-kernel/kigen-9999 merged.
  
  >>> Recording sys-kernel/kigen in "world" favorites file...
  >>> Auto-cleaning packages...
  
  >>> No outdated packages were found on your system.
  
   * GNU info directory index is up-to-date.
  z13 ~ # 

- Care for **/etc/kigen/**

Kigen has 3 sets of config files:
 - /etc/kigen/master.conf
 - /etc/kigen/kernel/default.conf
 - /etc/kigen/initramfs/{default.conf,modules.conf,version.conf,url.conf}

They are heavily commented, their options should be self explanatory.

**Remember that command line parameters will always overwrite the config files.**

- Main help menu

Main
::
  pong ~ # kigen
  
    a Portage kernel|initramfs generator
  
  Usage:
        /usr/sbin/kigen <options|target> [parameters]
  
  Options:
    --help, -h                 This and examples
    --nocolor, -n              Do not colorize output
    --version                  Version
    --credits                  Credits and license
  
  Targets:
    kernel, k                  Build kernel/modules
    initramfs, i               Build initramfs
    tool, t                    Use handy tools
  
  Parameters:
   kigen kernel                --help, -h
   kigen initramfs             --help, -h
   kigen tool                  --help, -h
  pong ~ # 

- Use of **kigen kernel** to generate a kernel/system.map

Help menu.
::
  z13 ~ # kigen k -h
  Parameter:                   Config value:      Description:
  
  Kernel:
    --dotconfig=/file          ""                 Custom kernel .config file
    --initramfs=/file          ""                 Embed initramfs into the kernel
    --fixdotconfig=<feature>   ""                 Check and auto fix the kernel config file (experimental)
    --clean                    False              Clean precompiled objects only
    --mrproper                 False              Clean precompiled objects and remove config file
    --menuconfig               False              Interactive kernel options menu
    --fakeroot=/dir            "/"                Append modules to /dir/lib/modules
    --nooldconfig              False              Do not ask for new kernel/initramfs options
    --nomodinstall             False              Do not install modules
    --nomodules                False              Do not compile or install modules
  
  Misc:
    --nosaveconfig             False              Do not save kernel config in /etc/kernels
    --noboot                   False              Do not copy kernel to /boot
    --rename=/file             ""                 Custom kernel file name
    --logfile=/file            "/var/log/kigen.log" 
    --debug, -d                False              Debug verbose
  z13 ~ # 

Default behavior.
::
  z13 ~ # kigen k
   * Gentoo Base System release 2.0.2 on x86_64
   * Kernel sources Makefile version 2.6.38-gentoo-r5 aka Flesh-EatingBatswithFangs
   * kernel.copy_config /usr/src/linux/.config -> /usr/src/linux/.config-2011-06-17-14-39-59
   * kernel.oldconfig 
  scripts/kconfig/conf --oldconfig Kconfig
  #
  # configuration written to .config
  #
   * kernel.prepare 
   * kernel.bzImage 
   * kernel.modules 
   * kernel.modules_install /lib/modules
   * saved /etc/kernels/dotconfig-kigen-x86_64-2.6.38-gentoo-r5
   * success 2.9Mb /boot/System.map-kigen-x86_64-2.6.38-gentoo-r5
   * success 5.4Mb /boot/kernel-kigen-x86_64-2.6.38-gentoo-r5
  z13 ~ # 

It is up to you to adapt your /etc/lilo.conf or /boot/grub/grub.cfg file.

- Use of **kigen initramfs** to generate an initramfs

Help menu.
::
  z13 ~ # kigen i -h
  Parameter:          Config value:   Description:
  
  Features:
  + from source code
  | --source-luks             False       Include LUKS support from sources
  | --source-lvm2             False       Include LVM2 support from sources
  | --source-dropbear         False       Include dropbear support from sources
  |  --debugflag              False        Compile dropbear with #define DEBUG_TRACE in debug.h
  | --source-screen           False       Include the screen binary tool from sources
  | --source-disklabel        False       Include support for UUID/LABEL from sources
  | --source-ttyecho          False       Compile and include the handy ttyecho.c tool
  | --source-strace           False       Compile and include the strace binary tool from sources
  | --source-dmraid           False       Include DMRAID support from sources
  | --source-all              False       Include all possible features from sources
  + from host binaries
  | --bin-busybox             False       Include busybox support from host
  | --bin-luks                Flase       Include LUKS support from host
  | --bin-lvm2                False       Include LVM2 support from host
  | --bin-dropbear            False       Include dropbear support from host
  | --bin-screen              False       Include the screen binary tool from host
  | --bin-disklabel           False       Include support for UUID/LABEL from host
  | --bin-strace              False       Include the strace binary tool from host
  | --bin-evms                False       Include the evms binary tool from host
  | --bin-glibc               False       Include host GNU C libraries (required for dns,dropbear)
  | --bin-libncurses          False       Include host libncurses (required for dropbear)
  | --bin-zlib                False       Include host zlib (required for dropbear)
  | --bin-dmraid              False       Include DMRAID support from host
  | --bin-all                 False       Include all possible features from host
  
    --dynlibs                 False       Include detected libraries from dynamically linked binaries
    --splash=<theme>          ""          Include splash support (splashutils must be merged)
     --sres=YxZ[,YxZ]         ""           Splash resolution, all if not set
    --rootpasswd=<passwd>     ""          Create and set root password (required for dropbear)
    --keymaps=xx[,xx]|all     "all"           Include all keymaps
    --plugin=/dir[,/dir]      ""          Include list of user generated custom roots
  
  Busybox:
    --dotconfig=/file         ""          Custom busybox config file
    --defconfig               False       Set .config to largest generic options
    --oldconfig               False       Ask for new busybox options if any
    --menuconfig              False       Interactive busybox options menu
  
  Misc:
    --nocache                 False       Delete previous cached data on startup
    --nomodules               False       Do not install kernel modules (all is kernel builtin)
    --noboot                  False       Do not copy initramfs to /boot
    --rename=/file            ""          Custom initramfs file name
    --logfile=/file           "/var/log/kigen.log"
    --debug, -d               False       Debug verbose
  z13 ~ # 

Default behavior.
::
  z13 ~ # kigen i 
   * Gentoo Base System release 2.0.2 on x86_64
   * initramfs.append.base
   * ... Gentoo linuxrc 3.4.15 patched
   * initramfs.append.modules 2.6.38-gentoo-r5
   * ... MODULES_SATA  
   * ... MODULES_DMRAID    
   * ... MODULES_MDADM     
   * ... MODULES_VIDEO     intel-agp drm drm_kms_helper i915 i2c-algo-bit 
   * ... MODULES_ISCSI     iscsi_tcp 
   * ... MODULES_MISC  
   * ... MODULES_CRYPT     
   * ... MODULES_FS    
   * ... MODULES_WAITSCAN  scsi_wait_scan 
   * ... MODULES_USB   ehci-hcd ohci-hcd sl811-hcd uhci-hcd 
   * ... MODULES_SCSI  sx8 fdomain imm 
   * ... MODULES_PATA  pata_legacy pata_pcmcia 
   * ... MODULES_FIREWIRE  
   * ... MODULES_NET   sky2 tg3 atl1c e1000 e1000e 
   * ... MODULES_LVM   
   * ... MODULES_EVMS  
   * ... MODULES_ATARAID   
   * ... MODULES_PCMCIA    i82092 pcmcia pd6729 yenta_socket 
   * initramfs.append.source.busybox 1.18.4
   * ... busybox.download
   * ... busybox.extract
   * ... busybox.copy_config 
   * ... busybox.make
   * ... busybox.strip
   * ... busybox.compress
   * ... busybox.cache
   * initramfs.append.keymaps all
   * ... azerty be bg br-a br-l 
   * ... by cf croat cz de dk 
   * ... dvorak es et fi fr gr 
   * ... hu il is it jp keymapList 
   * ... la lt mk nl no pl 
   * ... pt ro ru se sg sk-y 
   * ... sk-z slovene trf trq ua uk 
   * ... us wangbe 
   * initramfs.compress
   * boot.mounted
   * success 1.8Mb /boot/initramfs-kigen-x86_64-2.6.38-gentoo-r5
   * boot.umounted
  z13 ~ # 

Generally, what can be compiled with KIGen should be cacheable.
In this case, busybox cache is used.
::
  z13 ~ # kigen i 
   * Gentoo Base System release 2.0.2 on x86_64
   * initramfs.append.base
   * ... Gentoo linuxrc 3.4.15 patched
   * initramfs.append.modules 2.6.38-gentoo-r5
   * ... MODULES_SATA  
   * ... MODULES_DMRAID    
   * ... MODULES_MDADM     
   * ... MODULES_VIDEO     intel-agp drm drm_kms_helper i915 i2c-algo-bit 
   * ... MODULES_ISCSI     iscsi_tcp 
   * ... MODULES_MISC  
   * ... MODULES_CRYPT     
   * ... MODULES_FS    
   * ... MODULES_WAITSCAN  scsi_wait_scan 
   * ... MODULES_USB   ehci-hcd ohci-hcd sl811-hcd uhci-hcd 
   * ... MODULES_SCSI  sx8 fdomain imm 
   * ... MODULES_PATA  pata_legacy pata_pcmcia 
   * ... MODULES_FIREWIRE  
   * ... MODULES_NET   sky2 tg3 atl1c e1000 e1000e 
   * ... MODULES_LVM   
   * ... MODULES_EVMS  
   * ... MODULES_ATARAID   
   * ... MODULES_PCMCIA    i82092 pcmcia pd6729 yenta_socket 
   * initramfs.append.source.busybox 1.18.4
   * ... cache found: importing
   * initramfs.append.keymaps all
   * ... azerty be bg br-a br-l 
   * ... by cf croat cz de dk 
   * ... dvorak es et fi fr gr 
   * ... hu il is it jp keymapList 
   * ... la lt mk nl no pl 
   * ... pt ro ru se sg sk-y 
   * ... sk-z slovene trf trq ua uk 
   * ... us wangbe 
   * initramfs.compress
   * boot.mounted
   * success 1.8Mb /boot/initramfs-kigen-x86_64-2.6.38-gentoo-r5
   * boot.umounted
  z13 ~ # 

Now let's make a full blown initramfs.
::
  z13 ~ # kigen i --splash=emergence --source-disklabel --source-luks --bin-lvm2 --source-dropbear --debugflag --rootpasswd=mypasswd --keymaps=all --source-ttyecho --source-strace --source-screen --bin-glibc --bin-zlib --bin-libncurses --defconfig --nocache
   * Gentoo Base System release 2.0.2 on x86_64
   * initramfs.append.base
   * ... Gentoo linuxrc 3.4.15 patched
   * initramfs.append.modules 2.6.38-gentoo-r5
   * ... MODULES_SATA  
   * ... MODULES_DMRAID    
   * ... MODULES_MDADM     
   * ... MODULES_VIDEO     intel-agp drm drm_kms_helper i915 i2c-algo-bit 
   * ... MODULES_ISCSI     iscsi_tcp 
   * ... MODULES_MISC  
   * ... MODULES_CRYPT     
   * ... MODULES_FS    
   * ... MODULES_WAITSCAN  scsi_wait_scan 
   * ... MODULES_USB   ehci-hcd ohci-hcd sl811-hcd uhci-hcd 
   * ... MODULES_SCSI  sx8 fdomain imm 
   * ... MODULES_PATA  pata_legacy pata_pcmcia 
   * ... MODULES_FIREWIRE  
   * ... MODULES_NET   sky2 tg3 atl1c e1000 e1000e 
   * ... MODULES_LVM   
   * ... MODULES_EVMS  
   * ... MODULES_ATARAID   
   * ... MODULES_PCMCIA    i82092 pcmcia pd6729 yenta_socket 
   * initramfs.append.source.busybox 1.18.4
   * ... busybox.extract
   * ... busybox.copy_config 
   * ... busybox.defconfig
   * ... busybox.make
   * ... busybox.strip
   * ... busybox.compress
   * ... busybox.cache
   * initramfs.append.bin.lvm2 /sbin/lvm.static from host
   * initramfs.append.source.luks 1.3.1
   * ... luks.download
   * ... luks.extract
   * ... luks.configure
   * ... luks.make
   * ... luks.strip
   * ... luks.compress
   * ... luks.cache
   * initramfs.append.source.disklabel 1.41.14
   * ... e2fsprogs.download
   * ... e2fsprogs.extract
   * ... e2fsprogs.configure
   * ... e2fsprogs.make
   * ... e2fsprogs.strip
   * ... e2fsprogs.compress
   * ... e2fsprogs.cache
   * initramfs.append.source.dropbear 0.53
   * ... dropbear.download
   * ... dropbear.extract
   * ... dropbear.patch_debug_header #define DEBUG_TRACE
   * ... dropbear.configure
   * ... dropbear.make
   * ... dropbear.strip
   * ... dropbear.dsskey
  Will output 1024 bit dss secret key to '/var/tmp/kigen/work/dropbear-0.53/etc/dropbear/dropbear_dss_host_key'
  Generating key, this may take a while...
   * ... dropbear.rsakey
  Will output 4096 bit rsa secret key to '/var/tmp/kigen/work/dropbear-0.53/etc/dropbear/dropbear_rsa_host_key'
  Generating key, this may take a while...
   * ... dropbear.compress
   * ... dropbear.cache
   * initramfs.append.source.strace 4.5.20
   * ... strace.download
   * ... strace.extract
   * ... strace.configure
   * ... strace.make
   * ... strace.strip
   * ... strace.compress
   * ... strace.cache
   * initramfs.append.source.screen 4.0.3
   * ... screen.download
   * ... screen.extract
   * ... screen.configure
   * ... screen.make
   * ... screen.strip
   * ... screen.compress
   * ... screen.cache
   * initramfs.append.source.ttyecho
   * ... gcc -static /usr/share/kigen/tools/ttyecho.c
   * ...     -o /var/tmp/kigen/work/initramfs-source-ttyecho-temp/sbin/ttyecho
   * initramfs.append.bin.glibc
   * ... /lib/libm.so.6
   * ... /lib/libnss_files.so.2
   * ... /lib/libnss_dns.so.2
   * ... /lib/libnss_nis.so.2
   * ... /lib/libnsl.so.1
   * ... /lib/libresolv.so.2
   * ... /lib/ld-linux.so.2
   * ... /lib/ld-linux-x86-64.so.2
   * ... /lib/libc.so.6
   * ... /lib/libnss_compat.so.2
   * ... /lib/libutil.so.1
   * ... /etc/ld.so.cache
   * ... /lib/libcrypt.so.1
   * initramfs.append.bin.libncurses
   * ... /lib/libncurses.so.5
   * initramfs.append.bin.zlib
   * ... /lib/libz.so.1
   * initramfs.append.splash emergence 
   * initramfs.append.rootpasswd
   * ... /etc/passwd
   * ... /etc/group
   * initramfs.append.keymaps all
   * ... azerty be bg br-a br-l 
   * ... by cf croat cz de dk 
   * ... dvorak es et fi fr gr 
   * ... hu il is it jp keymapList 
   * ... la lt mk nl no pl 
   * ... pt ro ru se sg sk-y 
   * ... sk-z slovene trf trq ua uk 
   * ... us wangbe 
   * initramfs.compress
   * boot.mounted
   * success 13.2Mb /boot/initramfs-kigen-x86_64-2.6.38-gentoo-r5
   * boot.umounted
  z13 ~ # 

Typically this adds support for splash/luks/lvm2/dropbear to the initramfs.
Note that by default kigen will will fetch the sources and link statically.
Passing --bin-all --dynlibs will use host binaries when possible.

It is up to you to adapt your /etc/lilo.conf or /boot/grub/grub.cfg file.

KIGen has a toolbox. It is provided for convenience (read lazyness).
It lets you extract a .config file from a kernel.
::
  z13 ~ # kigen tool
  Parameter:          Config value:   Description:
  
  Kernel:
    --getdotconfig=/vmlinux   ""          Extract .config from compiled binary kernel (if IKCONFIG has been set)
  
  Initramfs:
    --extract=/file           ""                  Extract initramfs file
     --to=/dir                "/var/tmp/kigen/extracted-initramfs"
                           Custom extracting directory
    --compress=/dir           ""                  Compress directory into initramfs
     --into=/file             "/var/tmp/kigen/compressed-initramfs/initramfs_data.cpio.gz"
                           Custom initramfs file
  
  Misc:
    --rmcache                 False       Remove cached data
  z13 ~ # mount /boot
  z13 ~ # kigen tool --getdotconfig=/boot/kernel-kigen-x86_64-2.6.38-gentoo-r5 
   * Gentoo Base System release 2.0.3 on x86_64
   * kernel.extract.getdotconfig from /boot/kernel-kigen-x86_64-2.6.38-gentoo-r5 to /var/tmp/kigen/dotconfig
  z13 ~ # head /var/tmp/kigen/dotconfig
  #
  # Automatically generated make config: don't edit
  # Linux/x86_64 2.6.38-gentoo-r5 Kernel Configuration
  # Sun Jun 19 20:23:40 2011
  #
  CONFIG_64BIT=y
  # CONFIG_X86_32 is not set
  CONFIG_X86_64=y
  CONFIG_X86=y
  CONFIG_INSTRUCTION_DECODER=y
  z13 ~ # 

You can easily extract an initramfs for troubleshooting or the sake of customization.
::
  z13 ~ # kigen t --extract=/boot/initramfs-kigen-x86_64-2.6.38-gentoo-r5
   * Gentoo Base System release 2.0.3 on x86_64
   * tool.extract.initramfs to /var/tmp/kigen/extracted-initramfs
  z13 ~ # ls -ls /var/tmp/kigen/extracted-initramfs
  total 20
   0 drwxr-xr-x 1 root root   212 Jun 20 10:46 bin
   0 drwxr-xr-x 1 root root    82 Jun 20 10:46 dev
   0 drwxr-xr-x 1 root root   250 Jun 20 10:46 etc
   0 drwxr-xr-x 1 root root     0 Jun 20 10:46 home
  20 -rwxr-xr-x 1 root root 18642 Jun 20 10:46 init
   0 drwxr-xr-x 1 root root    96 Jun 20 10:46 lib
   0 lrwxrwxrwx 1 root root     3 Jun 20 10:46 lib64 -> lib
   0 lrwxrwxrwx 1 root root     4 Jun 20 10:46 linuxrc -> init
   0 drwxr-xr-x 1 root root     0 Jun 20 10:46 proc
   0 drwxr-xr-x 1 root root    56 Jun 20 10:46 root
   0 drwxr-xr-x 1 root root   134 Jun 20 10:46 sbin
   0 drwxr-xr-x 1 root root     0 Jun 20 10:46 sys
   0 drwxr-xr-x 1 root root     0 Jun 20 10:46 tmp
   0 drwxr-xr-x 1 root root    34 Jun 20 10:46 usr
   0 drwxr-xr-x 1 root root    20 Jun 20 10:46 var
  z13 ~ # 

You can actually create your own initramfs environment and litterally compress it.
You can then do some tweaking and then close again the initramfs.
::
  z13 ~ # kigen t --compress=/var/tmp/kigen/extracted-initramfs
   * Gentoo Base System release 2.0.3 on x86_64
   * tool.compress.initramfs from /var/tmp/kigen/extracted-initramfs into /var/tmp/kigen/compressed-initramfs/initramfs_data.cpio.gz
  z13 ~ # ls -ls /var/tmp/kigen/compressed-initramfs/initramfs_data.cpio.gz
  12568 -rw-r--r-- 1 root root 12867574 Jun 20 11:13 /var/tmp/kigen/compressed-initramfs/initramfs_data.cpio.gz
  z13 ~ # 

APT (Debian/Ubuntu)
~~~~~~~~~~~~~~~~~~~

TODO?

==========================================
Howto boot LUKS/LVM through SSH (dropbear)
==========================================

Warning: this only works with ethernet devices.
TODO: wlan devices.

Build initramfs with SSH support
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Make sure libraries are called.
::
  z13 ~ # kigen i --splash=emergence --source-disklabel --source-luks --bin-lvm2 --source-dropbear --debugflag --rootpasswd=mypasswd --keymaps=all --source-ttyecho --source-strace --source-screen --bin-glibc --bin-zlib --bin-libncurses --defconfig 
   * Gentoo Base System release 2.0.2 on x86_64
   * initramfs.append.base
   * ... Gentoo linuxrc 3.4.15 patched
   * initramfs.append.modules 2.6.38-gentoo-r5
   * ... MODULES_SATA  
   * ... MODULES_DMRAID    
   * ... MODULES_MDADM     
   * ... MODULES_VIDEO     intel-agp drm drm_kms_helper i915 i2c-algo-bit 
   * ... MODULES_ISCSI     iscsi_tcp 
   * ... MODULES_MISC  
   * ... MODULES_CRYPT     
   * ... MODULES_FS    
   * ... MODULES_WAITSCAN  scsi_wait_scan 
   * ... MODULES_USB   ehci-hcd ohci-hcd sl811-hcd uhci-hcd 
   * ... MODULES_SCSI  sx8 fdomain imm 
   * ... MODULES_PATA  pata_legacy pata_pcmcia 
   * ... MODULES_FIREWIRE  
   * ... MODULES_NET   sky2 tg3 atl1c e1000 e1000e 
   * ... MODULES_LVM   
   * ... MODULES_EVMS  
   * ... MODULES_ATARAID   
   * ... MODULES_PCMCIA    i82092 pcmcia pd6729 yenta_socket 
   * initramfs.append.source.busybox 1.18.4
   * ... cache found: importing
   * initramfs.append.bin.lvm2 /sbin/lvm.static from host
   * initramfs.append.source.luks 1.3.1
   * ... cache found: importing
   * initramfs.append.source.disklabel 1.41.14
   * ... cache found: importing
   * initramfs.append.source.dropbear 0.53
   * ... cache found: importing
   * initramfs.append.source.strace 4.5.20
   * ... cache found: importing
   * initramfs.append.source.screen 4.0.3
   * ... cache found: importing
   * initramfs.append.source.ttyecho
   * ... gcc -static /usr/share/kigen/tools/ttyecho.c
   * ...     -o /var/tmp/kigen/work/initramfs-source-ttyecho-temp/sbin/ttyecho
   * initramfs.append.bin.glibc
   * ... /lib/libm.so.6
   * ... /lib/libnss_files.so.2
   * ... /lib/libnss_dns.so.2
   * ... /lib/libnss_nis.so.2
   * ... /lib/libnsl.so.1
   * ... /lib/libresolv.so.2
   * ... /lib/ld-linux.so.2
   * ... /lib/ld-linux-x86-64.so.2
   * ... /lib/libc.so.6
   * ... /lib/libnss_compat.so.2
   * ... /lib/libutil.so.1
   * ... /etc/ld.so.cache
   * ... /lib/libcrypt.so.1
   * initramfs.append.bin.libncurses
   * ... /lib/libncurses.so.5
   * initramfs.append.bin.zlib
   * ... /lib/libz.so.1
   * initramfs.append.splash emergence 
   * initramfs.append.rootpasswd
   * ... /etc/passwd
   * ... /etc/group
   * initramfs.append.keymaps all
   * ... azerty be bg br-a br-l 
   * ... by cf croat cz de dk 
   * ... dvorak es et fi fr gr 
   * ... hu il is it jp keymapList 
   * ... la lt mk nl no pl 
   * ... pt ro ru se sg sk-y 
   * ... sk-z slovene trf trq ua uk 
   * ... us wangbe 
   * initramfs.compress
   * boot.mounted
   * success 13.2Mb /boot/initramfs-kigen-x86_64-2.6.38-gentoo-r5
   * boot.umounted
  z13 ~ # 

Set kernel command option
~~~~~~~~~~~~~~~~~~~~~~~~~

To boot in SSH mode, pass the 'dodropbear' option in the kernel command line.
Edit /boot/grub/grub.cfg to have the kernel command line look like.
::
  linux /kernel-kigen-x86_64-2.6.37-gentoo ro single init=/linuxrc splash=verbose,theme:sabayon vga=791 console=tty1 quiet resume=swap:/dev/mapper/vg_hogbarn-swap real_resume=/dev/mapper/vg_hogbarn-swap dolvm root=/dev/ram0 ramdisk=8192 real_root=/dev/mapper/vg_hogbarn-lv_root crypt_root=/dev/sda2 docrypt dokeymap keymap=be dodropbear ip=dhcp

Kill dropbear daemon and restart openssh (DEPRECATED)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**The linuxrc should kill dropbear automagically.**

Make sure existing connections with initramfs are killed and openssh binds to :22 correctly.
Add on the following to /etc/conf.d/local.
::
  pkill dropbear
  sleep 1
  /etc/init.d/sshd restart

Connect to initramfs and boot remotely
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ssh to initramfs (you might have to remove the previous certificate in .ssh/known_hosts).
::
  z13 ~ # ssh 192.168.1.70
  The authenticity of host '192.168.1.70 (192.168.1.70)' can't be established.
  RSA key fingerprint is 7b:12:41:2a:fc:18:1c:23:81:b5:02:6e:a9:8e:c3:70.
  Are you sure you want to continue connecting (yes/no)? yes
  Warning: Permanently added '192.168.1.70' (RSA) to the list of known hosts.
  root@192.168.1.70's password: 
  
  
  BusyBox v1.18.4 (2011-06-17 21:10:46 CEST) built-in shell (ash)
  Enter 'help' for a list of built-in commands.
  
  # uname -a
  Linux (none) 2.6.39-sabayon #3 SMP Wed Jun 15 17:51:49 CEST 2011 i686 GNU/Linux
  # ls -l /
  drwxr-xr-x    2 root     root             0 Jun 17 23:07 bin
  drwxr-xr-x    4 root     root         13380 Jun 17 23:07 dev
  drwxr-xr-x    7 root     root             0 Jun 17 23:07 etc
  drwxr-xr-x    2 root     root             0 Jun 17 23:02 home
  -rwxr-xr-x    1 root     root         18642 Jun 17 23:02 init
  drwxr-xr-x    6 root     root             0 Jun 17 23:02 lib
  lrwxrwxrwx    1 root     root             3 Jun 17 23:02 lib64 -> lib
  -rw-r--r--    1 root     root           214 Jun 17 23:07 modules.cache
  dr-xr-xr-x   72 root     root             0 Jun 17 23:06 proc
  drwxr-xr-x    2 root     root             0 Jun 17 23:02 root
  drwxr-xr-x    2 root     root             0 Jun 17 23:07 sbin
  drwxr-xr-x   12 root     root             0 Jun 17 23:07 sys
  drwxr-xr-x    2 root     root             0 Jun 17 23:02 tmp
  drwxr-xr-x    6 root     root             0 Jun 17 23:02 usr
  drwxr-xr-x    5 root     root             0 Jun 17 23:02 var
  # ip a
  1: lo: <LOOPBACK> mtu 16436 qdisc noop state DOWN 
      link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
  2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
      link/ether 08:00:27:50:5e:a3 brd ff:ff:ff:ff:ff:ff
      inet 192.168.1.70/24 brd 192.168.1.255 scope global eth0
  # netstat
  Active Internet connections (w/o servers)
  Proto Recv-Q Send-Q Local Address           Foreign Address         State       
  tcp        0      0 Unknown-08-00-27-50-5e-a3.lan:22 z13.lan:34046           ESTABLISHED 
  Active UNIX domain sockets (w/o servers)
  Proto RefCnt Flags       Type       State         I-Node Path
  # ps
    PID USER       VSZ STAT COMMAND
      1 root      1596 S    /bin/sh /init dokeymap dolvm docrypt dokeymap dodrop
      2 root         0 SW   [kthreadd]
      3 root         0 SW   [ksoftirqd/0]
      4 root         0 SW   [kworker/0:0]
      5 root         0 SW   [kworker/u:0]
      6 root         0 SW   [migration/0]
      7 root         0 SW<  [cpuset]
      8 root         0 SW<  [khelper]
      9 root         0 SW   [kworker/u:1]
     31 root         0 SW<  [netns]
    493 root         0 SW   [sync_supers]
    495 root         0 SW   [bdi-default]
    496 root         0 SW<  [kintegrityd]
    498 root         0 SW<  [kblockd]
    570 root         0 SW<  [ata_sff]
    582 root         0 SW   [khubd]
    589 root         0 SW<  [md]
    691 root         0 SW   [kworker/0:1]
    711 root         0 SW   [kswapd0]
    712 root         0 SWN  [ksmd]
    781 root         0 SWN  [khugepaged]
    782 root         0 SW   [fsnotify_mark]
    793 root         0 SW   [ecryptfs-kthrea]
    814 root         0 SW<  [crypto]
    826 root         0 SW<  [kthrotld]
   1425 root         0 SW   [cciss_scan]
   1450 root         0 SW<  [iscsi_eh]
   1457 root         0 SW<  [fc_exch_workque]
   1458 root         0 SW<  [fc_rport_eq]
   1461 root         0 SW<  [fnic_event_wq]
   1545 root         0 SW   [scsi_eh_2]
   1548 root         0 SW   [kworker/u:2]
   1563 root         0 SW   [scsi_eh_3]
   1566 root         0 SW   [scsi_eh_4]
   1569 root         0 SW   [kworker/u:3]
   1570 root         0 SW   [kworker/u:4]
   1636 root         0 SW<  [cnic_wq]
   1640 root         0 SW<  [exec-osm]
   1647 root         0 SW<  [block-osm]
   1687 root         0 RW   [kworker/0:2]
   1692 root         0 SW<  [kpsmoused]
   1707 root         0 SW<  [edac-poller]
   1753 root         0 SW   [kworker/u:5]
   4190 root         0 SW   [jfsIO]
   4191 root         0 SW   [jfsCommit]
   4192 root         0 SW   [jfsSync]
   4273 root         0 SW<  [rpciod]
   4375 root         0 SW<  [xfs_mru_cache]
   4376 root         0 SW<  [xfslogd]
   4377 root         0 SW<  [xfsdatad]
   4378 root         0 SW<  [xfsconvertd]
   5066 root      1596 S    udhcpc
   5067 root      1224 S    dropbear -E
   5073 root      1460 S <  cryptsetup luksOpen /dev/sda2 root
   5074 root      4036 S    dropbear -E
   5075 root      1600 S    -sh
   5080 root      4264 R    ps
  # ls
  boot-luks-lvm.sh  boot-luks.sh
  # cat boot-luks-lvm.sh
  #!/bin/sh
  if  [ "$1" = "-h" ]     || \
      [ "$1" = "--help" ] || \
      [ "$1" = "" ]       || \
      [ "$2" = "" ]
  then
      echo "$0 <root device> <lvm root device>"
      echo "i.e. # ./boot-luks-lvm.sh /dev/sda2 /dev/mapper/vg_sabayon-lv_root"
      exit
  fi
  pkill cryptsetup
  sleep 2
  /sbin/cryptsetup luksOpen $1 root
  sleep 2
  /bin/lvm vgscan
  /bin/lvm vgchange -a y
  /sbin/ttyecho -n /dev/console $2
  # ./boot-luks-lvm.sh
  ./boot-luks-lvm.sh <root device> <lvm root device>
  i.e. # ./boot-luks-lvm.sh /dev/sda2 /dev/mapper/vg_sabayon-lv_root
  # ./boot-luks-lvm.sh /dev/sda2 /dev/mapper/vg_sabayon-lv_root
  Enter passphrase for /dev/sda2: 
    Reading all physical volumes.  This may take a while...
    Found volume group "vg_sabayon" using metadata type lvm2
    2 logical volume(s) in volume group "vg_sabayon" now active
  # Connection to 192.168.1.70 closed by remote host.
  Connection to 192.168.1.70 closed.
  z13 ~ # 

The initramfs is now booting from the content of the LUKS container remotely! Yiha
Note the autodeconnection done by the host.

:Authors: 
    erick 'r1k0' michau (python engine),

    Portage community (linuxrc scripts),

:Version: 0.4.3
