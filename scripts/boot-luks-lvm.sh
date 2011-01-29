#!/bin/sh
if  [ "$1" = "-h" ]     || \
    [ "$1" = "--help"]  || \
    [ "$1" = "" ]       || \
    [ "$2" = "" ]
then
    echo "$0 <root device> <lvm root device>"
    echo "i.e. # ./boot-luks-lvm.sh /dev/sda2 /dev/mapper/vg_sabayon-lv_root"
    exit
fi
/sbin/ttyecho -n /dev/console ^D 
sleep 3                          
/sbin/cryptsetup luksOpen $1 root
vgscan                                                      
vgchange -a y                                               
/sbin/ttyecho -n /dev/console $2
sleep 1                           
exit                              

