#!/bin/sh
if  [ "$1" = "-h" ]     || \
    [ "$1" = "--help" ] || \
    [ "$1" = "" ]
then
    echo "$0 <root device>"
    echo "i.e. # $0 /dev/sda2"
    exit
fi

pkill cryptsetup
sleep 2 || exit 
/sbin/cryptsetup luksOpen $1 root || exit 
sleep 2 || exit 
/bin/lvm vgscan 
sleep 1 || exit 
/bin/lvm vgchange -a y
sleep 1 || exit 1 
/sbin/ttyecho -n /dev/console q
