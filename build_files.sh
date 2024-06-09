#!/bin/bash

# Update package lists
apt-get update

# Install Python and pip
apt-get install -y python3 python3-pip

# Install project dependencies
pip3 install -r requirements.txt

# Continue with the rest of your build process
echo "Build process completed"
