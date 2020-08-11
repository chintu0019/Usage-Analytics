#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

SCRIPTNAME="`greadlink -n -e "$0"`"
SCRIPTDIR="`dirname "$SCRIPTNAME"`"

#echo "SCRIPTNAME" $SCRIPTNAME
#echo "SCRIPTDIR" $SCRIPTDIR

#echo "arg" $1
user=unnamed

cd "$SCRIPTDIR"/results
mkdir -p "$user"
userdir="`greadlink -n -e "$user"`"

#echo "userdir" $userdir

cd "$userdir"
participants_file="`greadlink -n -e "$SCRIPTDIR/results/Participants.csv"`"
#echo "participants_file" $participants_file

#unset IFS
#while read -r userID username
#    do
#        echo "$userID $username"
#    done < <(grep "" $participants_file)

#userID=`tail -1 $participants_file | head -1 | cut -d',' -f1` 
#echo "userID" $userID

cd "$SCRIPTDIR"

python update_userid.py $userdir $user

#echo "clean up? [y/n]"
#read response
#if [ "$response" == 'y' ]
#then 
#    cd results
#    rm -rf $user
#fi
