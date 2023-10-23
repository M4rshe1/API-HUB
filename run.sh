#!/bin/bash

# Define the branch you want to check (e.g., "main" or "master")
branch="main"

# Check if the local branch is behind the remote branch

if git fetch origin "$branch" && [ "$(git rev-list HEAD...origin/"$branch" --count)" -eq 0 ]; then
    echo "The Git repository is up to date."
    echo "Docker image will not be rebuilt."
    # shellcheck disable=SC2162
    if not [ "$1" = "-rebuild" ]; then
        read -p "Rebuild? (Y/N): " confirm
        if [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]]; then
            rebuild=true
        else
            rebuild=false
        fi
    else
        rebuild=true
    fi
else
    rebuild=true
fi

if [ "$rebuild" = true ] || [ "$1" = "-rebuild" ]; then
    echo "The Git repository is not up to date."
    echo "Pulling the latest changes..."
    git pull
    echo "Building the Docker image..."
    sudo docker build -t apihub .
    echo "Deleting the old Docker container..."
    sudo docker rm -f apihub
    echo "Running the new Docker container..."
    sudo docker run -d -p 6969:6969 -v config:/app/config --name apihub apihub
fi

echo "Done."