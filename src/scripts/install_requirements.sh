#!/bin/bash 

# cd where the script is located
cd "$(dirname "$0")"

# Install Python requirements
pip3 install -r ../aio/requirements-dev.txt
