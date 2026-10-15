#!/bin/bash

# Stop if any command fails
set -e

echo "Staging all changes..."
git add .

echo "Committing changes..."
git commit -m "Update Project"

echo "Pushing changes to GitHub..."
git push

echo "Successfully synced with GitHub!"
