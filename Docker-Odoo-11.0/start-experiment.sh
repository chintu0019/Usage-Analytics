#!/bin/sh

echo "enter participant's name"
read name
if [ -d $DIRECTORY ]; then
    mkdir ./odoo_logs/$name
    echo "Folder created ./odoo_logs $name"
    echo "Logging to file: odoo_$name.log"
else 
    echo "Folder with the name $name exists"
    echo "Appending the logs to file: odoo_$name.log"
fi

systemctl start docker
docker-compose up >> ./odoo_logs/$name/odoo_$name.log