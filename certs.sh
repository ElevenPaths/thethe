set -e

# Reset
Color_Off='\033[0m' # Text Reset

# Regular Colors
Black='\033[0;30m'  # Black
Red='\033[0;31m'    # Red
Green='\033[0;32m'  # Green
Yellow='\033[0;33m' # Yellow
Blue='\033[0;34m'   # Blue
Purple='\033[0;35m' # Purple
Cyan='\033[0;36m'   # Cyan
White='\033[0;37m'  # White

# Bold
BBlack='\033[1;30m'  # Black
BRed='\033[1;31m'    # Red
BGreen='\033[1;32m'  # Green
BYellow='\033[1;33m' # Yellow
BBlue='\033[1;34m'   # Blue
BPurple='\033[1;35m' # Purple
BCyan='\033[1;36m'   # Cyan
BWhite='\033[1;37m'  # White

KEY_NAME=thethe
CERTS_PATH=./external/certs/

if [ -d "external/certs" ]; then
    echo -e "${Green}[+] Directory ${CERTS_PATH} exists, skipping.${Color_Off}"
else
    echo -e "${Green}[+] Creating ${CERTS_PATH}${Color_Off}"
    mkdir -p external/certs
fi

read -r -p "[?] Do you want to create a self-signed certificate? (skip if you will set your own cert later) [y/N] " response

# check openssl is there
if command -v openssl >/dev/null 2>&1; then
    echo -e "${Green}[+] openssl is installed. Good.${Color_Off}"
else
    echo -e "${Red}[-] Missing openssl installation. We won't be able to generate certificates.${Color_Off}"
    exit 1
fi

if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    read -p "Country Name (2 letter code) [ES]: " country
    country=${country:-ES}
    read -p "State or Province Name (full name) [Spain]: " state
    state=${state:-Spain}
    read -p "Locality Name (eg, city) [Malaga]: " locality
    locality=${locality:-Malaga}
    read -p "Organization Name (eg, company) [ElevenPaths]: " organization
    organization=${organization:-ElevenPaths}

    #Generate a key and csr
    openssl req -new -nodes -keyout ${CERTS_PATH}${KEY_NAME}.key -out ${CERTS_PATH}${KEY_NAME}.csr -days 3650 -subj "/C=$country/ST=$state/L=$locality/O=$organization" >/dev/null 2>&1
    echo -e "${Green}[+] Created ${CERTS_PATH}${KEY_NAME}.key${Color_Off}"
    echo -e "${Green}[+] Created ${CERTS_PATH}${KEY_NAME}.csr${Color_Off}"

    #Self sign csr
    openssl x509 -req -days 365 -in ${CERTS_PATH}${KEY_NAME}.csr -signkey ${CERTS_PATH}${KEY_NAME}.key -out ${CERTS_PATH}${KEY_NAME}.crt >/dev/null 2>&1
    echo -e "${Green}[+] Created ${CERTS_PATH}${KEY_NAME}.crt (self-signed)${Color_Off}"

    # Remove csr
    rm ${CERTS_PATH}${KEY_NAME}.csr

    echo -e "${BGreen}[*] Self-signed certificate created.${Color_Off}"

else
    echo -e "${Yellow}[!] Remember: YOU SHOULD PUT YOUR OWN CERT AND KEY IN external/certs OR thethe WON'T WORK"
fi
