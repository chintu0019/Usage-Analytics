#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

SCRIPTNAME="`readlink -e "$0"`"
SCRIPTDIR="`dirname "$SCRIPTNAME"`"


if [ "$#" -le 1 ] ;then
    >&2 echo "Usage: $0 input1 [input2 input3 ... inputN] output"
    exit 10
fi


ifiles=()
ofile=''
for file in "${@}" ;do
    if [ -n "$ofile" ] ;then
        if [ ! -f "$ofile" ]; then
            >&2 echo "Error: $ofile does not exist or is not a regular file!"
            exit 1
        else
            ifiles+=( "$ofile" )
        fi
    fi
    ofile="$file"
done
if [ -f "$ofile" ]; then
    >&2 echo "Error: output file $ofile exists!"
    exit 2
fi


first=1
for file in "${ifiles[@]}" ;do
    if [ $first -eq 1 ] ;then
        first=0
        cp "$file" "$ofile"
    else
        tail -n +2 "$file" >> "$ofile"
    fi
done

