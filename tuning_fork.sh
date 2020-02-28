#!/bin/bash

cd /home/pi
if [[ -e /home/pi/tuning_fork ]]; then
        rm tuning_fork || rm -r tuning_fork
fi
mkdir tuning_fork
cd /home/pi/tuning_fork
if [[ ! -e /home/pi/tuning_fork/temp_file.py ]]; then
        touch temp_file.py
fi
echo "Enter data : "
a=`head -n 20 /home/pi/uploaded.py | tail -1`
b=`head -n 21 /home/pi/uploaded.py | tail -1`
while sleep 3; do
        if [[ -s /home/pi/tuning_fork/temp_file.py ]]; then
                echo "" > /home/pi/tuning_fork/temp_file.py
        fi
        echo "Data 1 was: $a"
        echo "Enter new data 1 "
        read a
        sa='s|\[.*,.*,.*\]\)#TUNEME1|['
        sb=']\)#TUNEME1|'
        sc="${sa}${a}${sb}"
        sed -e $sc /home/pi/uploaded.py > /home/pi/tuning_fork/temp_file.py
        cat /home/pi/tuning_fork/temp_file.py > /home/pi/uploaded.py
        if [[ -s /home/pi/tuning_fork/temp_file.py ]]; then
                echo "" > /home/pi/tuning_fork/temp_file.py
        fi
        echo "Data 2 was: $b"
        echo "Enter new data 2 "
        read b
        sa='s|\[.*,.*,.*\]\)#TUNEME2|['
        sb=']\)#TUNEME2|'
        sc="${sa}${b}${sb}"
        sed -e $sc /home/pi/uploaded.py > /home/pi/tuning_fork/temp_file.py
        cat /home/pi/tuning_fork/temp_file.py > /home/pi/uploaded.py
        echo "Enter PID Shown in corner of Vision Status Tab "
        read p
        kill $p
        sleep 1
done
