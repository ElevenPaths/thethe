#!/bin/bash
# https://jeromejaglale.com/doc/programming/mongodb_docker_mongodump_mongorestore
set -e

echo "usage: ./backup_thethe_db.sh <mongo_user> <mongo_password>"
echo "Doing database backup..."
docker exec thethe_mongo sh -c "mongodump --username $1  --password $2 --authenticationDatabase admin --archive" >db.dump
gzip -c db.dump >db.dump.gz
rm db.dump
