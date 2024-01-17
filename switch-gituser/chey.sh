#!/bin/bash

# Set your GitHub username and email
USERNAME="CheyD24"
EMAIL="156814226+CheyD24@users.noreply.github.com"

# Configure git with the new credentials
git config user.name "$USERNAME"
git config user.email "$EMAIL"

echo "Git user has been set to: $USERNAME ($EMAIL)"