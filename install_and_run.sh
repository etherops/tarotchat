#!/bin/bash

# INSTALL
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# RUN
clear
set -x
python play.py --num-cards=1 --question="General reading"
