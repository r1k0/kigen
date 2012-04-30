#!/bin/sh
if  [ "$1" = "-h" ]     || \
    [ "$1" = "--help" ] || \
    [ "$1" = "" ]      # || \
#    [ "$2" = "" ]
then
    echo "$0 <root device>" # <lvm root device>"
    echo "i.e. # ./boot-luks-lvm.sh /dev/sda2" # /dev/mapper/vg_sabayon-lv_root"
    exit
fi
pkill cryptsetup
sleep 2
/sbin/cryptsetup luksOpen $1 root
sleep 2
/bin/lvm vgscan
sleep 1
/bin/lvm vgchange -a y
sleep 1
/sbin/ttyecho -n /dev/console q
