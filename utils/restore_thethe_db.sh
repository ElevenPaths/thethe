#!/bin/bash
# https://jeromejaglale.com/doc/programming/mongodb_docker_mongodump_mongorestore

if [ "$1" == "" ]; then
    echo "Usage: $0 <name_of_mongodb_container>"
    exit 1
fi

gzip -kd db.dump.gz
docker exec -i $1 sh -c 'mongorestore --drop --username root  --password root --authenticationDatabase admin --archive' < db.dump
rm db.dump