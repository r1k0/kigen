============
Introduction
============

.. sectnum::

.. contents:: Table of contents

Definition
~~~~~~~~~~

**kigen uses Genkernel linuxrc and provides the same boot interface as Genkernel does.**

KIGen for Linux aims at providing first an equal set of features (in Python)
as Genkernel does for Gentoo as well as a python interface to sys-boot/boot-update for Funtoo.
Genkernel being a bash script, interfacing it with boot-update is 'tricky' if not insane.

In Funtoo, sys-boot/boot-update is now responsible for managing a unified boot
configuration file known as /etc/boot.conf.
It ships all kernel/initramfs boot information and autogenerates /boot/grub/grub.conf
or /boot/grub/grub.cfg depending on your GRUB version (in Funtoo, grub-0.97 is
known as sys-boot/grub-legacy and grub-1.97 as sys-boot/grub).

KIGen provides a more visible configuration file than genkernel
in terms of kernel modules at least.
KIGen will automagically detect if you are running boot-update (we support Gentoo and
Sabayon too) then read your /etc/boot.conf and overwrite your /etc/kigen.conf
configuration in terms of kernel modules only.

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

KIGen is on purpose using simple syntax.

Features
~~~~~~~~

- LUKS (cryptsetup binary)
- LVM2 (lvm.static binary)
- UUID (blkid binary)
- splash decorator
- customizable busybox toolbox
  - system stack tools
  - network stack tools
  - alot more
- SSH daemon (dropbear)

Supported OS
~~~~~~~~~~~~

KIGen supports Portage and works on the following linux based flavors:

- Funtoo  and its boot-update interface,
- Gentoo  (no boot-update interface yet),
- Sabayon (no boot-update interface yet).
- VLOS    (no boot-update interface yet).
- ChromeOS? ;P

provided your custom /linuxrc for the initramfs of course.

Portage and Funtoo boot-update support
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

kgen works on Debian and Arch with no support for color (but who cares?).
igen could fully work too except for --splash that currently uses splashutils from Portage.
It is planned to support --splash on Debian and Arch too.
KIGen is not meant (for now) to be installed on non Portage systems but will in the future.

If you provide a custom /linuxrc file for Debian's initramfs, KIGen should in theory work its way through.

Portage systems kernel boot options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

KIGen's linuxrc is the same as Genkernel's one except a couple of lines (bug using splash and luks for silent splash)

real_root
  points to the root device (ie. /dev/sda3 or /dev/mapper/root in case of LUKS).

root
  needs to point to the ramdisk.

vga
  should be the resolution of the screen.

subdir

real_init
  passes argument to the init on boot.

init_opts

cdroot

cdroot_type

loop
  starts livecd loop.

looptype
  loop options.

domdadm
  activates support for mdadm.

dodmraid
  activates support for dmraid.

doevms
  activates support for evms.

dolvm
  activates support for LVM2.

doscsi
  activates support for iscsi.

debug
  runs debug shell if requested

scandelay

doload

nodetect

noload

lvmraid

part

ip

nfsroot

iscsi_initiatorname

iscsi_target

iscsi_tgpt

iscsi_address

iscsi_port

iscsi_username

iscsi_password

iscsi_username_in

iscsi_password_in

iscsi_debug

crypt_root
  points to the real root device (ie. /dev/sda3).

crypt_swap
  points to the swap device encrypted by LUKS.

root_key=/keyfile
  in case your root is encrypted with a key, you can use a device like a usb pen to store the key.

root_keydev=/dev
  points to the device that carries the root_key, if not set will automatically look for the device in every boot.

swap_key
  same as root_key for the swap.

swap_keydev
  same as root_keydev for swap.

real_resume

noresume

crypt_silent

real_rootflags

keymap
  setup keymap in linuxrc

unionfs

aufs

nounionfs

=====================================
Howto build and boot kernel/initramfs
=====================================

