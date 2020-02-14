#!/bin/bash
# https://jeromejaglale.com/doc/programming/mongodb_docker_mongodump_mongorestore

echo "Doing database backup..."
docker exec thethe_mongo sh -c 'mongodump --username root  --password root --authenticationDatabase admin --archive' > db.dump
gzip -c db.dump > db.dump.gz
rm db.dump
