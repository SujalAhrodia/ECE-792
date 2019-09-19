#!/bin/sh

echo Granularity: "$1"
echo Total Time: "$2"
echo X="$3"
echo Y="$4"

T=$1
TP=$2
X=$3
Y=$4
prev_min=0
now=0

printf "\t\t\t Load Averages \n" >> testlog.csv
printf "TimeStamp\t\t1min \t5 min \t15 min \n" >> testlog.csv
printf "TimeStamp\t\t Alert String \t\t CPU Usage \n" >> alertlog.csv

while [ $now -lt $TP ]
do

sleep $T

#LOGGING THE LOAD AVERAGES
printf "$(date "+%Y/%m/%d-%H:%M:%S,")\t" >> testlog.csv
uptime | awk '{print $10"\t" $11"\t" $12""}' >> testlog.csv

a=$(uptime | awk '{print substr($10,0,4)}')
b=$(uptime | awk '{print substr($11,0,4)}')
echo $(uptime)

#LOGGING THE ALERT MESSAGES
if [ $(echo "$a > $X" | bc) -eq 1 ]
then
        printf "$(date "+%Y/%m/%d-%H:%M:%S,")\t" >> alertlog.csv
        printf "HIGH CPU usage,\t\t $a \n" >> alertlog.csv
fi

if [ $(echo "$b > $Y" | bc) -eq 1 ]
then
        if [   $(echo "$a > $prev_min" | bc) -eq 1 ]
        then
                printf "$(date "+%Y/%m/%d-%H:%M:%S,")\t" >> alertlog.csv
                printf "Very HIGH CPU usage,\t $b \n" >> alertlog.csv
        fi
fi

prev_min=$a
now=$((now+T))

done

#NOTE: For the first reading of VERY HIGH CPU USAGE, we do not have any previous value to compare with, as our recordings start from that instant. So we compare the first 1 min value with 0 and it is always greater than or equal to zero. So it is expected that the alertlog will have a VERY HIGH CPU USAGE log everytime, which can be ignored.
