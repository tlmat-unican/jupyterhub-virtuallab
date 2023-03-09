#!/bin/sh

DISK=/dev/root
DISK_FREE=$(df -BG $DISK | grep $DISK | awk '{ print $4 }' | sed 's/G//g')
USER_SERVERS=$(docker ps | wc -l)
NEW_USER_SERVERS=$(docker ps | grep -E "(Up [0-4] minute|seconds)" | wc -l)

MEMORY_USED=$(free -m | grep Mem | awk '{ print $3 }')
CPU=$[100-$(vmstat 1 1|tail -1|awk '{print $15}')]
TIME=$(date +"%F %H:%M")

echo "$TIME,$USER_SERVERS,$DISK_FREE,$MEMORY_USED,$CPU,$NEW_USER_SERVERS"
