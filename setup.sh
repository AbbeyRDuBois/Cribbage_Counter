#!/usr/bin/env bash

# Find pip.
PIP=$(which pip3)

# Check if pip is installed.
if [ -z $PIP ]; then
    echo "pip3 is not installed. Please install pip3."
    exit 1
fi

# Install dependencies.
$PIP install -r requirements.txt