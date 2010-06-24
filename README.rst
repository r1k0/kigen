==================================
KIGen kernel/initramfs generator
==================================

.. sectnum::

.. contents:: Table of contents

Introduction
~~~~~~~~~~~~

KIGen for Linux aims at providing first an equal set of features (in Python)
as Genkernel does for Gentoo as well as a python interface to sys-boot/boot-update.
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

========
Support
========

Features
~~~~~~~~

  - LUKS (cryptsetup binary)
  - LVM2 (lvm.static binary)
  - UUID (blkid binary)
  - splash decorator
  - customizable busybox toolbox
    - telnet
    - vi
    - httpd
    - awk
    - a lot more

Supported OS
~~~~~~~~~~~~

KIGen supports Portage and provides support for the following linux based flavors:

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
  points to the root device (ie. /dev/sda3 or /dev/mapper/root in case of LUKS)

root

subdir

real_init
  passes argument to the init on boot.

init_opts

cdroot

cdroot_type

loop

looptype

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

unionfs

aufs

nounionfs

=====================================
HOWTO build and boot kernel/initramfs
=====================================

Gentoo
~~~~~~

- Add to local overlay

Download an ebuild of your choice at www.github.com/r1k0/kigen/downloads.
If you're not familiar with creating your own overlay, refer to www.gentoo.org/proj/en/overlays/userguide.xml.
::
  mkdir -p /usr/local/portage/sys-kernel/kigen/
  cd /usr/local/portage/sys-kernel/kigen/
  wget http://github.com/downloads/r1k0/kigen/kigen-9999.ebuild
  ebuild kigen-9999.ebuild digest

- Merge KIGen
::
  emerge kigen -av

- Care for /etc/kigen.conf

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

 

- Use of kgen to generate a kernel/system.map

- Use of igen to generate an initramfs

Funtoo
~~~~~~

- Add to local overlay

- Merge KIGen

- Care for /etc/kigen.conf

- Use of kgen to generate a kernel/system.map

- Use of igen to generate an initramfs

- Use of igen to generate an initramfs with support for sys-boot/boot-update



:Authors: 
    erick 'r1k0' michau (python engine),

    Portage community (linuxrc scripts),

:Version: 0.1.2 
