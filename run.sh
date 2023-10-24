#!/bin/bash

# Define the branch you want to check (e.g., "main" or "master")
branch="main"

# Check if the local branch is behind the remote branch
rebuild=false
logs=false
cleanup=false

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
done


if git fetch origin "$branch" && [ "$(git rev-list HEAD...origin/"$branch" --count)" -eq 0 ]; then
    echo "The Git repository is up to date."
    # shellcheck disable=SC2162
    if ! "$rebuild"; then
        rebuild=true
    else
        echo "No rebuild required."
        rebuild=false
    fi

else
    rebuild=true
fi

if $rebuild; then
    echo "The Git repository is not up to date."
    echo "Pulling the latest changes..."
    git pull origin "$branch"
    echo "Deleting the old Docker container..."
    sudo docker rm -f apihub
    echo "Deleting the old Docker image..."
    sudo docker images rmi --force apihub
    echo "Building the Docker image..."
    sudo docker build --no-cache -t apihub .
    echo "Running the new Docker container..."
    sudo docker run -d -p 6969:6969 --restart unless-stopped --name apihub apihub
#    sudo docker run -d -p 6969:6969 -v config.json:/app/config.json --restart unless-stopped --name apihub apihub
fi
if $cleanup; then
    echo "Cleaning up..."
    sudo docker images -a | grep "none" | awk '{print $3}' | xargs sudo docker image rm -f
fi
if $logs ; then
    echo "Showing the logs..."
    sudo docker logs -f apihub
fi


echo "Done."
