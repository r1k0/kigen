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
