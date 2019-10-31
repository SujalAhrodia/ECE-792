#!bin/bash

# For gre interface on q6ns1
sudo ip netns exec q6ns1 ip tunnel add gre1 mode gre remote 100.0.2.1 local 100.0.1.1 ttl 255
sudo ip netns exec q6ns1 ip link set gre1 up
sudo ip netns exec q6ns1 ip addr add 11.0.0.1/24 dev gre1

# For gre interface on q6ns2
sudo ip netns exec q6ns2 ip tunnel add gre1 mode gre remote 100.0.1.1 local 100.0.2.1 ttl 255
sudo ip netns exec q6ns2 ip link set gre1 up
sudo ip netns exec q6ns2 ip addr add 11.0.0.2/24 dev gre1