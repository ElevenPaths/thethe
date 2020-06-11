#!/bin/bash
# https://jeromejaglale.com/doc/programming/mongodb_docker_mongodump_mongorestore
set -e

echo "usage: ./restore_thethe_db.sh <mongo_user> <mongo_password>"
echo "Restoring database from backup..."
gzip -kd db.dump.gz
docker exec -i thethe_mongo sh -c "mongorestore --drop --username $1  --password $2 --authenticationDatabase admin --archive" <db.dump
rm db.dump
