#!/bin/sh
if  [ "$1" = "-h" ]     || \
    [ "$1" = "--help" ] || \
    [ "$1" = "" ]
then
    echo "$0 <root device>"
    echo "i.e. # ./boot-luks.sh /dev/sda2"
    exit
fi
pkill cryptsetup
sleep 2
/sbin/cryptsetup luksOpen $1 root
sleep 2
/sbin/ttyecho -n /dev/console /dev/mapper/root
