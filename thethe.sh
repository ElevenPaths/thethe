#!/bin/bash

# TheTHE: The Threat Hunting Environment
# (c) 2019-2020 (https://thethe.e-paths.com)
#
# Install, Run and Update TheTHE
#
# Install with this command (from your Linux machine):
#
# curl -sSL https://install.thethe.e-paths.com | bash
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

echo "                                                                  "
echo "                                                                  "
echo " _________  ___  ___  _______  _________  ___  ___  _______       "
echo "|\___   ___\\  \|\  \|\  ___ \|\___   ___\\  \|\  \|\  ___ \      "
echo "\|___ \  \_\ \  \\\  \ \   __/\|___ \  \_\ \  \\\  \ \   __/|     "
echo "     \ \  \ \ \   __  \ \  \_|/__  \ \  \ \ \   __  \ \  \_|/__   "
echo "      \ \  \ \ \  \ \  \ \  \_|\ \  \ \  \ \ \  \ \  \ \  \_|\ \  "
echo "       \ \__\ \ \__\ \__\ \_______\  \ \__\ \ \__\ \__\ \_______\ "
echo "        \|__|  \|__|\|__|\|_______|   \|__|  \|__|\|__|\|_______| "
echo "                                                                  "
echo "                                                                  "
echo "                                                                  "
echo -e "${Blue}Welcome to The Threat Hunting Environment ${Color_Off} "
echo "                                                                  "

KEY_NAME=thethe
CERTS_PATH=./

function generate_certs() {
    read -r -p "[?] Do you want to create a new auto-signed certificate? [y/N]" response
    echo
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
        openssl req -new -nodes -keyout ${CERTS_PATH}${KEY_NAME}.key -out ${CERTS_PATH}${KEY_NAME}.csr -days 3650 -subj "/C=$country/ST=$state/L=$locality/O=$organization"
        echo "${Green}[+] Created ${CERTS_PATH}${KEY_NAME}.key"
        echo "${Green}[+] Created ${CERTS_PATH}${KEY_NAME}.csr"

        #Self sign csr
        openssl x509 -req -days 365 -in ${CERTS_PATH}${KEY_NAME}.csr -signkey ${CERTS_PATH}${KEY_NAME}.key -out ${CERTS_PATH}${KEY_NAME}.crt
        echo -e "${Green}[+] Created ${CERTS_PATH}${KEY_NAME}.crt (self-signed)${Color_Off}"

        # Remove csr
        rm ${CERTS_PATH}${KEY_NAME}.csr

        # Move certs
        mv ${CERTS_PATH}${KEY_NAME}.key ./external/certs
        mv ${CERTS_PATH}${KEY_NAME}.crt ./external/certs

        echo -e "${BGreen}[*] Self-signed certificate created.${Color_Off}"

    else
        "${Yellow} [?] Remember: YOU SHOULD PUT YOUR OWN ${BYellow}thethe.key${Color_Off} and ${BYellow}thethe.crt{$Color_Off} ${Yellow} in ${BYellow}external/certs/${Color_Off} ${Yellow}path or thethe server WON'T WORK.${Color_Off}"
    fi
}

function check_certs() {
    CERT_CRT=./external/certs/thethe.crt
    if [ -f "$CERT_CRT" ]; then
        echo "${Green}[+] Good. $CERT_CRT exists.${Color_Off}"
    else
        echo "${Yellow}[?] $CERT_CRT is missing. Generating certificate and key...${Color_Off}"
        generate_certs
        return false
    fi

    CERT_KEY=./external/certs/thethe.key
    if [ -f "$CERT_KEY" ]; then
        echo "${Green}[+] Good. $CERT_KEY exists.${Color_Off}"
    else
        echo "${Yellow}[?] $CERT_KEY is missing. Generating certificate and key...${Color_Off}"
        generate_certs
        return false
    fi

    return true
}

function set_secret() {
    secret=$(openssl rand -hex 64)
    echo
    echo -e "${Blue}[+] Generating secret...${Color_Off}"
    export THETHE_SECRET=$secret
}

function check_dependencies() {
    echo -e "${Blue}[+] Checking dependencies${Color_Off}"

    # docker
    which docker >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        docker --version | grep "Docker version" >/dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo -e "${Green}[+] Docker is installed. Good.${Color_Off}"
        else
            echo -e "${Red}[!] Missing docker installation. Bad.${Color_Off}"
            echo "https://docs.docker.com/install/"
            exit
        fi
    else
        echo -e "${Red}[!] Missing docker installation. Bad.${Color_Off}"
        echo "https://docs.docker.com/install/"
        exit
    fi

    # docker-compose
    which docker-compose >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        docker-compose --version | grep "docker-compose version" >/dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo -e "${Green}[+] docker-compose is installed. Good.${Color_Off}"
        else
            echo -e "${Red}[!] Missing docker-compose installation. Bad.${Color_Off}"
            echo "https://docs.docker.com/compose/install/"
            exit
        fi
    else
        echo -e "${Red}[!] Missing docker-compose installation. Bad.${Color_Off}"
        echo "https://docs.docker.com/compose/install/"
        exit
    fi

    # openssl
    which openssl >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        openssl version | grep -i "ssl" >/dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo -e "${Green}[+] openssl is installed. Good.${Color_Off}"
        else
            echo -e "${Yellow}[?] Missing openssl installation. We won't be able to generate certificates.${Color_Off}"
        fi
    else
        echo -e "${Yellow}[?] Missing openssl installation. We won't be able to generate certificates.${Color_Off}"
    fi

    # git
    which git >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        git --version | grep -i "git version" >/dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo -e "${Green}[+] git is installed. Good.${Color_Off}"
        else
            echo -e "${Red}[!] Missing git installation.${Color_Off}"
            exit
        fi
    else
        echo -e "${Red}[!] Missing git installation.${Color_Off}"
        exit
    fi
}

