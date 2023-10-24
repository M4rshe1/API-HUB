#!/bin/bash

# Define the branch you want to check (e.g., "main" or "master")
branch="main"

# Check if the local branch is behind the remote branch
rebuild=false
logs=false
cleanup=false
pull=false
restart=false
drop=false

for arg in "$@"; do
    # Check if the current argument is equal to the target string
    if [ "$arg" = "-rebuild" ]; then
        rebuild=true
    fi
    if [ "$arg" = "-logs" ]; then
        logs=true
    fi
    if [ "$arg" = "-cleanup" ]; then
        cleanup=true
    fi
    if [ "$arg" = "-pull" ]; then
        pull=true
    fi
    if [ "$arg" = "-restart" ]; then
        restart=true
    fi
    if [ "$arg" = "-drop" ]; then
        drop=true
    fi
done

if $drop -eq true; then
    echo "Drop unversioned files..."
    git clean -f -d
    echo "Drop umcommited changes..."
    git reset --hard
fi


if [ "$(git rev-list HEAD...origin/"$branch" --count)" -eq 0 ]; then
    echo "The Git repository is up to date."
    # shellcheck disable=SC2162
    rebuild=true
else
    echo "The Git repository is not up to date."
    rebuild=true
fi

if $rebuild -eq true; then
    if $pull -eq true; then
        echo "Pulling the latest changes..."
        git pull origin "$branch"
    fi
    echo "Deleting the old Docker container..."
    sudo docker rm -f apihub
    echo "Deleting the old Docker image..."
    sudo docker images rmi --force apihub
    echo "Building the Docker image..."
    sudo docker build --no-cache -t apihub .
    echo "Running the new Docker container..."
#    sudo docker run -d -p 6969:6969 --restart unless-stopped --name apihub apihub
    mkdir -p "${PWD}"/docker_conf
    cp "${PWD}"/config.json "${PWD}"/docker_conf/config.json
    sudo docker-compose up -d
#    sudo docker run -d -p 6969:6969 -v "${PWD}"/docker_conf/config.json:/app/config.json --restart unless-stopped --name apihub apihub
fi

if $restart -eq true; then
    echo "Restarting the Docker container..."
    sudo docker restart apihub
fi


if $cleanup -eq true; then
    echo "Cleaning up..."
    sudo docker images -a | grep "none" | awk '{print $3}' | xargs sudo docker image rm -f
fi
if $logs -eq true; then
    echo "Showing the logs..."
    sudo docker logs -f apihub
fi


echo "Done."
