#!/bin/bash

echo interface = $1 >> /etc/dnsmasq.d/dnsmasq.conf

new_ip=$(echo "$2" | cut -c-6)

echo dhcp-range=$1,$new_ip.2,$new_ip.254 >> /etc/dnsmasq.d/dnsmasq.conf

sudo systemctl restart dnsmasq