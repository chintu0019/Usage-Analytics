#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

SCRIPTNAME="`readlink -e "$0"`"
SCRIPTDIR="`dirname "$SCRIPTNAME"`"

cd "$SCRIPTDIR"

while [[ $# -gt 0 ]] ;do
key="$1"

case "$key" in
    -h|--help)
        >&2 echo "Back up the db"
        >&2 echo "--database|-d database.tar.bz2   -- Back up on this file the database..."
        >&2 echo "--docker_machine|-m              -- ...of this docker machine."
        >&2 echo ""
        exit 1
    ;;
    -d|--database)
        shift
        database="$1"
        shift
    ;;
    -m|--docker_machine)
        shift
        docker_machine="$1"
        shift
    ;;
    *)
        >&2 echo "Ignored: "$1
        shift
    ;;
esac
done

if [[ -n ${clean_table+x} ]] ;then
    if [[ -z ${docker_machine+x} ]] ;then
        >&2 echo "Tell me the docker machine id! (with -m)"
        exit 1
    fi
fi



if [[ -n ${database+x} ]] ;then
    echo "Copying the db in $docker_machine in file $database"
    if [ -f "$database" ] ;then
        >&2 echo "Database file exists!"
        exit 1
    fi

    dbfpath="`readlink -e "$database"`"
    dbdir="`dirname "$dbfpath"`"
    dbfname="`basename "$dbfpath"`"

    mkdir -p "$dbdir"
    docker run --rm -v odoo10_odoo-db-data-odoo10:/volume -v "$dbdir":/backup alpine tar -cjf /backup/"$dbfname" -C /volume ./

    echo "Done."
fi

