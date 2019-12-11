#!/bin/bash
# https://jeromejaglale.com/doc/programming/mongodb_docker_mongodump_mongorestore

docker exec thethe_mongo_1 sh -c 'mongodump --username root  --password root --authenticationDatabase admin --archive' > db.dump
gzip -c db.dump > db.dump.gz
rm db.dump
