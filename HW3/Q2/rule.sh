#!/bin/bash

a=$(echo "$1" | cut -c-6)
ip=$a.0/24

iptables -t nat -A POSTROUTING -s $ip ! -d $ip -j MASQUERADE