# Main
PS3='Enter your choice: '
options=("Install" "Run" "Update" "Quit")
select opt in "${options[@]}"; do
    case $opt in
    "Install")
        echo -e "${BBlue}[+] Installing thethe.${Color_Off}"

        check_dependencies
        echo -e "${BGreen}[*] Dependencies checked.${Color_Off}"

        if $(git rev-parse --is-inside-work-tree); then
            echo -e "${Red}[!] Aborting. This is a git repository. Should you mean ${BRed}Update?${Color_Off}"
            exit
        fi

        echo -e "${Green}[+] Cloning repository thethe from https://github.com/ElevenPaths/thethe...${Color_Off}"
        git clone --depth=1 https://github.com/ElevenPaths/thethe >/dev/null 2>&1

        echo -e "${Green}[+] Entering repository${Color_Off}"
        cd thethe

        set_secret
        check_certs

        echo -e "${Blue}[+] Building docker images. It will take a while.${Color_Off}"
        docker-compose build >/dev/null 2>&1

        echo -e "${BGreen}[*] Installation completed.${Color_Off}"

        read -sp "[?] Do you want to start thethe now? [y/n]: " stop
        until [[ "$start" =~ ^[yYnN]*$ ]]; do
            echo "$start: invalid selection."
            read -sp "[?] Do you want to start thethe now? [y/n]: " start
        done
        if [[ "$start" =~ ^[yY]$ ]]; then
            docker-compose up -d >/dev/null 2>&1
            echo -e "${BGreen}[*] Done. You should see thethe running.${Color_Off}"
        else
            echo -e "${Green}Adios.${Color_Off}"
        fi

        break
        ;;

    "Run")
        echo "you chose choice 2"
        break
        ;;

    "Update")
        echo "you chose choice $REPLY which is $opt"
        break
        ;;

    "Quit")
        echo
        echo -e "${Green}Good bye${Color_Off}"
        exit
        ;;

    *) echo "invalid option $REPLY" ;;
    esac
done

# Detect docker installation
which docker >/dev/null 2>&1
if [ $? -eq 0 ]; then
    docker --version | grep "Docker version" >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        # Detect docker container (already running)
        thethe_server_container="$(docker ps -q --filter "name=thethe_server")"
        if [[ $thethe_server_container != "" ]]; then
            echo "thethe is already running..."
            read -p "Do you want to stop thethe now? [y/N]: " stop
            until [[ "$stop" =~ ^[yYnN]*$ ]]; do
                echo "$stop: invalid selection."
                read -p "Do you want to stop thethe now? [y/N]: " stop
            done
            if [[ "$stop" =~ ^[yY]$ ]]; then
                docker-compose down
                echo "Done!"
            else
                echo "Aborted!"
            fi
            echo
            echo "If you want to see more options, just run this script again!"
            exit
        fi

        # Detect docker image (already installed)
        thethe_server_image="$(docker images -q thethe_server)"
        if [[ $thethe_server_image != "" ]]; then
            echo "thethe is installed but is not running..."
            read -p "Do you want to start thethe now? [y/N]: " start
            until [[ "$start" =~ ^[yYnN]*$ ]]; do
                echo "$start: invalid selection."
                read -p "Do you want to start thethe now? [y/N]: " start
            done
            if [[ "$start" =~ ^[yY]$ ]]; then
                docker-compose up -d
                echo "Done!"
            else
                echo "Aborted!"
            fi
            echo
            echo "If you want to see more options, just run this script again!"
            exit
        fi

        echo "Welcome to The Threat Hunting Environment installer!"
        echo
        echo "I need to ask you a few questions before starting setup."
        echo "You can use the default options and just press enter if you are ok with them."
        echo

        read -r -p "Do you want to create a new certificate? [y/N]" response
        echo

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
            openssl req -new -nodes -keyout ${CERTS_PATH}${KEY_NAME}.key -out ${CERTS_PATH}${KEY_NAME}.csr -days 3650 -subj "/C=$country/ST=$state/L=$locality/O=$organization"
            echo "Created ${CERTS_PATH}${KEY_NAME}.key"
            echo "Created ${CERTS_PATH}${KEY_NAME}.csr"

            #Self sign csr
            openssl x509 -req -days 365 -in ${CERTS_PATH}${KEY_NAME}.csr -signkey ${CERTS_PATH}${KEY_NAME}.key -out ${CERTS_PATH}${KEY_NAME}.crt
            echo "Created ${CERTS_PATH}${KEY_NAME}.crt (self-signed)"

            # Remove csr
            rm ${CERTS_PATH}${KEY_NAME}.csr
        else
            echo "You can put your own certificate on certs path"
        fi

        # Start the thethe docker service
        # docker-compose up -d
        echo
        echo "Finished!"
        echo
        echo "If you want to see more options, just run this script again!"
    else
        echo "Docker not found"
        echo "You need Docker to run thethe"
        echo "Check that you have a docker installed and try again"
        exit
    fi
fi
