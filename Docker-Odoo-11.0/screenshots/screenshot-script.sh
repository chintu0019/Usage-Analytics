#!/bin/bash
set -euo pipefail
IFS=$'\n\t'


echo "enter participant's name"
read name
if [ -e "$name" ]
then
    echo "Participant folder exist"
    cd ./"$name"
else
    echo "Creating folder $name"
    mkdir ./"$name"
    cd ./"$name"
fi


echo "screenshots being stored in ./$name ...."
while true;
do
    scrot --focused '%y-%m-%d-%H-%M-%S.png'
done

