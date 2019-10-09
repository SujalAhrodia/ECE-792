import os
import time

name=os.popen('hostname').read()
name=name[:-1]
curr=0
total=180 #run for 3 minutes
n=0
while curr <= total:
    time.sleep(60) #sleep for 1 minute
    result=os.popen('uptime').read()
    n=result.find('load average: ')
    min1=result[n+14:n+17]
    min5=result[n+20:n+23]
    min15=result[n+26:n+29]
    with open("/var/customlog/logs/testlog.csv","a") as file:
        string=name + ', ' + min1 + ', ' + min5+ ', '+min15
        file.write(string+'\n')
    curr+=2
