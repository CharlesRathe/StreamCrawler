#Author: M. Zubair Rafique

#Permission  to  freely  reproduce  all  or  part  of  this  code  for  noncommercial
#purposes is granted provided that copies bear this notice and the full citation
#of our NDSS 2016 paper.  
#https://zubairrafique.wordpress.com/2015/10/28/ndss-2016-its-free-for-a-reason-exploring-the-ecosystem-of-free-live-streaming-services/

# Reproduction for commercial purposes is strictly prohibited without the prior written consent from 
# the KU Leuven, the Internet Society, and the first author: M Zubair Rafique

#Comments and Suggestions: <zubair.rafique@cs.kuleuven.be> <rafique.zubair@gmail.com>
# ======================================================================================

#!/bin/bash 
interface=$(ifconfig | grep 'wlan' | cut -d ' ' -f1) #use eth, wlan, tun depending on config
interface=$(echo $interface|cut -d ' ' -f1)
echo $interface
sudo echo "nameserver 127.0.1.1">>/etc/resolvconf/resolv.conf.d/base
sudo echo "nameserver 8.8.8.8">>/etc/resolvconf/resolv.conf.d/base
sudo echo "nameserver 127.0.1.1">>/etc/resolvconf/resolv.conf.d/head
sudo echo "nameserver 8.8.8.8">>/etc/resolvconf/resolv.conf.d/head
sudo service network-manager restart
sleep 2
for ((name=16;name<=49;name+=1))
do
echo $i
sudo ip netns add bot$name
sudo ip link add veth-a$name type veth peer name veth-b$name
sudo ip link set veth-a$name netns bot$name
sudo ip netns exec bot$name ifconfig veth-a$name up 192.168.$name.1 netmask 255.255.255.0
sudo ifconfig veth-b$name up 192.168.$name.254 netmask 255.255.255.0
sudo ip netns exec bot$name route add default gw 192.168.$name.254 dev veth-a$name
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
sudo iptables -t nat -A POSTROUTING -s 192.168.$name.0/24 -o $interface -j MASQUERADE #use eth0 or wlan0 depending on config
sudo iptables -A FORWARD -i $interface -o veth-b$name -j ACCEPT
sudo iptables -A FORWARD -o wlan0 -i veth-b$name -j ACCEPT
sudo ip netns exec bot$name ip link set lo up
done
