import libvirt
import sys
from time import sleep
import datetime
import csv

cl=libvirt.open("qemu:///system")

if cl == None:
    print ("Failed to connect", sys.stderr)
    exit(1)

interval = int(raw_input("Enter the polling interval : "))
window = int(raw_input("Enter the window size : "))
total = int(raw_input("Enter the total time : "))

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

# moving averages of each VM
avgs = {}

#computing moving averages
for k in cpus.values():
    # print(k[1][0])
    avg=[]
    for i in range (0, n-window+1):
        sum1=0
        for j in range(i, i+window):
            sum1+=k[1][j]
        avg.append(float(sum1/window))
    avgs[k[0]] = avg       
    

# # list of sorted cpus
sorted_cpus= []

# #list of sorted mems
sorted_mems = []

# # sorting
# for i in cpus:

# sorted_cpus = sorted(cpus.items(), key=lambda x: x[1][1])
# sorted_mems = sorted(mems.items(), key=lambda x: x[1][1])

# try:

#     if sys.argv[1] == "CPU":
#         print ("------------------")
#         print ("Sorted List of VMS:")
#         print ("------------------")
#         for i in sorted_cpus:
#             print ("VM Name: "+ str(i[1][0]))
#             print ("CPU Usage: "+ str(i[1][1])+ "%" )
        
#         print ("------------------")
#         print ("Threshold Check")
#         print ("------------------")

#         t = float(raw_input("Enter the threshold value for CPU Usage: "))

#         for i in sorted_cpus:
#             if i[1][1] > t :
#                 timestamp = str(datetime.datetime.now())
#                 msg = (str(i[1][0]) + "\t" + timestamp + "\t" + str(i[1][1]) + "%" )
#                 print (msg)
#                 with open('alert.txt', 'a') as f:
#                     # wr = csv.writer(f, quoting=csv.QUOTE_MINIMAL,delimiter=' ')
#                     f.write(msg + "\n")
#                     f.close()

#     elif sys.argv[1] == "MEM":
#         print ("------------------")
#         print ("Sorted List of VMS:")
#         print ("------------------")
#         for i in sorted_mems:
#             print ("VM Name: "+ str(i[1][0]))
#             print ("MEM Usage: "+ str(i[1][1])+ "%" )

# except:
#     print ("Please give arguments. eg: CPU/MEM")
#     exit(1)