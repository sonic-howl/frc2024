#!/bin/bash

# Set your GitHub username and email
USERNAME="Sakthi19s"
EMAIL="157066523+Sakthi19s@users.noreply.github.com"

# Configure git with the new credentials
git config user.name "$USERNAME"
git config user.email "$EMAIL"

echo "Git user has been set to: $USERNAME ($EMAIL)"