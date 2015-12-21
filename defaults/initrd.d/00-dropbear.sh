#!/bin/sh

. /etc/initrd.d/00-common.sh

runnetstack() {
    if [ "$IP" != "" ]
    then
        good_msg 'Starting network stack'
    fi

    # getting ip up via dhcp
    if [ "${IP}" = "udhcpc" ] || [ "${IP}" = "dhcp" ] || [ "${IP}" = "DHCP" ]
    then
        echo -e "${BOLD}   ::${NORMAL} Bringing up IP via udhcpc..."
        udhcpc &
    elif [ "${IP}" != "" ]
    then
        # getting static ip up
        echo -e "${BOLD}   ::${NORMAL} Bringing up static IP $IP..."
        if [ -n "${NETMASK}" ]
        then
            ifconfig eth0 "${IP}" netmask "${NETMASK}"
        else
            ifconfig eth0 "${IP}"
        fi
        echo -e "${BOLD}   ::${NORMAL} Creating /etc/resolv.conf..."
        if [ -n "${NAMESERVER}" ]
        then
            echo "nameserver ${NAMESERVER}" >> /etc/resolv.conf
        fi
        if [ -n "${DOMAIN}" ]
        then
            echo "domain ${DOMAIN}" >> /etc/resolv.conf
        fi
    fi

    if [ -n "${DEFAULTGW}" ]
    then
        echo -e "${BOLD}   ::${NORMAL} Setting default gateway ..."
        route add default gw ${DEFAULTGW}
    fi

    if [ -n "${DROPBEAR}" ]
    then
        if [ -e /dev/pty0 ]; then # CONFIG_LEGACY_PTYS=n
            ret=1
        else
            [ -d /dev/pts ] || mkdir -p /dev/pts
#            if mount -t devpts devpts /dev/pts 2>/dev/null; then # CONFIG_UNIX98_PTYS=n
#                good_msg "/dev/pts mounted"
#                ret=1
#            else
#                warn_msg "Cannot mount /dev/pts"
#                rm -fr /dev/pts
#            fi
        fi

        if [ "${ret}" = '1' ] && [ -z "${IP}" ]
        then
            bad_msg 'ip= kernel parameter is missing value'
            bad_msg 'add to kernel line ip=x.x.x.x or ip=dhcp'
        else
            echo -e "${BOLD}   ::${NORMAL} Starting dropbear SSH daemon..."
            if [ -f "/sbin/dropbear" ]; then
                # starting dropbear
                dropbear || bad_msg "Oh crap! dropbear won't start -_-'"
            else
                bad_msg "/sbin/dropbear is missing.. Have you run 'kigen initramfs --[bin|source]-dropbear ..'?"
            fi
        fi
#        if [ -e /usr/bin/setsid ] && [ -e /bin/cttyhack ]
#        then
#            echo -e "${BOLD}   ::${NORMAL} Setting job control on..."
#            # that's for ctrl+c
#            setsid cttyhack sh
#        fi
#
#        [ -x /bin/sh ] && /bin/sh || /bin/ash
   fi
}
