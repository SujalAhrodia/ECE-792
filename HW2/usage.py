import libvirt
import sys
from time import sleep

cl=libvirt.open("qemu:///system")

if cl == None:
    print ("Failed to connect", sys.stderr)
    exit(1)

vm=cl.listDomainsID()
cpus = {}
mems = {}
j=0

for i in vm:
    stats = cl.lookupByID(i).getCPUStats(True)[0]
    ctime = (float(stats['cpu_time'])/1000000000)
    stime = (float(stats['system_time'])/1000000000)
    utime = (float(stats['user_time'])/1000000000)

    usage = float(100*(utime+stime)/ctime)
    cpus[j] = cl.lookupByID(i).name(),usage
    j=j+1

# list of sorted cpus
sorted_cpus= []

# sorting
sorted_cpus = sorted(cpus.items(), key=lambda x: x[1][1])

print ("------------------")
print ("Sorted List of VMS:")
print ("------------------")
for i in sorted_cpus:
    print ("VM Name: "+ str(i[1][0]))
    print ("CPU Usage: "+ str(i[1][1])+ "%" )



# for i in range(0,len(vm)):
#     gstate, gmmem, gmem, gcpu, gcput = cl.lookupByID(vm[i]).info()
#     vms[i] = [vm[i],cl.lookupByID(vm[i]).name(), gcpu, gmem]

