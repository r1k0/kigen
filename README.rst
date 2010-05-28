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

KIGen is a kernel and initramfs builder designed to interface with
sys-apps/boot-update and provides a more visible configuration file than genkernel
in terms of kernel modules at least.
KIGen will automagically detect if you are running boot-update (we support Gentoo and
Sabayon too) then read your /etc/boot.conf and overwrite your /etc/KIGen.conf
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

  - LUKS by shipping the cryptsetup binary
  - LVM2 by shipping the lvm.static binary
  - UUID by shipping the blkid binary
  - splash decorator

Supported OS
~~~~~~~~~~~~

KIGen supports Portage and provides support for the following linux based flavors:

  - Funtoo  and its boot-update interface,
  - Gentoo  (no boot-update interface yet),
  - Sabayon (no boot-update interface yet).
  - VLOS    (no boot-update interface yet).
  - ChromeOS? ;P

but KIGen works on the following flavors:
  
  - Debian
  - Ubuntu
  - ArchLinux

Portage support
~~~~~~~~~~~~~~~

KIGen imports colors from Portage itself. It keeps the code simpler.
If Portage API cannot be found color are disabled, hence non Portage systems
don't and won't have any color support.

KIGen will detect /etc/boot.conf and will append the modules configuration from /etc/KIGen.conf
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

KIGen works on Debian without any color support.
KIGen is not meant (for now) to be installed on non Portage systems and should work out of the box
by locally importing its modules.

Have fun too!


