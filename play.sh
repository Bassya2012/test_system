#!/bin/bash

cd test_system

if [[ ! -d "env" ]]; then
    python3 -m venv env
fi
source ./env/bin/activate

pip install -r requirements.txt

python3 main_flaskapi.py
