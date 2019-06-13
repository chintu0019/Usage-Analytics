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

        >&2 echo "Start an experiment session"
        >&2 echo "--database|-d database.tar.bz2   -- Set up the db from this backup file."
        >&2 echo "--clean_table|-c                 -- Clean the db filestore of..."
        >&2 echo "--docker_machine|-m 1234567      -- ...of this docker machine id."
        >&2 echo "--no_experiment|-n               -- Do other actions, but skip the experiment."

        exit 1
    ;;
    -d|--database)
        shift
        database="$1"
        shift
    ;;
    -c|--clean_table)
        shift
        clean_table=''
    ;;
    -m|--docker_machine)
        shift
        docker_machine="$1"
        shift
    ;;
    -n|--no_experiment)
        shift
        no_experiment=''
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
    echo "copying db $database in $docker_machine"
    if [ ! -f "$database" ] ;then
        >&2 echo "Database file missing!"
        exit 1
    fi

    dbfpath="`readlink -e "$database"`"
    dbdir="`dirname "$dbfpath"`"
    dbfname="`basename "$dbfpath"`"

    docker run --rm -v odoo11_odoo-db-data-odoo11:/volume -v "$dbdir":/backup alpine sh -c "find /volume -mindepth 1 -delete ; tar -C /volume/ -xjf /backup/$dbfname"

    echo "Done."
fi

if [[ -n ${clean_table+x} ]] ;then
    docker exec "$docker_machine" /usr/bin/psql -U postgres -d odoo11 -c 'delete from ir_attachment;'
fi


if [[ -n ${clean_table+x} ]] ;then
    echo "Experiment skipped as requested."
    exit 0
fi


mkdir -p results
docker-compose up --build

cd odoo/csvfolder

find  -type f  -iname '*.csv'  -size +63c  -exec cp -v '{}' ../../results ';'
rm *

