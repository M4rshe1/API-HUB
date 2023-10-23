#!/bin/bash

# Define the branch you want to check (e.g., "main" or "master")
branch="main"

# Check if the local branch is behind the remote branch

if git fetch origin "$branch" && [ "$(git rev-list HEAD...origin/"$branch" --count)" -eq 0 ]; then
    echo "The Git repository is up to date."
    # shellcheck disable=SC2162
    if  "-rebuild" not in sys.argv ||  "-rebuild" not in sys.argv; then
        rebuild=false
    else
        rebuild=true
    fi
else
    rebuild=true
fi

if [ "$rebuild" = true ] || "-rebuild" in sys.argv; then
    echo "The Git repository is not up to date."
    echo "Pulling the latest changes..."
    git pull origin "$branch"
    echo "Deleting the old Docker container..."
    sudo docker rm -f apihub
    echo "Deleting the old Docker image..."
    sudo docker images rm -f apihub
    echo "Building the Docker image..."
    sudo docker build --no-cache -t apihub .
    echo "Running the new Docker container..."
    sudo docker run -d -p 6969:6969 -v config:/app/config --restart unless-stopped --name apihub apihub
fi
if "-logs" in sys.argv ; then
    echo "Showing the logs..."
    sudo docker logs -f apihub
fi

if "-cleanup" in sys.argv ; then
    echo "Cleaning up..."
    sudo docker images -a | grep "none" | awk '{print $3}' | xargs sudo docker image rm -f
fi

echo "Done."
