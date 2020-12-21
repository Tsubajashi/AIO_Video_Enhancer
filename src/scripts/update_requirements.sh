#!/bin/bash 

# This file is intended for developer usage

# cd where the script is located, one folder above
cd "$(dirname "$0")"/..

# Dump the stuff installed to a file
pip3 freeze > aio_enhancer/requirements.txt
