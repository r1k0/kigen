=======
General
=======

.. sectnum::

.. contents:: Table of contents

Introduction
~~~~~~~~~~~~

**KIGen now only supports Python3**

**KIGen uses Genkernel linuxrc and provides the same boot interface as Genkernel does.**

KIGen for Linux aims at providing first an equal set of features (in Python)
as Genkernel does for Gentoo as well as a python interface to sys-boot/boot-update for Funtoo.
Genkernel being a bash script, interfacing it with boot-update is 'tricky' if not insane.

KIGen provides a more visible configuration file than genkernel in terms of kernel modules at least.
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
- strace
- screen
- keymaps (imported from genkernel)
- ttyecho binary (handy for ssh tty->console)
- GLibC libraries (auth, dns)
- libncurses
- zlib

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

KIgen could work except for --splash that currently uses splashutils from Portage and provided your custom linuxrc.
KIGen is not meant (for now) to be installed on non Portage systems but will in the future.

Portage systems kernel boot options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

KIGen's linuxrc is the same as Genkernel's one except a couple of lines (bug using splash and luks for silent splash).
Some GRUB examples of kernel command line boot options.
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
        linux   /kernel-kigen-x86_64-2.6.35-sabayon ro init=/linuxrc splash=verbose,theme:sabayon vga=791 console=tty1 quiet resume=swap:/dev/mapper/vg_hogbarn-swap real_resume=/dev/mapper/vg_hogbarn-swap dolvm root=/dev/ram0 ramdisk=8192 real_root=/dev/mapper/vg_hogbarn-lv_root crypt_root=/dev/sda2 docrypt dokeymap keymap=be dodropbear
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

KIGen is on purpose using simple syntax: it's a relaxing project, a drink a smoke some music
and let's geek around, that's the spirit.
It's not rocket science but I do enjoy a lot writing code, it keeps the mind busy ;P

==============================
Howto build a kernel/initramfs 
==============================

Portage (Gentoo/Sabayon/Funtoo)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Add to local overlay

Download an ebuild of your choice at http://www.github.com/r1k0/kigen/downloads.
If you're not familiar with creating your own overlay, refer to http://www.gentoo.org/proj/en/overlays/userguide.xml.
::
  pong ~ # mkdir -p /usr/local/portage/sys-kernel/kigen/
  pong ~ # cd /usr/local/portage/sys-kernel/kigen/
  pong ~ # wget http://github.com/downloads/r1k0/kigen/kigen-9999.ebuild
  pong ~ # ebuild kigen-9999.ebuild digest

- Merge KIGen

Optionally set the +doc USE flag.
::
  pong ~ # echo "sys-kernel/kigen doc" >> /etc/portage/package.use