Gentoo Portage
~~~~~~~~~~~~~~

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
  pong ~ # emerge kigen -av

  These are the packages that would be merged, in order:
  
  Calculating dependencies        ... done!                          
  [ebuild  N    ] sys-kernel/kigen-9999  USE="doc" 0 kB [1]
  
  Total: 1 package (1 new), Size of downloads: 0 kB
  Portage tree and overlays:
   [0] /usr/portage
   [1] /usr/local/portage
  
  Would you like to merge these packages? [Yes/No] 
  
  >>> Verifying ebuild manifests
  
  >>> Emerging (1 of 1) sys-kernel/kigen-9999 from r1k0
   * checking ebuild checksums ;-) ...                                                                                                                                      [ ok ]
   * checking auxfile checksums ;-) ...                                                                                                                                     [ ok ]
   * checking miscfile checksums ;-) ...                                                                                                                                    [ ok ]
   * CPV:  sys-kernel/kigen-9999
   * REPO: r1k0
   * USE:  amd64 doc elibc_glibc kernel_linux multilib userland_GNU
  >>> Unpacking source...
   * GIT NEW clone -->
   *    repository:       git://github.com/r1k0/kigen.git
  Cloning into bare repository /usr/portage/distfiles/git-src/kigen...
  remote: Counting objects: 1823, done.
  remote: Compressing objects: 100% (1811/1811), done.
  remote: Total 1823 (delta 1270), reused 0 (delta 0)
  Receiving objects: 100% (1823/1823), 410.80 KiB | 298 KiB/s, done.
  Resolving deltas: 100% (1270/1270), done.
   *    at the commit:        06820483a5b859dace01f3210ec82c844b2170fd
   *    branch:           master
   *    storage directory:    "/usr/portage/distfiles/git-src/kigen"
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
   * checking 49 files for package collisions
  --- /etc/
  >>> /etc/._cfg0000_kigen.conf
  --- /usr/
  --- /usr/share/
  --- /usr/share/man/
  --- /usr/share/man/man8/
  >>> /usr/share/man/man8/kigen.8.bz2
  --- /usr/share/kigen/
  >>> /usr/share/kigen/defaults/
  >>> /usr/share/kigen/defaults/modprobe
  >>> /usr/share/kigen/defaults/initrd.scripts
  >>> /usr/share/kigen/defaults/udhcpc.scripts
  >>> /usr/share/kigen/defaults/linuxrc
  >>> /usr/share/kigen/defaults/initrd.defaults
  >>> /usr/share/kigen/defaults/keymaps.tar.gz
  >>> /usr/share/kigen/arch/
  >>> /usr/share/kigen/arch/x86_64/
  >>> /usr/share/kigen/arch/x86_64/busybox.config
  >>> /usr/share/kigen/arch/x86_64/kernel.config
  >>> /usr/share/kigen/arch/x86/
  >>> /usr/share/kigen/arch/x86/busybox.config
  >>> /usr/share/kigen/arch/x86/kernel.config
  --- /usr/share/doc/
  >>> /usr/share/doc/kigen-9999/
  >>> /usr/share/doc/kigen-9999/TODO.bz2
  >>> /usr/share/doc/kigen-9999/README.rst.bz2
  --- /usr/lib/
  --- /usr/lib/python2.6/
  --- /usr/lib/python2.6/site-packages/
  --- /usr/lib/python2.6/site-packages/kigen/
  --- /usr/lib/python2.6/site-packages/kigen/modules/
  >>> /usr/lib/python2.6/site-packages/kigen/modules/__init__.py
  >>> /usr/lib/python2.6/site-packages/kigen/modules/nocolor.py
  >>> /usr/lib/python2.6/site-packages/kigen/modules/cliparser.py
  --- /usr/lib/python2.6/site-packages/kigen/modules/initramfs/
  >>> /usr/lib/python2.6/site-packages/kigen/modules/initramfs/__init__.py
  >>> /usr/lib/python2.6/site-packages/kigen/modules/initramfs/busybox.py
  >>> /usr/lib/python2.6/site-packages/kigen/modules/initramfs/append.py
  >>> /usr/lib/python2.6/site-packages/kigen/modules/initramfs/bootupdate.py
  >>> /usr/lib/python2.6/site-packages/kigen/modules/initramfs/luks.py
  >>> /usr/lib/python2.6/site-packages/kigen/modules/initramfs/compress.py
  >>> /usr/lib/python2.6/site-packages/kigen/modules/initramfs/extract.py
  >>> /usr/lib/python2.6/site-packages/kigen/modules/initramfs/dev/
  >>> /usr/lib/python2.6/site-packages/kigen/modules/initramfs/dev/__init__.py
  >>> /usr/lib/python2.6/site-packages/kigen/modules/initramfs/dev/gnupg.py
  >>> /usr/lib/python2.6/site-packages/kigen/modules/initramfs/dev/dmraid.py
  >>> /usr/lib/python2.6/site-packages/kigen/modules/initramfs/dev/device_mapper.py
  >>> /usr/lib/python2.6/site-packages/kigen/modules/initramfs/dev/evms.py
  >>> /usr/lib/python2.6/site-packages/kigen/modules/initramfs/dev/multipath.py
  >>> /usr/lib/python2.6/site-packages/kigen/modules/initramfs/dev/fuse.py
  >>> /usr/lib/python2.6/site-packages/kigen/modules/initramfs/dev/unionfs_fuse.py
  >>> /usr/lib/python2.6/site-packages/kigen/modules/initramfs/dev/aufs.py
  >>> /usr/lib/python2.6/site-packages/kigen/modules/initramfs/dev/splash.py
  >>> /usr/lib/python2.6/site-packages/kigen/modules/initramfs/dev/iscsi.py
  >>> /usr/lib/python2.6/site-packages/kigen/modules/initramfs/initramfs.py
  >>> /usr/lib/python2.6/site-packages/kigen/modules/initramfs/dropbear.py
  >>> /usr/lib/python2.6/site-packages/kigen/modules/initramfs/e2fsprogs.py
  >>> /usr/lib/python2.6/site-packages/kigen/modules/initramfs/lvm2.py
  --- /usr/lib/python2.6/site-packages/kigen/modules/utils/
  >>> /usr/lib/python2.6/site-packages/kigen/modules/utils/__init__.py
  >>> /usr/lib/python2.6/site-packages/kigen/modules/utils/misc.py
  >>> /usr/lib/python2.6/site-packages/kigen/modules/utils/shell.py
  >>> /usr/lib/python2.6/site-packages/kigen/modules/config.py
  >>> /usr/lib/python2.6/site-packages/kigen/modules/stdout.py
  >>> /usr/lib/python2.6/site-packages/kigen/modules/credits.py
  --- /usr/lib/python2.6/site-packages/kigen/modules/kernel/
  >>> /usr/lib/python2.6/site-packages/kigen/modules/kernel/kernel.py
  >>> /usr/lib/python2.6/site-packages/kigen/modules/kernel/__init__.py
  >>> /usr/lib/python2.6/site-packages/kigen/modules/kernel/extract.py
  --- /usr/sbin/
  >>> /usr/sbin/kigen
   * 
   * This is still experimental software, be cautious.
   * 
  
  >>> Recording sys-kernel/kigen in "world" favorites file...
  
   * Messages for package sys-kernel/kigen-9999:
  
   * GIT NEW clone -->
   *    repository:       git://github.com/r1k0/kigen.git
   *    at the commit:        06820483a5b859dace01f3210ec82c844b2170fd
   *    branch:           master
   *    storage directory:    "/usr/portage/distfiles/git-src/kigen"
   * 
   * This is still experimental software, be cautious.
   * 
  >>> Auto-cleaning packages...
  
  >>> No outdated packages were found on your system.
  
   * GNU info directory index is up-to-date.
   pong ~ #

