#!/bin/sh

echo 1-minute Threshold: "$1"
echo 5-minute Threshold: "$2"

thresh1=$(uptime | awk '{print substr($8,1,length($8)-1)}' )
thresh5=$(uptime | awk '{print substr($9,1,length($9)-1)}')

printf "One minute observation: $thresh1 \nFive minute observation: $thresh5\n"

printf "Timestamp, Alert message, CPU Load Average\n" >> alert.csv
high="HIGH CPU usage"
very_high="Very HIGH CPU usage"

if [ $1 > $thresh1 ]
then
	zenity --error --text="HIGH CPU usage" --title="Warning!"
	printf "$(date "+%Y/%m/%d-%H:%M:%S, ")" >> alert.csv
	printf "${high}, ${thresh1}\n" >> alert.csv	
fi

if [ $2 > $thresh5 ]
then
	zenity --error --text="Very HIGH CPU usage" --title="Warning!"
	printf "$(date "+%Y/%m/%d-%H:%M:%S, ")" >> alert.csv
        printf "${very_high}, ${thresh5}\n" >> alert.csv

fi

#need to add timer condition around if