emerge it.
::
  z13 ~ # emerge kigen -av
  
  These are the packages that would be merged, in order:
  
  Calculating dependencies                   ... done!
  [ebuild  N    ] sys-kernel/kigen-9999  USE="doc" 0 kB [1]
  
  Total: 1 package (1 new), Size of downloads: 0 kB
  Portage tree and overlays:
   [0] /usr/portage
   [1] /usr/local/portage
  
  Would you like to merge these packages? [Yes/No] 
  
  >>> Verifying ebuild manifests
  
  >>> Emerging (1 of 1) sys-kernel/kigen-9999 from r1k0
   * Package:    sys-kernel/kigen-9999
   * Repository: r1k0
   * USE:        amd64 doc elibc_glibc kernel_linux multilib userland_GNU
   * FEATURES:   preserve-libs sandbox
  >>> Unpacking source...
   * GIT NEW clone -->
   *    repository:               git://github.com/r1k0/kigen.git
  Cloning into bare repository /usr/portage/distfiles/git-src/kigen...
  remote: Counting objects: 3456, done.
  remote: Compressing objects: 100% (1137/1137), done.
  remote: Total 3456 (delta 2420), reused 3264 (delta 2293)
  Receiving objects: 100% (3456/3456), 666.88 KiB | 79 KiB/s, done.
  Resolving deltas: 100% (2420/2420), done.
   *    at the commit:            47005719708b5a2136128e186bc922d8def73ed5
   *    branch:                   master
   *    storage directory:        "/usr/portage/distfiles/git-src/kigen"
  Cloning into /var/tmp/portage/sys-kernel/kigen-9999/work/kigen-9999...
  done.
  >>> Unpacked to /var/tmp/portage/sys-kernel/kigen-9999/work/kigen-9999
  >>> Source unpacked in /var/tmp/portage/sys-kernel/kigen-9999/work
  >>> Compiling source in /var/tmp/portage/sys-kernel/kigen-9999/work/kigen-9999 ...
  >>> Source compiled.
  >>> Test phase [not enabled]: sys-kernel/kigen-9999
  
  >>> Install kigen-9999 into /var/tmp/portage/sys-kernel/kigen-9999/image/ category sys-kernel
  >>> Completed installing kigen-9999 into /var/tmp/portage/sys-kernel/kigen-9999/image/
  
  ecompressdir: bzip2 -9 /usr/share/man
  
  >>> Installing (1 of 1) sys-kernel/kigen-9999
   * checking 63 files for package collisions
  --- /usr/
  --- /usr/lib/
  --- /usr/lib/python3.1/
  --- /usr/lib/python3.1/site-packages/
  --- /usr/lib/python3.1/site-packages/kigen/
  --- /usr/lib/python3.1/site-packages/kigen/modules/
  --- /usr/lib/python3.1/site-packages/kigen/modules/initramfs/
  >>> /usr/lib/python3.1/site-packages/kigen/modules/initramfs/dev/
  >>> /usr/lib/python3.1/site-packages/kigen/modules/initramfs/dev/__init__.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/initramfs/dev/aufs.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/initramfs/dev/device_mapper.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/initramfs/dev/fuse.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/initramfs/dev/gnupg.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/initramfs/dev/iscsi.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/initramfs/dev/multipath.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/initramfs/dev/splash.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/initramfs/dev/unionfs_fuse.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/initramfs/sources/
  >>> /usr/lib/python3.1/site-packages/kigen/modules/initramfs/sources/__init__.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/initramfs/sources/busybox.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/initramfs/sources/dmraid.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/initramfs/sources/dropbear.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/initramfs/sources/e2fsprogs.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/initramfs/sources/luks.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/initramfs/sources/lvm2.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/initramfs/sources/screen.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/initramfs/sources/strace.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/initramfs/__init__.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/initramfs/append.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/initramfs/bootupdate.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/initramfs/compress.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/initramfs/extract.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/initramfs/initramfs.py
  --- /usr/lib/python3.1/site-packages/kigen/modules/kernel/
  >>> /usr/lib/python3.1/site-packages/kigen/modules/kernel/__init__.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/kernel/extract.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/kernel/kernel.py
  --- /usr/lib/python3.1/site-packages/kigen/modules/utils/
  >>> /usr/lib/python3.1/site-packages/kigen/modules/utils/__init__.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/utils/fstab.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/utils/isstatic.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/utils/listdynamiclibs.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/utils/misc.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/utils/process.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/__init__.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/cliparser.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/credits.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/default.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/etcparser.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/nocolor.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/stdout.py
  >>> /usr/lib/python3.1/site-packages/kigen/modules/usage.py
  --- /usr/share/
  >>> /usr/share/kigen/
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
  --- /etc/kigen/
  --- /etc/kigen/initramfs/
  >>> /etc/kigen/initramfs/._cfg0000_default.conf
  >>> /etc/kigen/initramfs/modules.conf
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
  
  >>> Recording sys-kernel/kigen in "world" favorites file...
  >>> Auto-cleaning packages...
  
  >>> No outdated packages were found on your system.
  
   * GNU info directory index is up-to-date.
  
   * IMPORTANT: 1 config files in '/etc' need updating.
   * See the CONFIGURATION FILES section of the emerge
   * man page to learn how to update config files.
  z13 ~ # etc-update 

