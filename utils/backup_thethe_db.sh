#!/bin/bash
# https://jeromejaglale.com/doc/programming/mongodb_docker_mongodump_mongorestore

if [ "$1" == "" ]; then
    echo "Usage: $0 <name_of_mongodb_container>"
    exit 1
fi

docker exec $1 sh -c 'mongodump --username root  --password root --authenticationDatabase admin --archive' > db.dump
gzip -c db.dump > db.dump.gz
rm db.dump
