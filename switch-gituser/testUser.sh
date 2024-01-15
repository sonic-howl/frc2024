#!/bin/bash

# Set your GitHub username and email
USERNAME="Username1"
EMAIL="email1@example.com"

# Configure git with the new credentials
git config --global user.name "$USERNAME"
git config --global user.email "$EMAIL"

echo "Git user has been set to: $USERNAME ($EMAIL)"