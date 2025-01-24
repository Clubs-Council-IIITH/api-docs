#!/bin/bash

# stop on error
set -e

# save current dir
CWD=$(basename $PWD)

STEP_COUNT=0

print_bold() {
    local bold_text="$1"
    local reset_format='\033[0m'
    local bold_format='\033[1m'

    let STEP_COUNT+=1
    printf "\nStep ${STEP_COUNT}: ${bold_format}${bold_text}${reset_format}\n\n"
}

# Repository URL
repo_url="git@github.com:Clubs-Council-IIITH/auth.git"

# Attempt to clone the repository
output=$(git clone "$repo_url" 2>&1)
exit_status=$?

# Check for the 404 error message
if echo "$output" | grep -q "404: Not Found"; then
    print_bold "You don't have permission to clone the repository. Ask for permissions or add ur local SSH key to github"
    exit 1
elif [ $exit_status -ne 0 ]; then
    print_bold "An error occurred while cloning the repository."
    echo "$output"
    exit 1
else
    rm -rf "$(basename "$repo_url" .git)"
fi

# Check if docker-compose is installed
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
elif command -v docker &> /dev/null && docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    print_bold "Error: Neither docker-compose nor docker compose is installed."
    exit 1
fi

print_bold "Using $DOCKER_COMPOSE"


print_bold "Cloning  the main repo and all of its submodules, this might take a mintute or two ..."

# check if services exists
if [ -d "./services" ]; then
  read -p 'services was found in the required location, do you want to update the existing (git pull) or reclone? [y/N]' input
    case ${input:0:1} in
	y|Y)
	    sudo rm -rf services
      git clone -j8 --recurse-submodules --remote-submodules git@github.com:Clubs-Council-IIITH/services.git services
	    ;;
	n|N|*)
      cd services
      git submodule foreach git pull origin master
	    ;;
    esac
else
    git clone -j8 --recurse-submodules --remote-submodules git@github.com:Clubs-Council-IIITH/services.git services
fi


if [ -d "./services" ]; then
    print_bold "Building docker images and docs, this might take serveral minutes the first time.."
    $DOCKER_COMPOSE -p api-docs -f ./docker-compose.yml up --build -d
fi
