#!/bin/sh
if  [ "$1" = "-h" ]     || \
    [ "$1" = "--help" ] || \
    [ "$1" = "" ]
then
    echo "$0 <LUKS root device>"
    echo "i.e. # $0 /dev/sda3"
    exit
fi

while [ "$(ps|grep cryptsetup|grep -v grep|wc -l)" -gt '0']; do
  cryptPID="$(ps|grep cryptsetup|grep -v grep|sed -e 's/^ //g')"
  echo Killing "$cryptPID"...
  kill -9 "$cryptPID" && echo PID "$cryptPID" killed.
  sleep 0.2
done

/sbin/cryptsetup luksOpen $1 root || exit 1
sleep 1
/bin/lvm vgscan 
sleep 1
/bin/lvm vgchange -a y
sleep 1

/sbin/ttyecho -n /dev/console q
