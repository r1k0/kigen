#!/bin/sh
if  [ "$1" = "-h" ]     || \
    [ "$1" = "--help"]  || \
    [ "$1" = "" ]
then
    echo "$0 <root device>"
    echo "i.e. # ./boot-luks-lvm.sh /dev/sda2"
    exit
fi
/sbin/ttyecho -n /dev/console ^D 
sleep 3                          
/sbin/cryptsetup luksOpen $1 root
sleep 1
/sbin/ttyecho -n /dev/console $1
sleep 1                           
exit                              

