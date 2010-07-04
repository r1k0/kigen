=====================================
HOWTO build and boot kernel/initramfs
=====================================

.. sectnum::

.. contents:: Table of contents

Gentoo Portage based (Gentoo, Sabayon, VLOS)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Add to local overlay

Download an ebuild of your choice at http://www.github.com/r1k0/kigen/downloads.
If you're not familiar with creating your own overlay, refer to http://www.gentoo.org/proj/en/overlays/userguide.xml.
::
  pong ~ # mkdir -p /usr/local/portage/sys-kernel/kigen/
  pong ~ # cd /usr/local/portage/sys-kernel/kigen/
  pong ~ # wget http://github.com/downloads/r1k0/kigen/kigen-9999.ebuild
  pong ~ # ebuild kigen-9999.ebuild digest

- Merge KIGen

emerge it.
::
  pong ~ # emerge kigen
  Calculating dependencies        ... done!      
  
  >>> Verifying ebuild manifests
  
  >>> Emerging (1 of 1) sys-kernel/kigen-9999 from r1k0
   * checking ebuild checksums ;-) ...                                                                                  [ ok ]
   * checking auxfile checksums ;-) ...                                                                                 [ ok ]
   * checking miscfile checksums ;-) ...                                                                                [ ok ]
   * CPV:  sys-kernel/kigen-9999
   * REPO: r1k0
   * USE:  amd64 doc elibc_glibc kernel_linux multilib userland_GNU
  >>> Unpacking source...
   * GIT NEW clone -->
   *    repository:       git://github.com/r1k0/kigen.git
  Initialized empty Git repository in /usr/portage/distfiles/git-src/kigen/
  remote: Counting objects: 731, done.
  remote: Compressing objects: 100% (725/725), done.
  remote: Total 731 (delta 478), reused 0 (delta 0)
  Receiving objects: 100% (731/731), 232.00 KiB | 293 KiB/s, done.
  Resolving deltas: 100% (478/478), done.
   *    at the commit:        75ef987008c5dcbfe1d916a8aa6c258db2052f85
   *    branch:           master
   *    storage directory:    "/usr/portage/distfiles/git-src/kigen"
  Initialized empty Git repository in /var/tmp/portage/sys-kernel/kigen-9999/work/kigen-9999/.git/
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
  
  >>> Installing (1 of 1) sys-kernel/kigen-9999
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
  busybox-version         = 1.16.0
  luks-version            = 1.1.2
  e2fsprogs-version       = 1.40.9
  lvm2-version            = 2.02.65
  
  # busybox shipping programs
  # remember you have a busybox
  # config file that supports it
  busybox-progs           = [ ash sh mount uname echo cut cat telnet udhcpc vi sed cmp patch awk httpd
  
  # compilation options
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
  MODULES_NET             = e1000 tg3 atl1c
  MODULES_ISCSI           = scsi_transport_iscsi libiscsi iscsi_tcp
  MODULES_FIREWIRE        = ieee1394 ohci1394 sbp2
  MODULES_PCMCIA          = pcmcia pcmcia_core yenta_socket pd6729 i82092 i82365 tcic ds ide-cs firmware_class
  MODULES_USB             = ehci-hcd uhci usb-ohci hid usb-storage uhci-hcd ohci-hcd usbhid sl811-hcd
  MODULES_FS              = ext2 ext3 reiserfs jfs nfs xfs fuse
  
  #========================
  # BELOW NOT YET SUPPORTED
  #KERNEL_MAKE_DIRECTIVE  = bzImage
  #KERNEL_MAKE_DIRECTIVE_2=
  #KERNEL_BINARY          = arch/x86_64/boot/bzImage
  #COMPRESS_INITRD        = yes
  #========================

 

- Use of **kgen** to generate a kernel/system.map

Help menu.
::
  pong ~ # kgen -h
  
    a GNU/Linux kernel generator
  
  Usage:
        kgen <options>
  
  Options:
    --conf=/file           Custom master config file
    -h, --help             This
    -n, --nocolor          Do not colorize output
    -d, --debug            Show more output
    --logfile=/file        Log to file, default to /var/log/kgen.log
    --version              Version
    --credits              Credits and license
  
    --dotconfig=/file      Custom kernel config file (full path)
    --kernname=mykernel    Custom kernel file name
    --nooldconfig          Will not ask for new kernel/initramfs options
    --mrproper             Clean precompiled objects and remove config file
    --clean                Clean precompiled objects only
    --oldconfig            Will ask for new kernel/initramfs options
    --menuconfig           Interactive kernel options menu
    --nomodinstall         Do not install modules
    --nosaveconfig         Do not save kernel config in /etc/kernels
    --fakeroot=/dir        Append modules to /dir/lib/modules
    --noboot               Do not copy kernel to /boot
  pong ~ #

Default behavior.
::
  pong ~ # kgen
   * kernel.oldconfig 2.6.34-gentoo-r1
  scripts/kconfig/conf -o arch/x86/Kconfig
  #
  # configuration written to .config
  #
   * kernel.prepare 2.6.34-gentoo-r1
   * kernel.bzImage 2.6.34-gentoo-r1
   * kernel.modules 2.6.34-gentoo-r1
   * kernel.modules_install /lib/modules/2.6.34-gentoo-r1
   * saved /etc/kernels/dotconfig-kigen-x86_64-2.6.34-gentoo-r1
   * produced /boot/kernel-kigen-x86_64-2.6.34-gentoo-r1
   * produced /boot/System.map-kigen-x86_64-2.6.34-gentoo-r1
  pong ~ # 

It is up to you to adapt your /etc/lilo.conf or /boot/grub/grub.cfg file.

- Use of **igen** to generate an initramfs

Help menu.
::
  pong ~ # igen -h
  
    a GNU/Linux initramfs generator
  
  Usage:
        igen <options>
  
  Options:
    --conf=/file           Custom master config file
    -h, --help             This
    -n, --nocolor          Do not colorize output
    -d, --debug            Show more output
    --logfile=/file        Log to file, default to /var/log/igen.log
    --version              Version
    --credits              Credits and license
  
    --dotconfig=/file      Custom busybox config file (full path)
    --menuconfig           Interactive initramfs options menu
    --linuxrc=/file        Custom linuxrc /init for the initramfs
    --disklabel            Include support for disklabel and UUID
    --luks                 Include LUKS support (host binary if found)
    --lvm2                 Include LVM2 support (host binary if found)
    --splash               Include splash support (media-gfx/splashutils if found)
     --stheme=<theme>       Splash theme, gentoo by default
     --sres=INTxINT         Splash resolution,comma separated list of INTxINT, all if not set
     --sinitrd=/file        Splash custom initrd.splash (host if found)
    --nocache              Do not use cached data
    --nohostbin            Do not use host binaries but compile from sources
    --noboot               Do not copy initramfs to /boot
  pong ~ #

Default behavior.
::
  pong ~ # igen --luks --lvm2 --splash --stheme=gentoo
   * initramfs.append.base
   * initramfs.append.busybox 1.16.0 [ ash sh mount uname echo cut cat telnet udhcpc vi sed cmp patch awk httpd
   * ... busybox.download
   * ... busybox.extract
   * ... busybox.copy_config
   * ... busybox.compile
   * ... busybox.strip
   * ... busybox.compress
   * ... busybox.cache
   * initramfs.append.modules 2.6.34-gentoo-r1
   * ... pata_legacy
   * ... pata_pcmcia
   * ... fdomain
   * ... imm
   * ... sx8
   * ... scsi_wait_scan
   * ... e1000
   * ... tg3
   * ... atl1c
   * ... pcmcia
   * ... yenta_socket
   * ... pd6729
   * ... i82092
   * ... ehci-hcd
   * ... uhci-hcd
   * ... ohci-hcd
   * ... sl811-hcd
   * initramfs.append.lvm2 /sbin/lvm.static from host
   * initramfs.append.luks 1.1.2 /sbin/cryptsetup from host
   * initramfs.append.splash gentoo 
   * initramfs.compress
   * produced /boot/initramfs-kigen-x86_64-2.6.34-gentoo-r1
  pong ~ # 

A second run would use what has been cached.
In this case, busybox cache is used.
::
  pong ~ # igen --luks --lvm2 --splash --stheme=gentoo
   * initramfs.append.base
   * initramfs.append.busybox 1.16.0 from cache
   * initramfs.append.modules 2.6.34-gentoo-r1
   * ... pata_legacy
   * ... pata_pcmcia
   * ... fdomain
   * ... imm
   * ... sx8
   * ... scsi_wait_scan
   * ... e1000
   * ... tg3
   * ... atl1c
   * ... pcmcia
   * ... yenta_socket
   * ... pd6729
   * ... i82092
   * ... ehci-hcd
   * ... uhci-hcd
   * ... ohci-hcd
   * ... sl811-hcd
   * initramfs.append.lvm2 /sbin/lvm.static from host
   * initramfs.append.luks 1.1.2 /sbin/cryptsetup from host
   * initramfs.append.splash gentoo 
   * initramfs.compress
   * produced /boot/initramfs-kigen-x86_64-2.6.34-gentoo-r1
  pong ~ # 

Now let's make a 3rd run without any host binaries and remove previous cached data.
::
  pong ~ # igen --luks --lvm2 --splash --stheme=gentoo --nohostbin --nocache
   * initramfs.append.base
   * initramfs.append.busybox 1.16.0 [ ash sh mount uname echo cut cat telnet udhcpc vi sed cmp patch awk httpd
   * ... busybox.download
   * ... busybox.extract
   * ... busybox.copy_config
   * ... busybox.compile
   * ... busybox.strip
   * ... busybox.compress
   * ... busybox.cache
   * initramfs.append.modules 2.6.34-gentoo-r1
   * ... pata_legacy
   * ... pata_pcmcia
   * ... fdomain
   * ... imm
   * ... sx8
   * ... scsi_wait_scan
   * ... e1000
   * ... tg3
   * ... atl1c
   * ... pcmcia
   * ... yenta_socket
   * ... pd6729
   * ... i82092
   * ... ehci-hcd
   * ... uhci-hcd
   * ... ohci-hcd
   * ... sl811-hcd
   * initramfs.append.lvm2 2.02.67
   * ... lvm2.download
   * ... lvm2.extract
   * ... lvm2.configure
   * ... lvm2.compile
   * ... lvm2.install
   * ... lvm2.strip
   * ... lvm2.compress
   * ... lvm2.cache
   * initramfs.append.luks 1.1.2
   * ... luks.download
   * ... luks.extract
   * ... luks.configure
   * ... luks.compile
   * ... luks.strip
   * ... luks.compress
   * ... luks.cache
   * initramfs.append.splash gentoo 
   * initramfs.compress
   * produced /boot/initramfs-kigen-x86_64-2.6.34-gentoo-r1
  pong ~ # 

Now let's use the cache.
::
  pong ~ # igen --luks --lvm2 --splash --stheme=gentoo --nohostbin
   * initramfs.append.base
   * initramfs.append.busybox 1.16.0 from cache
   * initramfs.append.modules 2.6.34-gentoo-r1
   * ... pata_legacy
   * ... pata_pcmcia
   * ... fdomain
   * ... imm
   * ... sx8
   * ... scsi_wait_scan
   * ... e1000
   * ... tg3
   * ... atl1c
   * ... pcmcia
   * ... yenta_socket
   * ... pd6729
   * ... i82092
   * ... ehci-hcd
   * ... uhci-hcd
   * ... ohci-hcd
   * ... sl811-hcd
   * initramfs.append.lvm2 2.02.67 from cache
   * initramfs.append.luks 1.1.2 from cache
   * initramfs.append.splash gentoo 
   * initramfs.compress
   * produced /boot/initramfs-kigen-x86_64-2.6.34-gentoo-r1
  pong ~ # 


Typically this adds support for splash luks and lvm2 to the initramfs.
Note that by default igen will pick up and ship host binaries.
Passing --nohostbin will fetch sources and compile statically.

It is up to you to adapt your /etc/lilo.conf or /boot/grub/grub.cfg file.

Funtoo Portage based
~~~~~~~~~~~~~~~~~~~~

- Add to local overlay

- Merge KIGen

- Care for /etc/kigen.conf

- Use of kgen to generate a kernel/system.map

- Use of igen to generate an initramfs

- Use of igen to generate an initramfs with support for sys-boot/boot-update



:Authors: 
    erick 'r1k0' michau (python engine),

    Portage community (linuxrc scripts),

:Version: 0.1.5
