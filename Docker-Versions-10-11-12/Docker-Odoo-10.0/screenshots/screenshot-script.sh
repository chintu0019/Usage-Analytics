#! /bin/bash

echo "enter participant's name"
read p_name
if [ -e "$p_name" ]
then
    echo "Participant folder exist"
    cd ./$p_name
else
    echo "Creating folder $p_name"
    mkdir ./$p_name
    cd ./$p_name
fi


echo "screenshots being stored in ./$p_name ...."
while true;
do
    scrot -u -c '%y-%m-%d-%H-%M-%S.png'
done