- Care for **/etc/kigen/**

Kigen has 3 sets of config files:
 - /etc/kigen/master.conf
 - /etc/kigen/kernel/default.conf
 - /etc/kigen/initramfs/{default.conf,modules.conf,version.conf}

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
  
  Parameters:
   kigen kernel                --help, -h
   kigen initramfs             --help, -h
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
  
  Misc:
    --nosaveconfig             False              Do not save kernel config in /etc/kernels
    --noboot                   False              Do not copy kernel to /boot
    --rename=/file             ""                 Custom kernel file name
    --logfile=/file            "/var/log/kigen.log" 
    --debug, -d                False              Debug verbose
  
  Handy tools:
    --getdotconfig=/vmlinux    ""                 Extract .config from compiled binary kernel (if IKCONFIG has been set)
  z13 ~ # 

Default behavior.
::
  z13 ~ # kigen k
   * Gentoo Base System release 2.0.1 on x86_64
   * Kernel sources Makefile version 2.6.37-gentoo aka Flesh-EatingBatswithFangs
   * kernel.copy_config /usr/src/linux/.config -> /usr/src/linux/.config.2011-01-08-15-55-39
   * kernel.oldconfig 
  scripts/kconfig/conf --oldconfig Kconfig
  #
  # configuration written to .config
  #
   * kernel.prepare 
   * kernel.bzImage 
   * kernel.modules 
   * kernel.modules_install //lib/modules/
   * saved /etc/kernels/dotconfig-kigen-x86_64-2.6.37-gentoo
   * produced /boot/System.map-kigen-x86_64-2.6.37-gentoo
   * produced /boot/kernel-kigen-x86_64-2.6.37-gentoo
  z13 ~ # 

It is up to you to adapt your /etc/lilo.conf or /boot/grub/grub.cfg file.

- Use of **kigen initramfs** to generate an initramfs

Help menu.
::
  z13 ~ # kigen i -h
  Parameter:                   Config value:      Description:
  
  Linuxrc:
    --linuxrc=/linuxrc[,/file] ""                 Include custom linuxrc (files copied over to etc)
  
  Busybox:
    --dotconfig=/file          ""                 Custom busybox config file
    --defconfig                False              Set .config to largest generic options
    --oldconfig                False              Ask for new busybox options if any
    --menuconfig               False              Interactive busybox options menu
  
  Features:
    --splash=<theme>           ""                 Include splash support (splashutils must be merged)
     --sres=YxZ[,YxZ]          ""                  Splash resolution, all if not set
    --disklabel                False              Include support for UUID/LABEL (host binary or sources)
    --luks                     True               Include LUKS support (host binary or sources)
    --lvm2                     False              Include LVM2 support (host binary or sources)
    --evms                     False              Include EVMS support (host binary only)
    --dmraid                   False              Include DMRAID support (host binary or sources)
    --dropbear                 False              Include dropbear tools and daemon (host binary or sources)
     --debugflag               False               Compile dropbear with #define DEBUG_TRACE in debug.h
    --rootpasswd=<passwd>      ""                 Create and set root password (required for dropbear)
    --keymaps                  False              Include all keymaps
    --ttyecho                  False              Include the handy ttyecho.c tool
    --strace                   False              Include the strace binary tool (host binary or sources)
    --screen                   False              Include the screen binary tool (host binary or sources)
    --plugin=/dir[,/dir]       ""                 Include list of user generated custom roots
  
  Libraries: (host only)
    --glibc                    False              Include host GNU C libraries (required for dns,dropbear)
    --libncurses               False              Include host libncurses (required for dropbear)
    --zlib                     False              Include host zlib (required for dropbear)
  
  Misc:
    --nocache                  False              Delete previous cached data on startup
    --hostbin                  False              Use host binaries (fall back to sources if dynamic linkage detected)
    --noboot                   False              Do not copy initramfs to /boot
    --rename=/file             ""                 Custom initramfs file name
    --logfile=/file            "/var/log/kigen.log" 
    --debug, -d                False              Debug verbose
  
  Handy tools:
    --extract=/file            ""                 Extract initramfs file
     --to=/dir                 "/var/tmp/kigen/extracted-initramfs"
                                                   Custom extracting directory
    --compress=/dir            ""                 Compress directory into initramfs
     --into=/file              "/var/tmp/kigen/compressed-initramfs/initramfs_data.cpio.gz"
                                                   Custom initramfs file
  z13 ~ # 

Default behavior.
::
  z13 ~ # kigen i
   * Gentoo Base System release 2.0.1 on x86_64
   * initramfs.append.base Gentoo linuxrc 3.4.10.907-r2
   * initramfs.append.modules 2.6.37-gentoo
   * ... dm-crypt
   * ... dm-crypt
   * ... raid0
   * ... raid1
   * ... raid456
   * ... raid10
   * ... dm-crypt
   * ... dm-crypt
   * ... raid0
   * ... raid1
   * ... raid456
   * ... raid10
   * ... pata_mpiix
   * ... pata_pdc2027x
   * ... pata_rz1000
   * ... pata_cmd64x
   * ... pata_hpt366
   * ... pata_hpt37x
   * ... pata_hpt3x3
   * ... pata_hpt3x2n
   * ... pata_optidma
   * ... pata_it821x
   * ... pata_artop
   * ... pata_oldpiix
   * ... pata_legacy
   * ... pata_it8213
   * ... pata_ali
   * ... pata_amd
   * ... pata_atiixp
   * ... pata_sis
   * ... pata_hpt3x2n
   * ... pata_marvell
   * ... pata_cs5520
   * ... pata_cs5530
   * ... sata_promise
   * ... sata_sil
   * ... sata_sil24
   * ... sata_nv
   * ... sata_sx4
   * ... sata_vsc
   * ... sata_qstor
   * ... sata_mv
   * ... sata_inic162x
   * ... pdc_adma
   * ... aic79xx
   * ... aic7xxx
   * ... aic7xxx_old
   * ... arcmsr
   * ... BusLogic
   * ... initio
   * ... gdth
   * ... sym53c8xx
   * ... imm
   * ... ips
   * ... qla1280
   * ... dc395x
   * ... atp870u
   * ... mptbase
   * ... mptscsih
   * ... mptspi
   * ... mptfc
   * ... mptsas
   * ... 3w-xxxx
   * ... 3w-9xxx
   * ... cpqarray
   * ... cciss
   * ... DAC960
   * ... sx8
   * ... aacraid
   * ... megaraid
   * ... megaraid_mbox
   * ... megaraid_mm
   * ... megaraid_sas
   * ... qla2xxx
   * ... lpfc
   * ... scsi_transport_fc
   * ... aic94xx
   * ... scsi_wait_scan
   * ... e1000
   * ... tg3
   * ... sky2
   * ... atl1c
   * ... scsi_transport_iscsi
   * ... libiscsi
   * ... iscsi_tcp
   * ... yenta_socket
   * ... pd6729
   * ... i82092
   * ... usb-storage
   * ... sl811-hcd
   * ... i915
   * ... drm
   * ... drm_kms_helper
   * ... i2c-algo-bit
   * initramfs.append.busybox 1.18.0
   * ... busybox.download
   * ... busybox.extract
   * ... busybox.copy_config 
   * ... busybox.make
   * ... busybox.strip
   * ... busybox.compress
   * ... busybox.cache
   * initramfs.compress
   * produced /boot/initramfs-kigen-x86_64-2.6.37-gentoo
  z13 ~ # 
  
A second run would use what has been cached.
Generally, what can be compiled with KIGen should be cacheable.
In this case, busybox cache is used.
::
  z13 ~ # kigen i
   * Gentoo Base System release 2.0.1 on x86_64
   * initramfs.append.base Gentoo linuxrc 3.4.10.907-r2
   * initramfs.append.modules 2.6.37-gentoo
   * ... dm-crypt
   * ... dm-crypt
   * ... raid0
   * ... raid1
   * ... raid456
   * ... raid10
   * ... dm-crypt
   * ... dm-crypt
   * ... raid0
   * ... raid1
   * ... raid456
   * ... raid10
   * ... pata_mpiix
   * ... pata_pdc2027x
   * ... pata_rz1000
   * ... pata_cmd64x
   * ... pata_hpt366
   * ... pata_hpt37x
   * ... pata_hpt3x3
   * ... pata_hpt3x2n
   * ... pata_optidma
   * ... pata_it821x
   * ... pata_artop
   * ... pata_oldpiix
   * ... pata_legacy
   * ... pata_it8213
   * ... pata_ali
   * ... pata_amd
   * ... pata_atiixp
   * ... pata_sis
   * ... pata_hpt3x2n
   * ... pata_marvell
   * ... pata_cs5520
   * ... pata_cs5530
   * ... sata_promise
   * ... sata_sil
   * ... sata_sil24
   * ... sata_nv
   * ... sata_sx4
   * ... sata_vsc
   * ... sata_qstor
   * ... sata_mv
   * ... sata_inic162x
   * ... pdc_adma
   * ... aic79xx
   * ... aic7xxx
   * ... aic7xxx_old
   * ... arcmsr
   * ... BusLogic
   * ... initio
   * ... gdth
   * ... sym53c8xx
   * ... imm
   * ... ips
   * ... qla1280
   * ... dc395x
   * ... atp870u
   * ... mptbase
   * ... mptscsih
   * ... mptspi
   * ... mptfc
   * ... mptsas
   * ... 3w-xxxx
   * ... 3w-9xxx
   * ... cpqarray
   * ... cciss
   * ... DAC960
   * ... sx8
   * ... aacraid
   * ... megaraid
   * ... megaraid_mbox
   * ... megaraid_mm
   * ... megaraid_sas
   * ... qla2xxx
   * ... lpfc
   * ... scsi_transport_fc
   * ... aic94xx
   * ... scsi_wait_scan
   * ... e1000
   * ... tg3
   * ... sky2
   * ... atl1c
   * ... scsi_transport_iscsi
   * ... libiscsi
   * ... iscsi_tcp
   * ... yenta_socket
   * ... pd6729
   * ... i82092
   * ... usb-storage
   * ... sl811-hcd
   * ... i915
   * ... drm
   * ... drm_kms_helper
   * ... i2c-algo-bit
   * initramfs.append.busybox 1.18.0
   * ... cache found: importing
   * initramfs.compress
   * produced /boot/initramfs-kigen-x86_64-2.6.37-gentoo
  z13 ~ # 

Now let's make a full blown initramfs.
::
  z13 ~ # kigen i --splash=emergence --disklabel --luks --lvm2 --keymaps --dropbear --debugflag --glibc --libncurses --zlib --rootpasswd=mypass --ttyecho --strace 
   * Gentoo Base System release 2.0.1 on x86_64
   * initramfs.append.base Gentoo linuxrc 3.4.10.907-r2
   * initramfs.append.modules 2.6.37-gentoo
   * ... dm-crypt
   * ... dm-crypt
   * ... raid0
   * ... raid1
   * ... raid456
   * ... raid10
   * ... dm-crypt
   * ... dm-crypt
   * ... raid0
   * ... raid1
   * ... raid456
   * ... raid10
   * ... pata_mpiix
   * ... pata_pdc2027x
   * ... pata_rz1000
   * ... pata_cmd64x
   * ... pata_hpt366
   * ... pata_hpt37x
   * ... pata_hpt3x3
   * ... pata_hpt3x2n
   * ... pata_optidma
   * ... pata_it821x
   * ... pata_artop
   * ... pata_oldpiix
   * ... pata_legacy
   * ... pata_it8213
   * ... pata_ali
   * ... pata_amd
   * ... pata_atiixp
   * ... pata_sis
   * ... pata_hpt3x2n
   * ... pata_marvell
   * ... pata_cs5520
   * ... pata_cs5530
   * ... sata_promise
   * ... sata_sil
   * ... sata_sil24
   * ... sata_nv
   * ... sata_sx4
   * ... sata_vsc
   * ... sata_qstor
   * ... sata_mv
   * ... sata_inic162x
   * ... pdc_adma
   * ... aic79xx
   * ... aic7xxx
   * ... aic7xxx_old
   * ... arcmsr
   * ... BusLogic
   * ... initio
   * ... gdth
   * ... sym53c8xx
   * ... imm
   * ... ips
   * ... qla1280
   * ... dc395x
   * ... atp870u
   * ... mptbase
   * ... mptscsih
   * ... mptspi
   * ... mptfc
   * ... mptsas
   * ... 3w-xxxx
   * ... 3w-9xxx
   * ... cpqarray
   * ... cciss
   * ... DAC960
   * ... sx8
   * ... aacraid
   * ... megaraid
   * ... megaraid_mbox
   * ... megaraid_mm
   * ... megaraid_sas
   * ... qla2xxx
   * ... lpfc
   * ... scsi_transport_fc
   * ... aic94xx
   * ... scsi_wait_scan
   * ... e1000
   * ... tg3
   * ... sky2
   * ... atl1c
   * ... scsi_transport_iscsi
   * ... libiscsi
   * ... iscsi_tcp
   * ... yenta_socket
   * ... pd6729
   * ... i82092
   * ... usb-storage
   * ... sl811-hcd
   * ... i915
   * ... drm
   * ... drm_kms_helper
   * ... i2c-algo-bit
   * initramfs.append.busybox 1.18.0
   * ... busybox.download
   * ... busybox.extract
   * ... busybox.copy_config 
   * ... busybox.make
   * ... busybox.strip
   * ... busybox.compress
   * ... busybox.cache
   * initramfs.append.lvm2 2.02.77
   * ... lvm2.download
   * ... lvm2.extract
   * ... lvm2.configure
   * ... lvm2.make
   * ... lvm2.install
   * ... lvm2.strip
   * ... lvm2.compress
   * ... lvm2.cache
   * initramfs.append.luks 1.1.3
   * ... luks.download
   * ... luks.extract
   * ... luks.configure
   * ... luks.make
   * ... luks.strip
   * ... luks.compress
   * ... luks.cache
   * initramfs.append.e2fsprogs 1.41.12
   * ... e2fsprogs.download
   * ... e2fsprogs.extract
   * ... e2fsprogs.configure
   * ... e2fsprogs.make
   * ... e2fsprogs.strip
   * ... e2fsprogs.compress
   * ... e2fsprogs.cache
   * initramfs.append.dropbear 0.52
   * ... dropbear.download
   * ... dropbear.extract
   * ... dropbear.patch_debug_header #define DEBUG_TRACE
   * ... dropbear.configure
   * ... dropbear.make
   * ... dropbear.strip
   * ... dropbear.dsskey
  Will output 1024 bit dss secret key to '/var/tmp/kigen/work/dropbear-0.52/etc/dropbear/dropbear_dss_host_key'
  Generating key, this may take a while...
   * ... dropbear.rsakey
  Will output 4096 bit rsa secret key to '/var/tmp/kigen/work/dropbear-0.52/etc/dropbear/dropbear_rsa_host_key'
  Generating key, this may take a while...
   * ... dropbear.compress
   * ... dropbear.cache
   * initramfs.append.strace 4.5.20
   * ... strace.download
   * ... strace.extract
   * ... strace.configure
   * ... strace.make
   * ... strace.strip
   * ... strace.compress
   * ... strace.cache
   * initramfs.append.ttyecho
   * ... gcc -static /usr/share/kigen/tools/ttyecho.c -o /var/tmp/kigen/work/initramfs-ttyecho-temp/sbin/ttyecho
   * initramfs.append.splash emergence 
   * initramfs.append.rootpasswd
   * ... /etc/passwd
   * ... /etc/group
   * initramfs.append.keymaps
   * initramfs.append.glibc
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
   * initramfs.append.libncurses
   * ... /lib/libncurses.so.5
   * initramfs.append.zlib
   * ... /lib/libz.so.1
   * initramfs.compress
   * produced /boot/initramfs-kigen-x86_64-2.6.37-gentoo
  z13 ~ # 

Re run from cache.
::
  z13 ~ # kigen i --splash=emergence --disklabel --luks --lvm2 --keymaps --dropbear --debugflag --glibc --libncurses --zlib --rootpasswd=mypass --ttyecho --strace 
   * Gentoo Base System release 2.0.1 on x86_64
   * initramfs.append.base Gentoo linuxrc 3.4.10.907-r2
   * initramfs.append.modules 2.6.37-gentoo
   * ... dm-crypt
   * ... dm-crypt
   * ... raid0
   * ... raid1
   * ... raid456
   * ... raid10
   * ... dm-crypt
   * ... dm-crypt
   * ... raid0
   * ... raid1
   * ... raid456
   * ... raid10
   * ... pata_mpiix
   * ... pata_pdc2027x
   * ... pata_rz1000
   * ... pata_cmd64x
   * ... pata_hpt366
   * ... pata_hpt37x
   * ... pata_hpt3x3
   * ... pata_hpt3x2n
   * ... pata_optidma
   * ... pata_it821x
   * ... pata_artop
   * ... pata_oldpiix
   * ... pata_legacy
   * ... pata_it8213
   * ... pata_ali
   * ... pata_amd
   * ... pata_atiixp
   * ... pata_sis
   * ... pata_hpt3x2n
   * ... pata_marvell
   * ... pata_cs5520
   * ... pata_cs5530
   * ... sata_promise
   * ... sata_sil
   * ... sata_sil24
   * ... sata_nv
   * ... sata_sx4
   * ... sata_vsc
   * ... sata_qstor
   * ... sata_mv
   * ... sata_inic162x
   * ... pdc_adma
   * ... aic79xx
   * ... aic7xxx
   * ... aic7xxx_old
   * ... arcmsr
   * ... BusLogic
   * ... initio
   * ... gdth
   * ... sym53c8xx
   * ... imm
   * ... ips
   * ... qla1280
   * ... dc395x
   * ... atp870u
   * ... mptbase
   * ... mptscsih
   * ... mptspi
   * ... mptfc
   * ... mptsas
   * ... 3w-xxxx
   * ... 3w-9xxx
   * ... cpqarray
   * ... cciss
   * ... DAC960
   * ... sx8
   * ... aacraid
   * ... megaraid
   * ... megaraid_mbox
   * ... megaraid_mm
   * ... megaraid_sas
   * ... qla2xxx
   * ... lpfc
   * ... scsi_transport_fc
   * ... aic94xx
   * ... scsi_wait_scan
   * ... e1000
   * ... tg3
   * ... sky2
   * ... atl1c
   * ... scsi_transport_iscsi
   * ... libiscsi
   * ... iscsi_tcp
   * ... yenta_socket
   * ... pd6729
   * ... i82092
   * ... usb-storage
   * ... sl811-hcd
   * ... i915
   * ... drm
   * ... drm_kms_helper
   * ... i2c-algo-bit
   * initramfs.append.busybox 1.18.0
   * ... cache found: importing
   * initramfs.append.lvm2 2.02.77
   * ... cache found: importing
   * initramfs.append.luks 1.1.3
   * ... cache found: importing
   * initramfs.append.e2fsprogs 1.41.12
   * ... cache found: importing
   * initramfs.append.dropbear 0.52
   * ... cache found: importing
   * initramfs.append.strace 4.5.20
   * ... cache found: importing
   * initramfs.append.ttyecho
   * ... gcc -static /usr/share/kigen/tools/ttyecho.c -o /var/tmp/kigen/work/initramfs-ttyecho-temp/sbin/ttyecho
   * initramfs.append.splash emergence 
   * initramfs.append.rootpasswd
   * ... /etc/passwd
   * ... /etc/group
   * initramfs.append.keymaps
   * initramfs.append.glibc
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
   * initramfs.append.libncurses
   * ... /lib/libncurses.so.5
   * initramfs.append.zlib
   * ... /lib/libz.so.1
   * initramfs.compress
   * produced /boot/initramfs-kigen-x86_64-2.6.37-gentoo
  z13 ~ # 

Now let's use binaries when possible.
::
  z13 ~ # kigen i --splash=emergence --disklabel --luks --lvm2 --keymaps --dropbear --debugflag --glibc --libncurses --zlib --rootpasswd=mypass --ttyecho --strace --hostbin
   * Gentoo Base System release 2.0.1 on x86_64
   * initramfs.append.base Gentoo linuxrc 3.4.10.907-r2
   * initramfs.append.modules 2.6.37-gentoo
   * ... dm-crypt
   * ... dm-crypt
   * ... raid0
   * ... raid1
   * ... raid456
   * ... raid10
   * ... dm-crypt
   * ... dm-crypt
   * ... raid0
   * ... raid1
   * ... raid456
   * ... raid10
   * ... pata_mpiix
   * ... pata_pdc2027x
   * ... pata_rz1000
   * ... pata_cmd64x
   * ... pata_hpt366
   * ... pata_hpt37x
   * ... pata_hpt3x3
   * ... pata_hpt3x2n
   * ... pata_optidma
   * ... pata_it821x
   * ... pata_artop
   * ... pata_oldpiix
   * ... pata_legacy
   * ... pata_it8213
   * ... pata_ali
   * ... pata_amd
   * ... pata_atiixp
   * ... pata_sis
   * ... pata_hpt3x2n
   * ... pata_marvell
   * ... pata_cs5520
   * ... pata_cs5530
   * ... sata_promise
   * ... sata_sil
   * ... sata_sil24
   * ... sata_nv
   * ... sata_sx4
   * ... sata_vsc
   * ... sata_qstor
   * ... sata_mv
   * ... sata_inic162x
   * ... pdc_adma
   * ... aic79xx
   * ... aic7xxx
   * ... aic7xxx_old
   * ... arcmsr
   * ... BusLogic
   * ... initio
   * ... gdth
   * ... sym53c8xx
   * ... imm
   * ... ips
   * ... qla1280
   * ... dc395x
   * ... atp870u
   * ... mptbase
   * ... mptscsih
   * ... mptspi
   * ... mptfc
   * ... mptsas
   * ... 3w-xxxx
   * ... 3w-9xxx
   * ... cpqarray
   * ... cciss
   * ... DAC960
   * ... sx8
   * ... aacraid
   * ... megaraid
   * ... megaraid_mbox
   * ... megaraid_mm
   * ... megaraid_sas
   * ... qla2xxx
   * ... lpfc
   * ... scsi_transport_fc
   * ... aic94xx
   * ... scsi_wait_scan
   * ... e1000
   * ... tg3
   * ... sky2
   * ... atl1c
   * ... scsi_transport_iscsi
   * ... libiscsi
   * ... iscsi_tcp
   * ... yenta_socket
   * ... pd6729
   * ... i82092
   * ... usb-storage
   * ... sl811-hcd
   * ... i915
   * ... drm
   * ... drm_kms_helper
   * ... i2c-algo-bit
   * initramfs.append.busybox 1.18.0
   * ... cache found: importing
   * initramfs.append.lvm2 /sbin/lvm.static from host
   * initramfs.append.cryptsetup /sbin/cryptsetup from host
   * initramfs.append.e2fsprogs 1.41.12
   * ... warning: /sbin/blkid is not static, compiling from sources
   * ... cache found: importing
   * initramfs.append.dropbear 0.52
   * ... warning: /usr/sbin/dropbear not found on host, compiling from sources
   * ... cache found: importing
   * initramfs.append.strace 4.5.20
   * ... warning: /usr/bin/strace not found on host, compiling from sources
   * ... cache found: importing
   * initramfs.append.ttyecho
   * ... gcc -static /usr/share/kigen/tools/ttyecho.c -o /var/tmp/kigen/work/initramfs-ttyecho-temp/sbin/ttyecho
   * initramfs.append.splash emergence 
   * initramfs.append.rootpasswd
   * ... /etc/passwd
   * ... /etc/group
   * initramfs.append.keymaps
   * initramfs.append.glibc
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
   * initramfs.append.libncurses
   * ... /lib/libncurses.so.5
   * initramfs.append.zlib
   * ... /lib/libz.so.1
   * initramfs.compress
   * produced /boot/initramfs-kigen-x86_64-2.6.37-gentoo
  z13 ~ # 

Typically this adds support for splash/luks/lvm2/dropbear to the initramfs.
Note that by default kigen will will fetch the sources and link statically.
Passing --hostbin will use host binaries when possible.

It is up to you to adapt your /etc/lilo.conf or /boot/grub/grub.cfg file.

APT (Debian/Ubuntu)
~~~~~~~~~~~~~~~~~~~

TODO?

==========================================
Howto boot LUKS/LVM through SSH (dropbear)
==========================================

Build initramfs with SSH support
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Make sure libraries are called.
::
  z13 ~ # kigen i --splash=emergence --disklabel --luks --lvm2 --dropbear --debugflag --rootpasswd=sabayon --keymaps --ttyecho --strace --glibc --libncurses --zlib --nocache
   * Gentoo Base System release 2.0.1 on x86_64
   * initramfs.append.base Gentoo linuxrc 3.4.10.907-r2
   * initramfs.append.modules 2.6.37-gentoo
   * ... dm-crypt
   * ... dm-crypt
   * ... raid0
   * ... raid1
   * ... raid456
   * ... raid10
   * ... dm-crypt
   * ... dm-crypt
   * ... raid0
   * ... raid1
   * ... raid456
   * ... raid10
   * ... pata_mpiix
   * ... pata_pdc2027x
   * ... pata_rz1000
   * ... pata_cmd64x
   * ... pata_hpt366
   * ... pata_hpt37x
   * ... pata_hpt3x3
   * ... pata_hpt3x2n
   * ... pata_optidma
   * ... pata_it821x
   * ... pata_artop
   * ... pata_oldpiix
   * ... pata_legacy
   * ... pata_it8213
   * ... pata_ali
   * ... pata_amd
   * ... pata_atiixp
   * ... pata_sis
   * ... pata_hpt3x2n
   * ... pata_marvell
   * ... pata_cs5520
   * ... pata_cs5530
   * ... sata_promise
   * ... sata_sil
   * ... sata_sil24
   * ... sata_nv
   * ... sata_sx4
   * ... sata_vsc
   * ... sata_qstor
   * ... sata_mv
   * ... sata_inic162x
   * ... pdc_adma
   * ... aic79xx
   * ... aic7xxx
   * ... aic7xxx_old
   * ... arcmsr
   * ... BusLogic
   * ... initio
   * ... gdth
   * ... sym53c8xx
   * ... imm
   * ... ips
   * ... qla1280
   * ... dc395x
   * ... atp870u
   * ... mptbase
   * ... mptscsih
   * ... mptspi
   * ... mptfc
   * ... mptsas
   * ... 3w-xxxx
   * ... 3w-9xxx
   * ... cpqarray
   * ... cciss
   * ... DAC960
   * ... sx8
   * ... aacraid
   * ... megaraid
   * ... megaraid_mbox
   * ... megaraid_mm
   * ... megaraid_sas
   * ... qla2xxx
   * ... lpfc
   * ... scsi_transport_fc
   * ... aic94xx
   * ... scsi_wait_scan
   * ... e1000
   * ... tg3
   * ... sky2
   * ... atl1c
   * ... scsi_transport_iscsi
   * ... libiscsi
   * ... iscsi_tcp
   * ... yenta_socket
   * ... pd6729
   * ... i82092
   * ... usb-storage
   * ... sl811-hcd
   * ... i915
   * ... drm
   * ... drm_kms_helper
   * ... i2c-algo-bit
   * initramfs.append.busybox 1.18.0
   * ... busybox.extract
   * ... busybox.copy_config 
   * ... busybox.make
   * ... busybox.strip
   * ... busybox.compress
   * ... busybox.cache
   * initramfs.append.lvm2 2.02.77
   * ... lvm2.extract
   * ... lvm2.configure
   * ... lvm2.make
   * ... lvm2.install
   * ... lvm2.strip
   * ... lvm2.compress
   * ... lvm2.cache
   * initramfs.append.luks 1.1.3
   * ... luks.extract
   * ... luks.configure
   * ... luks.make
   * ... luks.strip
   * ... luks.compress
   * ... luks.cache
   * initramfs.append.e2fsprogs 1.41.12
   * ... e2fsprogs.extract
   * ... e2fsprogs.configure
   * ... e2fsprogs.make
   * ... e2fsprogs.strip
   * ... e2fsprogs.compress
   * ... e2fsprogs.cache
   * initramfs.append.dropbear 0.52
   * ... dropbear.extract
   * ... dropbear.patch_debug_header #define DEBUG_TRACE
   * ... dropbear.configure
   * ... dropbear.make
   * ... dropbear.strip
   * ... dropbear.dsskey
  Will output 1024 bit dss secret key to '/var/tmp/kigen/work/dropbear-0.52/etc/dropbear/dropbear_dss_host_key'
  Generating key, this may take a while...
   * ... dropbear.rsakey
  Will output 4096 bit rsa secret key to '/var/tmp/kigen/work/dropbear-0.52/etc/dropbear/dropbear_rsa_host_key'
  Generating key, this may take a while...
   * ... dropbear.compress
   * ... dropbear.cache
   * initramfs.append.strace 4.5.20
   * ... strace.extract
   * ... strace.configure
   * ... strace.make
   * ... strace.strip
   * ... strace.compress
   * ... strace.cache
   * initramfs.append.ttyecho
   * ... gcc -static /usr/share/kigen/tools/ttyecho.c -o /var/tmp/kigen/work/initramfs-ttyecho-temp/sbin/ttyecho
   * initramfs.append.splash emergence 
   * initramfs.append.rootpasswd
   * ... /etc/passwd
   * ... /etc/group
   * initramfs.append.keymaps
   * initramfs.append.glibc
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
   * initramfs.append.libncurses
   * ... /lib/libncurses.so.5
   * initramfs.append.zlib
   * ... /lib/libz.so.1
   * initramfs.compress
   * produced /boot/initramfs-kigen-x86_64-2.6.37-gentoo
  z13 ~ # 


Set kernel command option
~~~~~~~~~~~~~~~~~~~~~~~~~

To boot in SSH mode, pass the 'dodropbear' option in the kernel command line.
Edit /boot/grub/grub.cfg to have the kernel command line look like.
::
  linux /kernel-kigen-x86_64-2.6.37-gentoo ro single init=/linuxrc splash=verbose,theme:sabayon vga=791 console=tty1 quiet resume=swap:/dev/mapper/vg_hogbarn-swap real_resume=/dev/mapper/vg_hogbarn-swap dolvm root=/dev/ram0 ramdisk=8192 real_root=/dev/mapper/vg_hogbarn-lv_root crypt_root=/dev/sda2 docrypt dokeymap keymap=be dodropbear

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
  rik@hogbarn ~ $ ssh 192.168.1.68 -l root
  root@192.168.1.68's password: 
  
  
  BusyBox v1.17.2 (2010-09-15 11:14:56 CEST) built-in shell (ash)
  Enter 'help' for a list of built-in commands.
  
  # uname -a
  Linux (none) 2.6.34-sabayon #19 SMP Thu Sep 9 10:06:15 CEST 2010 i686 GNU/Linux
  # ls /
  bin            home           lib64          root           temp
  dev            init           modules.cache  sbin           usr
  etc            lib            proc           sys            var
  # ip a
  1: lo: <LOOPBACK> mtu 16436 qdisc noop state DOWN 
      link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
  2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
      link/ether 08:00:27:54:d1:a9 brd ff:ff:ff:ff:ff:ff
      inet 192.168.1.68/24 brd 192.168.1.255 scope global eth0
  # netstat 
  Active Internet connections (w/o servers)
  Proto Recv-Q Send-Q Local Address           Foreign Address         State       
  tcp        0      0 sabayon.lan:22          gritch.lan:44967        ESTABLISHED 
  Active UNIX domain sockets (w/o servers)
  Proto RefCnt Flags       Type       State         I-Node Path
  # 
  # ls
  boot-luks-lvm.sh  boot-luks.sh
  # cat boot-luks-lvm.sh 
  #!/bin/sh
  if [ "$1" = "-h" ] || [ "$1" = "" ]
  then
      echo "$0 <root device>"
      exit
  fi
  /sbin/cryptsetup luksOpen $1 root
  vgscan
  vgchange -a y
  mkdir /newroot
  /sbin/ttyecho -n /dev/console exit
  sleep 1
  /sbin/ttyecho -n /dev/console exit
  sleep 1
  /sbin/ttyecho -n /dev/console q
  sleep 1
  exit
  # ./boot-luks-lvm.sh 
  ./boot-luks-lvm.sh <root device>
  # ./boot-luks-lvm.sh /dev/sda2
  Enter passphrase for /dev/sda2: 
  File descriptor 5 (pipe:[2521]) leaked on vgscan invocation. Parent PID 3984: /bin/sh
    Reading all physical volumes.  This may take a while...
    Found volume group "vg_sabayon" using metadata type lvm2
  File descriptor 5 (pipe:[2521]) leaked on vgchange invocation. Parent PID 3984: /bin/sh
    2 logical volume(s) in volume group "vg_sabayon" now active
  # Connection to 192.168.1.68 closed by remote host.
  Connection to 192.168.1.68 closed.
  rik@hogbarn ~ $ 

The initramfs is now booting from the content of the LUKS container remotely! Yiha
Note the autodeconnection done by the host thanks to /etc/conf.d/local.

:Authors: 
    erick 'r1k0' michau (python engine),

    Portage community (linuxrc scripts),

:Version: 0.3.0
