#!/bin/bash

# Set your GitHub username and email
USERNAME="Elyssa28"
EMAIL="156960263+Elyssa28@users.noreply.github.com"

# Configure git with the new credentials
git config user.name "$USERNAME"
git config user.email "$EMAIL"

echo "Git user has been set to: $USERNAME ($EMAIL)"