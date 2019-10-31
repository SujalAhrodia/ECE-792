#!bin/bash

# For vxlan interface on q6ns1
sudo ip netns exec q6ns1 ip link add vxlan0 type vxlan id 42 group 239.1.1.1 dev veth0 dstport 4789
sudo ip netns exec q6ns1 ip link set dev vxlan0 up
sudo ip netns exec q6ns1 ip addr add dev vxlan0 10.0.0.1/24

# For vxlan interface on q6ns2
sudo ip netns exec q6ns2 ip link add vxlan1 type vxlan id 42 group 239.1.1.1 dev veth0 dstport 4789
sudo ip netns exec q6ns2 ip link set dev vxlan1 up
sudo ip netns exec q6ns2 ip addr add dev vxlan1 10.0.0.2/24