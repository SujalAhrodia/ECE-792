import libvirt
import sys

cl=libvirt.open("qemu:///system")

# Host Information
hname = cl.getHostname()
hmodel, hmem, hacpu, hf, hnuma, hsocket, hcore, hthread =  cl.getInfo()

if cl == None:
    print ("Failed to connect", sys.stderr)
    exit(1)

print ("------------------")
print ("Host Information:")
print ("------------------")
print ("Host Name:" + str(hname))
print ("CPU Model:"+ str(hmodel))
print ("Host Memory:"+ str(hmem))
print ("Host Active CPUs:"+ str(hacpu))
print ("Host CPU Frequency(mHz):"+ str(hf))
print ("Number of NUMA nodes in Host:"+ str(hnuma))
print ("CPU Sockets/node :"+ str(hsocket))
print ("CPU cores/socket :"+ str(hcore))
print ("CPU threads/core :"+ str(hthread))
print ("------------------")

# Guest information via domains

print ("Guest Information:")
print ("------------------")

vm=cl.listDomainsID()

for i in vm:
    print ("Guest Name:" + str(cl.lookupByID(i).name()))
    gstate, gmmem, gmem, gcpu, gcput = cl.lookupByID(i).info()
    print ("State:" + str(gstate))
    print ("Maximum Memory:" + str(gmmem))
    print ("Memory:" + str(gmem))
    print ("No. of CPUs:" + str(gcpu))
    print ("CPU Time:" + str(gcput))
    print ("------------------")




