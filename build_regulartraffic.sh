#!/bin/bash

#first argument configuration file
# second argument trace file to generate

python traffic.py $1 | sort -k 1 -t ' ' -n > /tmp/traza;
python complete_client_server_traces.py $1 /tmp/traza > /tmp/traza_header;
cat /data/traza_header /tmp/traza > /tmp/traza2;
python mobility.py $1 /tmp/traza2 > $2;
