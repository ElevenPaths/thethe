#!/bin/bash
# https://jeromejaglale.com/doc/programming/mongodb_docker_mongodump_mongorestore

echo "Restoring database from backup..."
gzip -kd db.dump.gz
docker exec -i thethe_mongo sh -c 'mongorestore --drop --username root  --password root --authenticationDatabase admin --archive' < db.dump
rm db.dump
