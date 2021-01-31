#!/bin/bash
#Setting paths
MIN_PATH="./min"
WEB_PATH="./web-pages"
LOG_PATH="./log"

URLs=$1
THRESHOLD=$2
TIME=$3

#Enviroment variables
export EMAIL_USER=$4
export EMAIL_PASS=$5

#Space as the delimiter
IFS=' '

#Split the words based on the delimiter
read -a strarr <<< "$URLs"

#Count the total words
TOTAL_URLs="${#strarr[*]}"

apt-get install -qq -y wget

#Creating minimum files
if ! [ -d $MIN_PATH ] 
then
	mkdir $MIN_PATH
fi

if ! [ -d $WEB_PATH ]
then
	mkdir $WEB_PATH
fi

if ! [ -d $LOG_PATH ]
then
	mkdir $LOG_PATH
fi

#Removing old files
rm -rf $WEB_PATH/*
rm -rf $MIN_PATH/*
rm -rf $LOG_PATH/*

#Get the pages through the array created	
for i in "${!strarr[@]}";
do
    wget --html-extension --output-document=$WEB_PATH/${i}.html --quiet ${strarr[${i}]}
done

for i in "${!strarr[@]}";
do
    touch $MIN_PATH/${i}.txt
    echo "PRICE||" >> $MIN_PATH/${i}.txt
    echo "DATE||" >> $MIN_PATH/${i}.txt
    echo "URL|${strarr[${i}]}|" >> $MIN_PATH/${i}.txt
    echo "FIRSTPRICE||" >> $MIN_PATH/${i}.txt
    #echo -e "Option ${i} created! :)" 
done

#INITIALIZE OF PROGRAM
python3.7 ./init.py $TOTAL_URLs > $LOG_PATH/log_init.txt

while true; do

	#Get the pages through the array created	
      	for i in "${!strarr[@]}";
      	do
            wget --html-extension --output-document=$WEB_PATH/${i}.html --quiet ${strarr[${i}]}
  	done
	
	python3.7 ./price.py $TOTAL_URLs "$THRESHOLD" > $LOG_PATH/log_price.txt
	
	sleep $TIME
done
