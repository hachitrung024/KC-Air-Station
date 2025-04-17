#!/bin/bash

if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "didn't find virtualenv! run setup.sh before."
    exit 1
fi

python3 app/main.py
