#!/bin/bash

# Set your GitHub username and email
USERNAME="BMorozov"
EMAIL=""

# Configure git with the new credentials
git config user.name "$USERNAME"
git config user.email "$EMAIL"

echo "Git user has been set to: $USERNAME ($EMAIL)"