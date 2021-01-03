#!/bin/bash 

# This file is intended for developer usage
# please install the development Python dependencies
# at requirements.dev.txt first

# cd where the script is located, one folder above
cd "$(dirname "$0")"/..

# Dump the stuff installed to a file
pip-chill > aio/requirements-dev.txt
pip-chill > aio/requirements.txt

# Remove pip-chill dependency for end user
sed -i '/^pip-chill/d' aio/requirements.txt