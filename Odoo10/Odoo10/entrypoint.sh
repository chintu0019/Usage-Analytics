#!/bin/bash
set -e

HOST_USER="${HOST_USER:=root}"
HOST_GROUP="${HOST_GROUP:=root}"

function reset_mode_bits {
    cd "/usr/lib/python2.7/dist-packages/odoo/csvfolder"
    chmod "$HOST_USER:$HOST_GROUP" *.csv
    cd -
    exit 0
}
trap reset_mode_bits TERM


cd /
if [ ! -e /usr/lib/python2.7/dist-packages/odoo/__init__.py ] ;then
    echo "Copying odoo code in the host"

    echo rsync --owner --group --chown="$HOST_USER":"$HOST_GROUP" -rtu --delete /usr/lib/python2.7/dist-packages/odoo.untouched/'*' "/usr/lib/python2.7/dist-packages/odoo.orig"
    rsync --owner --group --chown="$HOST_USER":"$HOST_GROUP" -rtu --delete /usr/lib/python2.7/dist-packages/odoo.untouched/* "/usr/lib/python2.7/dist-packages/odoo.orig"

    echo rsync --owner --group --chown="$HOST_USER":"$HOST_GROUP" -rtu --delete /usr/lib/python2.7/dist-packages/odoo.untouched/'*' "/usr/lib/python2.7/dist-packages/odoo"
    rsync --owner --group --chown="$HOST_USER":"$HOST_GROUP" -rtu --delete /usr/lib/python2.7/dist-packages/odoo.untouched/* "/usr/lib/python2.7/dist-packages/odoo"

    cd /usr/lib/python2.7/dist-packages
    patch -p0 <./analyzer.patch
    cd /
fi

# set the postgres database host, port, user and password according to the environment
# and pass them as arguments to the odoo process if not present in the config file
: ${HOST:=${DB_PORT_5432_TCP_ADDR:='db'}}
: ${PORT:=${DB_PORT_5432_TCP_PORT:=5432}}
: ${USER:=${DB_ENV_POSTGRES_USER:=${POSTGRES_USER:='odoo'}}}
: ${PASSWORD:=${DB_ENV_POSTGRES_PASSWORD:=${POSTGRES_PASSWORD:='odoo'}}}

DB_ARGS=()
function check_config() {
    param="$1"
    value="$2"
    if ! grep -q -E "^\s*\b${param}\b\s*=" "$ODOO_RC" ; then
        DB_ARGS+=("--${param}")
        DB_ARGS+=("${value}")
   fi;
}
check_config "db_host" "$HOST"
check_config "db_port" "$PORT"
check_config "db_user" "$USER"
check_config "db_password" "$PASSWORD"

case "$1" in
    -- | odoo)
        shift
        if [[ "$1" == "scaffold" ]] ; then
            odoo "$@"
        else
            odoo "$@" "${DB_ARGS[@]}"
        fi
        ;;
    -*)
        exec odoo "$@" "${DB_ARGS[@]}"
        ;;
    *)
        exec odoo "$@"
esac

exit 1
