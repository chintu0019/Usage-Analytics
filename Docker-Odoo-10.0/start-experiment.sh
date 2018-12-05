#!/bin/sh

echo "enter participant's name"
read name
mkdir ./odoo_logs/$name
echo "Folder created ./odoo_logs $name"
cd ./odoo_logs/$name
echo "Logging to file: odoo_$name.log"
docker-compose up >> ./odoo_logs/$name/odoo_$name.log