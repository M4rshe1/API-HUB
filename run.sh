#!/bin/bash

# Define the branch you want to check (e.g., "main" or "master")
branch="main"

# Check if the local branch is behind the remote branch

if git fetch origin "$branch" && [ "$(git rev-list HEAD...origin/"$branch" --count)" -eq 0 ]; then
    echo "The Git repository is up to date."
    echo "Docker image will not be rebuilt."
    # shellcheck disable=SC2162
    if not [ "$1" = "-rebuild" ] || not [ "$2" = "-rebuild" ]; then
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

if [ "$rebuild" = true ] || [ "$1" = "-rebuild" ] || [ "$2" = "-rebuild" ]; then
    echo "The Git repository is not up to date."
    echo "Pulling the latest changes..."
    git pull origin "$branch"
    sleep 5
    echo "Deleting the old Docker image..."
    sudo docker image rm -f apihub
    echo "Building the Docker image..."
    sudo docker build --no-cache -t apihub .
    echo "Deleting the old Docker container..."
    sudo docker rm -f apihub
    echo "Running the new Docker container..."
    sudo docker run -d -p 6969:6969 -v config:/app/config --restart unless-stopped --name apihub apihub
fi
if [ "$1" = "-logs" ] || [ "$2" = "-logs" ]; then
    echo "Showing the logs..."
    sudo docker logs -f apihub
fi

echo "Done."
