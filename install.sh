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
echo -e "${Blue}Welcome to The Threat Hunting Environment Installer${Color_Off} "
echo "                                                                  "

function check_dependencies() {
    echo -e "${Green}[+] Checking dependencies.${Color_Off}"

    # docker
    if command -v docker >/dev/null 2>&1; then
        echo -e "${Green}[+] Docker is installed. Good.${Color_Off}"
    else
        echo -e "${Red}[!] Missing docker installation. Bad.${Color_Off}"
        echo "See there how to get docker: https://docs.docker.com/install/"
        exit 1
    fi

    # docker-compose
    if command -v docker-compose >/dev/null 2>&1; then
        echo -e "${Green}[+] docker-compose is installed. Good.${Color_Off}"
    else
        echo -e "${Red}[!] Missing docker-compose installation. Bad.${Color_Off}"
        echo "See there how to get docker-compose: https://docs.docker.com/compose/install/"
        exit 1
    fi

    # git
    if command -v git >/dev/null 2>&1; then
        echo -e "${Green}[+] git is installed. Good.${Color_Off}"
    else
        echo -e "${Red}[!] Missing git installation.${Color_Off}"
        exit 1
    fi
}

# Main

echo -e "${Green}[+] Installing thethe.${Color_Off}"

check_dependencies
echo -e "${BGreen}[*] Dependencies checked.${Color_Off}"

if git rev-parse >/dev/null 2>&1; then
    echo -e "${Red}[!] Aborting. This is a git repository. Did you mean ${BRed}update.sh?${Color_Off}"
    exit 1
fi

echo -e "${Green}[+] Cloning repository thethe from https://github.com/ElevenPaths/thethe...${Color_Off}"
git clone --depth=1 https://github.com/ElevenPaths/thethe >/dev/null 2>&1

echo -e "${Green}[+] Entering repository${Color_Off}"
cd thethe

set_secret
source certs.sh

echo -e "${Green}[+] Building docker images. It will take a while.${Color_Off}"
docker-compose build

echo -e "${BGreen}[*] Installation completed.${Color_Off}"
echo -e "${Blue}Run start.sh if you want to launch thethe.${Color_Off}"
