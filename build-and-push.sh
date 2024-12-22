#!/bin/bash

# Variables
USERNAME="gabidelcea"
REPO="my-flask-app"
TAG="latest"

# Log in to Docker Hub
echo "Logging into Docker Hub..."
docker login -u $USERNAME

# Build the Docker image
echo "Building Docker image..."
docker build -t $USERNAME/$REPO:$TAG .

# Push the image to Docker Hub
echo "Pushing Docker image to Docker Hub..."
docker push $USERNAME/$REPO:$TAG

echo "Done!"
