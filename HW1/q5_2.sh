#!/bin/sh

echo 1-minute Threshold: "$1"
echo 5-minute Threshold: "$2"
thresh1=$(uptime | awk '{print substr($8,1,length($8)-1)}' )
thresh5=$(uptime | awk '{print substr($9,1,length($9)-1)}')
printf "One minute observation: $thresh1 \nFive minute observation: $thresh5\n"

if [ $1 > $thresh1 ]
then
	zenity --error --text="Exceeding one minute threshold\!" --title="Warning!"
fi

if [ $2 > $thresh5 ]
then
	zenity --error --text="Exceeding five minute threshold\!" --title="Warning!"
fi
