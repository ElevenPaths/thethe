#!/bin/sh

KEY_NAME=thethe
CERTS_PATH=/etc/nginx/certificates/

mkdir -p ${CERTS_PATH}

#Change to your company details
country=ES
state=Spain
locality=Malaga
organization=elevenpaths.com

cd $CERTS_PATH

echo "Generating key request..."

#Generate a key and csr
openssl req -new -nodes -keyout ${CERTS_PATH}${KEY_NAME}.key -out ${CERTS_PATH}${KEY_NAME}.csr -days 3650 -subj "/C=$country/ST=$state/L=$locality/O=$organization"
echo "Created ${CERTS_PATH}${KEY_NAME}.key"
echo "Created ${CERTS_PATH}${KEY_NAME}.csr"

#Self sign csr
openssl x509 -req -days 365 -in ${CERTS_PATH}${KEY_NAME}.csr -signkey ${CERTS_PATH}${KEY_NAME}.key -out ${CERTS_PATH}${KEY_NAME}.crt
echo "Created ${CERTS_PATH}${KEY_NAME}.crt (self-signed)"

rm ${CERTS_PATH}${KEY_NAME}.csr