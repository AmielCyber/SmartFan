#!/bin/bash

# Script to run the smart fan python script
# Will take an argument and pass it to the python script
SF_PATH = "~/Documents/SmartFan/smart_fan.py"

python3 $SF_PATH "$1"
