import libvirt
import sys
from time import sleep
import datetime
import csv

cl=libvirt.open("qemu:///system")

if cl == None:
    print ("Failed to connect", sys.stderr)
    exit(1)

bool_cpu=0
bool_mem=0

try:
    if sys.argv[1] == "CPU":
        bool_cpu=1
    if sys.argv[1] == "MEM":
        bool_mem=1
    
    interval = int(raw_input("Enter the polling interval : "))
    window = int(raw_input("Enter the window size : "))
    total = int(raw_input("Enter the total time : "))
except:
    print ("Please give arguments. eg: CPU/MEM")
    exit(1)

vm=cl.listDomainsID()
cpus = {}
mems = {}
k=0

# reading and computing usage
for i in vm:
    temp_m = []
    temp_c = []
    for j in range(0,total):
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
        temp_m.append(musage)

        #CPU usage
        cusage = 100*float((utime+stime)/ctime)
        temp_c.append(cusage)

        sleep(interval)
    mems[k] = cl.lookupByID(i).name(), temp_m
    cpus[k] = cl.lookupByID(i).name(), temp_c
    k+=1

#no. of entries 
n = total/interval

# moving averages of each VM (CPU)
c_avgs = {}

#computing moving averages for CPU usage
for k in cpus.values():
    avg=[]
    for i in range (0, n-window+1):
        sum1=0
        for j in range(i, i+window):
            sum1+=k[1][j]
        avg.append(float(sum1/window))
    c_avgs[k[0]] = avg       

# moving averages of each VM(MEM)    
m_avgs = {}    

#computing moving averages for CPU usage
for k in mems.values():
    avg=[]
    for i in range (0, n-window+1):
        sum1=0
        for j in range(i, i+window):
            sum1+=k[1][j]
        avg.append(float(sum1/window))
    m_avgs[k[0]] = avg       

if bool_cpu:
    # sorting
    for i in range (0, n-window+1):
        # list of sorted cpus
        sorted_cpus= []

        print ("------------------")
        print ("At Polling interval : " + str(i+1))
        print ("------------------")
        print ("Sorted List of VMS:")
        print ("------------------")

        sorted_cpus = sorted(c_avgs.items(), key=lambda x: x[1][i])

        for j in sorted_cpus:
            print ("VM Name: "+ str(j[0]))
            print ("CPU Usage: "+ str(j[1][i])+ "%" )

if bool_mem:
    for i in range (0, n-window+1):

        # list of sorted mems
        sorted_mems = []
        
        print ("------------------")
        print ("At Polling interval : " + str(i+1))
        print ("------------------")
        print ("Sorted List of VMS:")
        print ("------------------")

        sorted_mems = sorted(c_avgs.items(), key=lambda x: x[1][i])

        for j in sorted_mems:
            print ("VM Name: "+ str(j[0]))
            print ("MEM Usage: "+ str(j[1][i])+ "%" )

