#!bin/bash

# Adding the namespaces
sudo ip netns add q6ns1
sudo ip netns add q6ns2
sudo ip netns add q6ns3
sudo ip netns add q6ns4

# For q6ns1
sudo ip netns exec q6ns1 sudo ip link add veth0 type veth peer name veth1
sudo ip netns exec q6ns1 sudo ip link set dev veth1 netns q6ns3
sudo ip netns exec q6ns1 ip link set dev veth0 up
sudo ip netns exec q6ns1 ip addr add dev veth0 100.0.1.1/24
sudo ip netns exec q6ns1 route add default gw 100.0.1.2

# For q6ns2
sudo ip netns exec q6ns2 sudo ip link add veth0 type veth peer name veth2
sudo ip netns exec q6ns2 sudo ip link set dev veth2 netns q6ns3
sudo ip netns exec q6ns2 ip link set dev veth0 up
sudo ip netns exec q6ns2 ip addr add dev veth0 100.0.2.1/24
sudo ip netns exec q6ns2 route add default gw 100.0.2.2

# For q6ns4
sudo ip netns exec q6ns4 sudo ip link add veth0 type veth peer name veth4
sudo ip netns exec q6ns4 sudo ip link set dev veth4 netns q6ns3
sudo ip netns exec q6ns4 ip link set dev veth0 up
sudo ip netns exec q6ns4 ip addr add dev veth0 100.0.3.1/24
sudo ip netns exec q6ns4 route add default gw 100.0.3.2