#!/bin/sh

echo Granularity: "$1"
echo Total Time: "$2"
echo X="$3"
echo Y="$4"

now=0 

printf "\t\t\t Load Averages \n" >> testlog.csv
printf "TimeStamp\t\t1min \t5 min \t15 min \n" >> testlog.csv
printf "TimeStamp\t\t Alert String \t\t CPU Usage \n" >> alertlog.csv

while [ $now -lt $2 ]

do
printf "$(date "+%Y/%m/%d-%H:%M:%S,")\t" >> testlog.csv
uptime | awk '{print $8"\t" $9"\t" $10"\n"}' >> testlog.csv

a=$(uptime | awk '{print $8}')
b=$(uptime | awk '{print $9}')

if [ $a > $3 ]
then 
	printf "$(date "+%Y/%m/%d-%H:%M:%S,")\t" >> alertlog.csv
	printf "HIGH CPU usage,\t\t $a \n" >> alertlog.csv
fi

if [ $b > $4 ]
then
	printf "$(date "+%Y/%m/%d-%H:%M:%S,")\t" >> alertlog.csv
	printf "Very HIGH CPU usage,\t $b \n" >> alertlog.csv
fi

now=$((now+1))

done

