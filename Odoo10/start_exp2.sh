#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

odoov=10

function kill_screenshot {
    kill -15 $ss ||true
}


SCRIPTNAME="`readlink -n -e "$0"`"
SCRIPTDIR="`dirname "$SCRIPTNAME"`"

user=unnamed

while [[ $# -gt 0 ]] ;do
key="$1"

case "$key" in
    -h|--help)

        >&2 echo "Start an experiment session"
        >&2 echo "--database|-d database.tar.bz2  -- Set up the db from this backup file."
        >&2 echo "--user|-u username              -- Output in this directory, default: unnamed."
        >&2 echo "--screenshots|-s                -- Do screenshots."
        >&2 echo "--clean_table|-c 1234567        -- Clean the db filestore of docker machine 1234567 (implies -n)"
        >&2 echo "--no_experiment|-n              -- Do the other action, but skip the experiment."

        exit 1
    ;;
    -d|--database)
        shift
        database="$1"
        shift
    ;;
    -c|--clean_table)
        shift
        docker_machine="$1"
        shift
    ;;
    -u|--user)
        shift
        user="$1"
        shift
    ;;
    -s|--screenshots)
        shift
        screenshots=''
    ;;
    -n|--no_experiment)
        shift
        no_experiment=''
    ;;
    *)
        >&2 echo "Ignored: "$1
        shift
    ;;
esac
done

if [[ -n ${docker_machine+x} ]] ;then
    no_experiment=''
fi

if [[ -n ${docker_machine+x} ]] && [[ -n ${database+x} ]] ;then
    >&2 echo "To the clean the table require the docker machine running."
    >&2 echo "To the restore the db requires the machine to be stopped."
    >&2 echo "Cannot do both!"
    exit 1
fi



if [[ -n ${database+x} ]] ;then
    echo "Copying db $database in the volume"
    if [ ! -f "$database" ] ;then
        >&2 echo "Database file is missing!"
        exit 1
    fi

    dbfpath="`readlink -n -e "$database"`"
    dbdir="`dirname "$dbfpath"`"
    dbfname="`basename "$dbfpath"`"

    docker run --rm -v odoo"$odoov"_odoo-db-data-odoo"$odoov":/volume -v "$dbdir":/backup alpine sh -c "find /volume -mindepth 1 -delete ; tar -C /volume/ -xjf /backup/$dbfname"

    echo "Done."
fi

if [[ -n ${docker_machine+x} ]] ;then
    echo "Cleaning table"
    docker exec "$docker_machine" /usr/bin/psql -U postgres -d odoo"$odoov" -c 'delete from ir_attachment;'
fi


if [[ -n ${no_experiment+x} ]] ;then
    echo "Experiment skipped as requested."
    exit 0
fi

if [[ -n ${screenshots+x} ]] ;then
    cd "$userdir"
    "$SCRIPTDIR"/screenshot.sh &
    ss=$!
    trap kill_screenshot EXIT INT TERM
fi

cd results
mkdir -p "$user"
userdir="`readlink -n -e "$user"`"

cd "$SCRIPTDIR"
docker-compose up --build

cd odoo/csvfolder

find  -type f  -iname '*.csv'  -size +63c  -exec cp -v '{}' "$userdir" ';'
rm *

if [$user != "unnamed"]
then
    python update_userid.py $userdir $user
fi