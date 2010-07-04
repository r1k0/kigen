==================================
KIGen kernel/initramfs generator
==================================

.. sectnum::

.. contents:: Table of contents

Introduction
~~~~~~~~~~~~

KIGen is a set of 2 commands: kgen and igen.

**igen uses Genkernel linuxrc and provides the same boot interface as Genkernel does.**

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

:Authors: 
    erick 'r1k0' michau (python engine),

    Portage community (linuxrc scripts),

:Version: 0.1.5
