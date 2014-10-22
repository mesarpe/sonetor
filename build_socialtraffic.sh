#!/bin/bash

#first argument configuration file
#second argument trace file to generate

python traffic.py $1 | sort -k 1 -t ' ' -n > /tmp/traza;
python mobility.py $1 /tmp/traza > $2;

