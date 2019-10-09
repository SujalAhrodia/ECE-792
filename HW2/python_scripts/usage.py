import libvirt
import sys
from time import sleep
import datetime

cl=libvirt.open("qemu:///system")

if cl == None:
    print ("Failed to connect", sys.stderr)
    exit(1)

vm=cl.listDomainsID()
cpus = {}
mems = {}
j=0

for i in vm:
    cstats = cl.lookupByID(i).getCPUStats(True)[0]
    mstats = cl.lookupByID(i).memoryStats()

    #CPU times
    ctime = (float(cstats['cpu_time'])/1000000000)
    stime = (float(cstats['system_time'])/1000000000)
    utime = (float(cstats['user_time'])/1000000000)

    #Memory Stats
    cmem = float(mstats['rss'])
    tmem = float(mstats['actual'])

    #Memory Usage
    musage = 100*float(cmem/tmem)
    mems[j] = cl.lookupByID(i).name(),musage

    #CPU usage
    cusage = 100*float((utime+stime)/ctime)
    cpus[j] = cl.lookupByID(i).name(),cusage

    j=j+1

# list of sorted cpus
sorted_cpus= []

#list of sorted mems
sorted_mems = []

# sorting
sorted_cpus = sorted(cpus.items(), key=lambda x: x[1][1])
sorted_mems = sorted(mems.items(), key=lambda x: x[1][1])

try:

    if sys.argv[1] == "CPU":
        print ("------------------")
        print ("Sorted List of VMS:")
        print ("------------------")
        for i in sorted_cpus:
            print ("VM Name: "+ str(i[1][0]))
            print ("CPU Usage: "+ str(i[1][1])+ "%" )
        
        print ("------------------")
        print ("Threshold Check")
        print ("------------------")

        t = float(raw_input("Enter the threshold value for CPU Usage: "))

        for i in sorted_cpus:
            if i[1][1] > t :
                timestamp = str(datetime.datetime.now())
                msg = (str(i[1][0]) + "\t" + timestamp + "\t" + str(i[1][1]) + "%" )
                print (msg)
                with open('alert.txt', 'a') as f:
                    f.write(msg + "\n")
                    f.close()

    elif sys.argv[1] == "MEM":
        print ("------------------")
        print ("Sorted List of VMS:")
        print ("------------------")
        for i in sorted_mems:
            print ("VM Name: "+ str(i[1][0]))
            print ("MEM Usage: "+ str(i[1][1])+ "%" )

except:
    print ("Please give arguments. eg: CPU/MEM")
    exit(1)