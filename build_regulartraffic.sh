#!/bin/bash

#first argument configuration file
# second argument trace file to generate

python traffic.py $1 | sort -k 1 -t ' ' -n > /data/traza;
python complete_client_server_traces.py $1 /data/traza > /data/traza_header;
cat /data/traza_header /data/traza > /data/traza2;
python mobility.py $1 /data/traza2 > $2;
