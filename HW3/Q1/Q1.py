import libvirt
from paramiko import SSHClient
from ipaddress import IPv4Address
from random import getrandbits
import pprint
import random
import os
import re

def printAddresses(h):
    conn=libvirt.open(h)
    domainID=conn.listDomainsID()
    #domainID=[74]
    #print(domainID)
    for d in domainID:
        dom=conn.lookupByID(d)
        print('\n'+dom.name())
        s=os.popen('virsh domifaddr '+dom.name()).read()
        s=re.match(r'.*\n.*\n.*ipv.* (\d+\.\d+\.\d+\.\d+)\/.*',s)
        mgmt_ip=''
        if s:
            mgmt_ip=s.group(1)
        else:
            continue
        print(mgmt_ip)
        intf = dom.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT)
        ip_dict={}
        mac_dict={}
        for (name, val) in intf.items():
            print('\n\t'+name)
            if val['addrs']:
                for ip in val['addrs']:
                    if '.' in ip['addr']:
                        print('\tIP : '+ip['addr'])
                        #for simplicity, we print only IPv4
                        ip_dict.update({name:ip['addr']})
            print('\tMAC : '+val['hwaddr'])
            mac_dict.update({name:val['hwaddr']})
        ip_dict,mac_dict=resolveDuplicates(ip_dict,mac_dict,mgmt_ip)
        print('\nResolved!')
        #pprint.pprint(ip_dict)
        pprint.pprint(mac_dict)

def resolveDuplicates(ip_dict,mac_dict,mgmt_ip):
    print('\nResolving duplicate addresses if any... \n')
    ip_list=list(ip_dict.values()) #has only the values
    ikey_list=list(ip_dict.keys()) #has only the keys
    ipush_dict={} #has the updated interface and ip that need to be pushed to the device
    dup=0
    for i in range(len(ip_list)):
        if ip_list[i] in ip_list[i+1:]:
            dup=1
            print('Duplicate IP detected at ' + ikey_list[i])
            if ip_list[i] != mgmt_ip:
                new_ip=getAnotherIP(ip_list)
                ipush_dict.update({ikey_list[i]:(ip_list[i],new_ip)})
    if not dup:
        print('No IP duplicates')
    dup=0
    mkey_list=list(mac_dict.keys())
    mac_list=list(mac_dict.values())
    mpush_dict={}
    for m in range(len(mac_list)):
        if mac_list[m] in mac_list[m+1:]:
            dup=1
            print('Duplicate MAC detected at '+ mkey_list[m])
            mac_list[m]=getAnotherMAC(mac_list)
            mpush_dict.update({mkey_list[m]:mac_list[m]})
    if not dup:
        print('No MAC duplicates')
    pushChanges(ipush_dict,mpush_dict,mgmt_ip)
    ip_dict=dict(zip(ip_dict.keys(),ip_list))
    mac_dict=dict(zip(mac_dict.keys(),mac_list))
    return ip_dict, mac_dict

def pushChanges(ipush_dict,mpush_dict,mgmt_ip):
    #uname=raw_input('Enter username for ' + mgmt_ip + ': ')
    #pw=raw_input('Enter password for above user : ')
    uname='root'
    pw='linux@123'
    ssh=SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(mgmt_ip,username=uname,password=pw)
    for key,val in ipush_dict.items():
        command='ip addr del '+val[0]+' dev '+key+'\nip addr add '+val[1]+' dev '+key
        print('Command executed : ' +command)
        si,so,se=ssh.exec_command(command)
        if se:
            print(se.readlines())

    for key,val in mpush_dict.items():
        print(mgmt_ip,key,val)
        command='sudo ifconfig '+key+' down\nsudo ifconfig '+key+' hw ether '+val+'\nsudo ifconfig '+key+' up'
        print('Command executed : '+command)
        si,so,se=ssh.exec_command(command)
        if se:
            print(se.readlines())

def getAnotherIP(ip_list):
    ip=str(IPv4Address(getrandbits(32)))
    if ip in ip_list: #prevent new addr from being repeated too
        getAnotherIP(ip_list)
    return ip

def getAnotherMAC(mac_list):
    mac="02:%02x:%02x:%02x:%02x:%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
        )
    if mac in mac_list:
        getAnotherMAC(mac_list)
    return mac

def main():
    print('\nProgram to detect and resolve duplicate MAC and IP addresses \n across multiple hypervisors and their VMs\n-------------------------------')
    n=input('Enter number of hypervisors : ')
    hypervisors=[]
    for i in range(n):
        h=raw_input('Enter hypervisor name : ')
        hypervisors.append(h)
        #hypervisors=['qemu:///system']
    for h in hypervisors:
        printAddresses(h)

if __name__=="__main__":
    main()
