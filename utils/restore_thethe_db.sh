#!/bin/bash
# https://jeromejaglale.com/doc/programming/mongodb_docker_mongodump_mongorestore

gzip -d db.dump.gz
docker exec -i thethe_mongo_1 sh -c 'mongorestore --username root  --password root --authenticationDatabase admin --archive' < db.dump