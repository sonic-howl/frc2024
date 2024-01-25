#!/bin/bash

# Set your GitHub username and email
USERNAME="kieran"
EMAIL="94074490+ColonelGuitar82@users.noreply.github.com"

# Configure git with the new credentials
git config user.name "$USERNAME"
git config user.email "$EMAIL"

echo "Git user has been set to: $USERNAME ($EMAIL)"