- Care for **/etc/kigen.conf**

Customize what you feel necessary or just leave the default.
You might want to tweak the modules to fit your needs.
::
  # kernel sources path
  kernel-sources          = /usr/src/linux
  
  # initramfs programs' versions
  busybox-version         = 1.17.1
  luks-version            = 1.1.3
  e2fsprogs-version       = 1.41.12
  lvm2-version            = 2.02.73
  dropbear-version        = 0.52
  
  # busybox shipping programs
  # remember you have a busybox
  # config file that has to support it
  # leave the variable empty if the linuxrc handles
  # 'busybox --install -s' at boot
  # symlinks will be automagically created
  busybox-progs           = [ ash sh mount uname echo cut cat telnet udhcpc vi sed cmp patch awk httpd telnetd setsid nohup
  
  # initramfs modules configuration
  # put your module in the appropriate group variable
  MODULES_ATARAID         = ataraid pdcraid hptraid
  MODULES_DMRAID          = dm-mod dm-mirror dm-crypt
  MODULES_EVMS            = dm-mod dm-snapshot dm-mirror dm-crypt dm-bbr raid0 raid1 raid456 raid5 raid6 raid10
  MODULES_LVM             = dm-mod dm-snapshot dm-mirror dm-crypt dm-bbr
  MODULES_MDADM           = dm-mod dm-snapshot dm-mirror dm-crypt dm-bbr raid0 raid1 raid456 raid5 raid6 raid10
  MODULES_PATA            = pata_mpiix pata_pdc2027x pata_radisys pata_sil680 pata_rz1000 pata_efar pata_cmd64x pata_hpt366 pata_hpt37x pata_hpt3x3 pata_hpt3x2n pata_optidma pata_it821x pata_artop pata_oldpiix pata_cypress pata_platform pata_serverworks pata_legacy pata_ns87410 pata_ns87415 pata_pcmcia pata_isapnp pata_it8213 pata_ali pata_amd pata_opti pata_atiixp pata_triflex pata_pdc202xx_old pata_sc1200 pata_qdi pata_netcell pata_sis pata_hpt3x2n pata_marvell pata_jmicron pata_via pata_cs5520 pata_cs5530 pata_cs5535 pata_sl82c105 libata
  MODULES_SATA            = sata_promise sata_sil sata_sil24 sata_svw sata_via sata_nv sata_sx4 sata_sis sata_uli sata_vsc sata_qstor ahci libata ata_piix sata_mv sata_inic162x pdc_adma
  MODULES_SCSI            = sd_mod sg sr_mod aic79xx aic7xxx aic7xxx_old arcmsr BusLogic ncr53c8xx NCR53c406a initio advansys aha1740 aha1542 aha152x dtc fdomain gdth pas16 pci2220i pci2000 psi240i qlogicfas qlogicfc qlogicisp qlogicpti seagate t128 u14-34f ultrastor wd7000 NCR53c406a sym53c8xx dmx3191d imm in2000 ips qla1280 sim710 sym53c416 dc395x atp870u mptbase mptscsih mptspi mptfc mptsas 3w-xxxx 3w-9xxx cpqarray cciss DAC960 sx8 aacraid megaraid megaraid_mbox megaraid_mm megaraid_sas qla2xxx lpfc scsi_transport_fc aic94xx
  MODULES_WAITSCAN        = scsi_wait_scan
  MODULES_NET             = e1000 tg3 sky2 # atl1c
  MODULES_ISCSI           = scsi_transport_iscsi libiscsi iscsi_tcp
  MODULES_FIREWIRE        = ieee1394 ohci1394 sbp2
  MODULES_PCMCIA          = pcmcia pcmcia_core yenta_socket pd6729 i82092 i82365 tcic ds ide-cs firmware_class
  MODULES_USB             = ehci-hcd uhci usb-ohci hid usb-storage uhci-hcd ohci-hcd usbhid sl811-hcd
  MODULES_FS              = ext2 ext3 reiserfs jfs nfs xfs fuse
  
  # compilation options
  # (usually leave as is on x86)
  UTILS_MAKE              = make
  UTILS_CC                = gcc
  UTILS_AS                = as
  UTILS_LD                = ld
  DEFAULT_MAKEOPTS        = -j2
  DEFAULT_KERNEL_MAKE     = make
  DEFAULT_UTILS_MAKE      = make
  DEFAULT_KERNEL_CC       = gcc
  DEFAULT_KERNEL_AS       = as
  DEFAULT_KERNEL_LD       = ld
  DEFAULT_UTILS_CC        = gcc
  DEFAULT_UTILS_AS        = as
  DEFAULT_UTILS_LD        = ld
  
  #========================
  # BELOW NOT YET SUPPORTED
  #KERNEL_MAKE_DIRECTIVE  = bzImage
  #KERNEL_MAKE_DIRECTIVE_2=
  #KERNEL_BINARY          = arch/x86_64/boot/bzImage
  #COMPRESS_INITRD        = yes
  #========================

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
  pong ~ # kigen --help kernel
  Parameter:           Default value:     Description:
  
    --config=/file             "/etc/kigen.conf"      Custom master config file
    --dotconfig=/file          "/usr/src/linux/.config"   Custom kernel .config file
    --rename=/file             "/boot/kernel-kigen-x86_64-2.6.35-sabayon"
                              Custom kernel file name
    --initramfs=/file          ""             Embed initramfs into the kernel
     --fixdotconfig            False           Check and auto fix the kernel config file (experimental)
    --clean                    False          Clean precompiled objects only
    --mrproper                 False          Clean precompiled objects and remove config file
    --oldconfig                True           Ask for new kernel options if any
    --menuconfig               False          Interactive kernel options menu
    --fakeroot=/dir            "/"            Append modules to /dir/lib/modules
    --nooldconfig              False          Do not ask for new kernel/initramfs options
    --nomodinstall             False          Do not install modules
    --nosaveconfig             False          Do not save kernel config in /etc/kernels
    --noboot                   False          Do not copy kernel to /boot
    --logfile=/file            "/var/log/kigen.log"   Log to file
    --debug, -d                False          Debug verbose
  
    --getdotconfig=/vmlinux    ""             Extract .config from compiled binary kernel (if IKCONFIG has been set)
  pong ~ # 

Default behavior.
::
  pong ~ # kigen kernel
   * Sabayon Linux amd64 G on x86_64
   * kernel.oldconfig 2.6.35-sabayon
  scripts/kconfig/conf -o arch/x86/Kconfig
  #
  # configuration written to .config
  #
   * kernel.prepare 2.6.35-sabayon
   * kernel.bzImage 2.6.35-sabayon
   * kernel.modules 2.6.35-sabayon
   * kernel.modules_install //lib/modules/2.6.35-sabayon
   * saved /etc/kernels/dotconfig-kigen-x86_64-2.6.35-sabayon
   * produced /boot/System.map-kigen-x86_64-2.6.35-sabayon
   * produced /boot/kernel-kigen-x86_64-2.6.35-sabayon
  pong ~ # 

It is up to you to adapt your /etc/lilo.conf or /boot/grub/grub.cfg file.

- Use of **kigen initramfs** to generate an initramfs

Help menu.
::
  pong ~ # kigen --help initramfs
  Parameter:           Default value:      Description:
  
    --config=/file             "/etc/kigen.conf" Custom master config file
    --dotconfig=/file          "/var/tmp/kigen/work/busybox-1.17.1/.config"
                                                Custom busybox config file
    --rename=/file             "/boot/initramfs-kigen-x86_64-2.6.35-sabayon"
                                                Custom initramfs file name
    --defconfig                False           Set .config to largest generic options
    --oldconfig                False           Ask for new busybox options if any
    --menuconfig               False           Interactive busybox options menu
    --linuxrc=/linuxrc[,/file] ""              Include custom linuxrc (files copied over to etc)
    --splash=<theme>           ""              Include splash support (splashutils must be merged)
     --sres=YxZ[,YxZ]          ""               Splash resolution, all if not set
    --disklabel                False           Include support for UUID/LABEL
    --luks                     False           Include LUKS support (host binary if found)
    --lvm2                     False           Include LVM2 support (host binary if found)
    --dropbear                 False           Include dropbear tools and daemon (host binaries if found)
     --glibc                   False            Include host GNU C libraries (required for dns,dropbear)
     --libncurses              False            Include host libncurses (required for dropbear)
     --zlib                    False            Include host zlib (required for dropbear)
     --rootpasswd=<passwd>     ""               Create and set root password (required for dropbear)
    --ttyecho                  False           Include the handy ttyecho.c tool
    --plugin=/dir[,/dir]       ""              Include list of user generated custom roots
    --nocache                  False           Do not use cached data
    --nohostbin                False           Do not use host binaries but compile from sources
    --noboot                   False           Do not copy initramfs to /boot
    --logfile=/file            "/var/log/kigen.log"    Log to file
    --debug, -d                False           Debug verbose
  
    --extract=/file            ""              Extract initramfs file
     --to=/dir                 "/var/tmp/kigen/extracted-initramfs"
                                                Custom extracting directory
    --compress=/dir            ""              Compress directory into initramfs
     --into=/file              "/var/tmp/kigen/compressed-initramfs/initramfs_data.cpio.gz"
                                                Custom initramfs file
  pong ~ #

Default behavior.
::
  pong ~ # kigen initramfs
   * Sabayon Linux amd64 G on x86_64
   * initramfs.append.base Gentoo linuxrc 3.4.10.907-r2
   * initramfs.append.modules 2.6.35-sabayon
   * ... pata_legacy
   * ... pata_pcmcia
   * ... fdomain
   * ... imm
   * ... sx8
   * ... scsi_wait_scan
   * ... e1000
   * ... tg3
   * ... sky2
   * ... pcmcia
   * ... yenta_socket
   * ... pd6729
   * ... i82092
   * ... ehci-hcd
   * ... uhci-hcd
   * ... ohci-hcd
   * ... sl811-hcd
   * initramfs.append.busybox 1.17.1 [ ash sh mount uname echo cut cat telnet udhcpc vi sed cmp patch awk httpd telnetd setsid nohup
   * ... busybox.extract
   * ... busybox.copy_config
   * ... busybox.make
   * ... busybox.strip
   * ... busybox.compress
   * ... busybox.cache
   * initramfs.compress
   * produced /boot/initramfs-kigen-x86_64-2.6.35-sabayon
  pong ~ # 

A second run would use what has been cached.
Generally, what can be compiled with KIGen should be cacheable.
In this case, busybox cache is used.
::
  pong ~ # kigen initramfs
   * Sabayon Linux amd64 G on x86_64
   * initramfs.append.base Gentoo linuxrc 3.4.10.907-r2
   * initramfs.append.modules 2.6.35-sabayon
   * ... pata_legacy
   * ... pata_pcmcia
   * ... fdomain
   * ... imm
   * ... sx8
   * ... scsi_wait_scan
   * ... e1000
   * ... tg3
   * ... sky2
   * ... pcmcia
   * ... yenta_socket
   * ... pd6729
   * ... i82092
   * ... ehci-hcd
   * ... uhci-hcd
   * ... ohci-hcd
   * ... sl811-hcd
   * initramfs.append.busybox 1.17.1 from cache
   * initramfs.compress
   * produced /boot/initramfs-kigen-x86_64-2.6.35-sabayon
  pong ~ # 

Now let's make a full blown initramfs using host binaries (which is default).
::
  pong ~ # kigen initramfs --defconfig --splash=sabayon --disklabel --luks --lvm2 --dropbear --glibc --libncurses --zlib --rootpasswd=mypass --ttyecho
   * Sabayon Linux amd64 G on x86_64
   * initramfs.append.base Gentoo linuxrc 3.4.10.907-r2
   * initramfs.append.modules 2.6.35-sabayon
   * ... pata_legacy
   * ... pata_pcmcia
   * ... fdomain
   * ... imm
   * ... sx8
   * ... scsi_wait_scan
   * ... e1000
   * ... tg3
   * ... sky2
   * ... pcmcia
   * ... yenta_socket
   * ... pd6729
   * ... i82092
   * ... ehci-hcd
   * ... uhci-hcd
   * ... ohci-hcd
   * ... sl811-hcd
   * initramfs.append.busybox 1.17.1 [ ash sh mount uname echo cut cat telnet udhcpc vi sed cmp patch awk httpd telnetd setsid nohup
   * ... busybox.extract
   * ... busybox.copy_config
   * ... busybox.defconfig
   * ... busybox.make
   * ... busybox.strip
   * ... busybox.compress
   * ... busybox.cache
   * initramfs.append.lvm2 /sbin/lvm.static from host
   * initramfs.append.luks 1.1.1 /sbin/cryptsetup from host
   * initramfs.append.e2fsprogs /sbin/blkid from host
   * initramfs.append.dropbear /usr/bin/dbscp /usr/bin/dbclient /usr/bin/dropbearkey /usr/bin/dropbearconvert /usr/sbin/dropbear from host
   * initramfs.append.splash sabayon 
   * initramfs.append.glibc
   * ... /lib/libnss_files.so.2
   * ... /lib/libnss_dns.so.2
   * ... /lib/libnss_nis.so.2
   * ... /lib/libnsl.so.1
   * ... /lib/libresolv.so.2
   * ... /lib/ld-linux.so.2
   * ... /lib/libc.so.6
   * ... /lib/libnss_compat.so.2
   * ... /lib/libutil.so.1
   * ... /etc/ld.so.cache
   * ... /lib/libcrypt.so.1
   * initramfs.append.libncurses
   * ... /lib/libncurses.so.5
   * initramfs.append.zlib
   * ... /lib/libz.so.1
   * initramfs.append.rootpasswd
   * ... /etc/passwd
   * ... /etc/group
   * initramfs.append.ttyecho
   * ... gcc /usr/share/kigen/tools/ttyecho.c -o /var/tmp/kigen/work/initramfs-ttyecho-temp/sbin/ttyecho
   * initramfs.compress
   * produced /boot/initramfs-kigen-x86_64-2.6.35-sabayon
  pong ~ # 

Let's compile from sources.
::
  pong ~ # kigen initramfs --defconfig --splash=sabayon --disklabel --luks --lvm2 --dropbear --glibc --libncurses --zlib --rootpasswd=mypass --ttyecho --nohostbin
   * Sabayon Linux amd64 G on x86_64
   * initramfs.append.base Gentoo linuxrc 3.4.10.907-r2
   * initramfs.append.modules 2.6.35-sabayon
   * ... pata_legacy
   * ... pata_pcmcia
   * ... fdomain
   * ... imm
   * ... sx8
   * ... scsi_wait_scan
   * ... e1000
   * ... tg3
   * ... sky2
   * ... pcmcia
   * ... yenta_socket
   * ... pd6729
   * ... i82092
   * ... ehci-hcd
   * ... uhci-hcd
   * ... ohci-hcd
   * ... sl811-hcd
   * initramfs.append.busybox 1.17.1 [ ash sh mount uname echo cut cat telnet udhcpc vi sed cmp patch awk httpd telnetd setsid nohup
   * ... busybox.download
   * ... busybox.extract
   * ... busybox.copy_config
   * ... busybox.defconfig
   * ... busybox.make
   * ... busybox.strip
   * ... busybox.compress
   * ... busybox.cache
   * initramfs.append.lvm2 2.02.73
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
   * initramfs.append.splash sabayon 
   * initramfs.append.glibc
   * ... /lib/libnss_files.so.2
   * ... /lib/libnss_dns.so.2
   * ... /lib/libnss_nis.so.2
   * ... /lib/libnsl.so.1
   * ... /lib/libresolv.so.2
   * ... /lib/ld-linux.so.2
   * ... /lib/libc.so.6
   * ... /lib/libnss_compat.so.2
   * ... /lib/libutil.so.1
   * ... /etc/ld.so.cache
   * ... /lib/libcrypt.so.1
   * initramfs.append.libncurses
   * ... /lib/libncurses.so.5
   * initramfs.append.zlib
   * ... /lib/libz.so.1
   * initramfs.append.rootpasswd
   * ... /etc/passwd
   * ... /etc/group
   * initramfs.append.ttyecho
   * ... gcc /usr/share/kigen/tools/ttyecho.c -o /var/tmp/kigen/work/initramfs-ttyecho-temp/sbin/ttyecho
   * initramfs.compress
   * produced /boot/initramfs-kigen-x86_64-2.6.35-sabayon
  pong ~ # 

Re run from cache.
::
  pong ~ # kigen initramfs --defconfig --splash=sabayon --disklabel --luks --lvm2 --dropbear --glibc --libncurses --zlib --rootpasswd=mypass --ttyecho --nohostbin
   * Sabayon Linux amd64 G on x86_64
   * initramfs.append.base Gentoo linuxrc 3.4.10.907-r2
   * initramfs.append.modules 2.6.35-sabayon
   * ... pata_legacy
   * ... pata_pcmcia
   * ... fdomain
   * ... imm
   * ... sx8
   * ... scsi_wait_scan
   * ... e1000
   * ... tg3
   * ... sky2
   * ... pcmcia
   * ... yenta_socket
   * ... pd6729
   * ... i82092
   * ... ehci-hcd
   * ... uhci-hcd
   * ... ohci-hcd
   * ... sl811-hcd
   * initramfs.append.busybox 1.17.1 from cache
   * initramfs.append.lvm2 2.02.73 from cache
   * initramfs.append.luks 1.1.3 from cache
   * initramfs.append.e2fsprogs 1.41.12 from cache
   * initramfs.append.dropbear 0.52 from cache
   * initramfs.append.splash sabayon 
   * initramfs.append.glibc
   * ... /lib/libnss_files.so.2
   * ... /lib/libnss_dns.so.2
   * ... /lib/libnss_nis.so.2
   * ... /lib/libnsl.so.1
   * ... /lib/libresolv.so.2
   * ... /lib/ld-linux.so.2
   * ... /lib/libc.so.6
   * ... /lib/libnss_compat.so.2
   * ... /lib/libutil.so.1
   * ... /etc/ld.so.cache
   * ... /lib/libcrypt.so.1
   * initramfs.append.libncurses
   * ... /lib/libncurses.so.5
   * initramfs.append.zlib
   * ... /lib/libz.so.1
   * initramfs.append.rootpasswd
   * ... /etc/passwd
   * ... /etc/group
   * initramfs.append.ttyecho
   * ... gcc /usr/share/kigen/tools/ttyecho.c -o /var/tmp/kigen/work/initramfs-ttyecho-temp/sbin/ttyecho
   * initramfs.compress
   * produced /boot/initramfs-kigen-x86_64-2.6.35-sabayon
  pong ~ # 


Typically this adds support for splash/luks/lvm2/dropbear to the initramfs.
Note that by default kigen will pick up and ship host binaries.
Passing --nohostbin will fetch sources and compile statically.

It is up to you to adapt your /etc/lilo.conf or /boot/grub/grub.cfg file.

:Authors: 
    erick 'r1k0' michau (python engine),

    Portage community (linuxrc scripts),

:Version: 0.1.5
