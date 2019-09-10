#!/bin/sh

echo Granularity: "$1"
echo Total Time: "$2"

now=0 

printf "\t\t\t Load Averages \n" >> testlog.csv
printf "TimeStamp\t\t1min \t5 min \t15 min \n" >> testlog.csv

while [ $now -lt $2 ]

do
printf "$(date "+%Y/%m/%d-%H:%M:%S,")\t" >>testlog.csv;
uptime | awk '{print $8"\t" $9"\t" $10"\n"}' >> testlog.csv

now=$((now+1))

#echo $(date "+%Y/%m/%d-%H:%M:%S") >> testlog.csv;
#cat /proc/loadavg >> testlog;

done

