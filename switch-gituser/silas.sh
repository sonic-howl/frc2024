#!/bin/bash

# Set your GitHub username and email
USERNAME="magnite5"
EMAIL="87040030+magnite5@users.noreply.github.com"

# Configure git with the new credentials
git config user.name "$USERNAME"
git config user.email "$EMAIL"

echo "Git user has been set to: $USERNAME ($EMAIL)"