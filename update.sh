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
echo -e "${Blue}Welcome to The Threat Hunting Environment Updater${Color_Off} "
echo "                                                                  "

echo -e "${Blue}Updating repo and submodules{Color_Off}"
git pull --recurse-submodules

echo -e "${Blue}Stopping thethe containers{Color_Off}"
docker-compose stop

echo -e "${Blue}Updating images{Color_Off}"
docker-compose pull

echo -e "${Blue}Recreating images{Color_Off}"
docker-compose build
