#!/bin/pwsh

echo "Building mage image..."
docker build -f mage.Dockerfile --no-cache -t mage .

echo "Building dashboard image..."
docker build -f dashboard.Dockerfile --no-cache -t dashboard .
