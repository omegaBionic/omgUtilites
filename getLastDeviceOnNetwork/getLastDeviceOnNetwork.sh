#!/bin/bash

DEBUG="false"
PORT="22,80,443"

### arg(s) ###
# get arg(s)
if [ $# -eq 1 ]; then
    NETWORK_IPV4=$1
else
    /bin/echo "In first parameter enter the network you want to scan like that :"
    /bin/echo "  - \"192.168.1.*\" for scan all ipv4 on 192.168.1.0"
    /bin/echo "  - \"192.168.1.1-10\" for scan all ipv4 between 1 and 10"
    /bin/echo "After wait for the first scan, connect your device on network and press key for launch second scan and enjoy!"
    read -p "Input your network: " NETWORK_IPV4 
fi
# show arg(s) if $DEBUG == true
if $DEBUG; then
    echo "[Debug] NETWORK_IPV4: '"${NETWORK_IPV4}"'"
fi

### main ###
echo "[Info] Program launched"
# first scan
RET_SCAN_IPV4_FIRST=$(nmap -p $PORT $NETWORK_IPV4 --open | grep "Nmap scan report for" | awk '{print $5}')
if $DEBUG; then
    echo "[Debug] RET_SCAN_IPV4_FIRST: ["
    for IPV4 in $RET_SCAN_IPV4_FIRST
    do
        echo "\""$IPV4"\""
    done
    echo ']'
fi

# second scan
read -p "[Info] Press key when you want launch the second scan." CONTINUE
RET_SCAN_IPV4_LAST=$(nmap -p $PORT $NETWORK_IPV4 --open | grep "Nmap scan report for" | awk '{print $5}')
if $DEBUG; then
    echo "[Debug] RET_SCAN_IPV4_LAST: ["
    for IPV4 in $RET_SCAN_IPV4_LAST
    do
        echo "\""$IPV4"\""
    done
    echo ']'
fi

# calculate if is in list
for IPV4_LAST in $RET_SCAN_IPV4_LAST
do
    IS_IN_LIST="false"
    for IPV4_FIRST in $RET_SCAN_IPV4_FIRST
    do
        if [ $IPV4_FIRST == $IPV4_LAST ]
        then
            IS_IN_LIST="true"
        fi
    done
    if ! $IS_IN_LIST
    then
        echo "[Info] New IPV4 item is: '"${IPV4_LAST}"'"
    fi
done

echo "[Info] End of program."