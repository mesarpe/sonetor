Description
-----------


Installation
------------

In order to install SONETOR, you have two options.
Either to install it using virtualenv, either without it.

setuptools - from Git repository

Without virtualenv:
```bash
> apt-get install git
> apt-get install python-dev
> apt-get install python-networkx python-scipy python-numpy python-pyparsing
> git clone https://github.com/panisson/pymobility.git
> cd pymobility
> python setup.py install
> cd ..
> git clone https://github.com/mesarpe/sonetor
> cd sonetor
```


With virtualenv:
```bash
> apt-get install git
> apt-get install python-dev
> apt-get install python-virtualenv
> apt-get install python-networkx python-scipy python-numpy
> virtualenv .
> source bin/activate
> easy_install numpy scipy pyparsing networkx
> git clone https://github.com/panisson/pymobility.git
> cd pymobility
> python setup.py install
> cd ..
> git clone https://github.com/mesarpe/sonetor
> cd sonetor
```

Creating the first trace file:

```bash
> build_regulartraffic.sh examples/example.ini /tmp/trace123
```

NOTE: if you still have problems, just let me know.

Dependencies
------------
NumPy, SciPy, Networkx and PyMobility

Examples
--------
#create new trace
python traffic.py examples/example.ini | sort -k 1 -t ' ' -n > /tmp/traza;

#add mobility
python mobility.py examples/example.ini /tmp/traza > /tmp/traza2;


Regular Traffic traces (build_regulartraffic.sh [configuration_file] [output_trace_file]:

python traffic.py examples/regulartraffic.ini | sort -k 1 -t ' ' -n > /tmp/traza;
python complete_client_server_traces.py examples/regulartraffic.ini > /tmp/traza_header;
cat /tmp/traza_header /tmp/traza > /tmp/traza2;
python mobility.py examples/example.ini /tmp/traza2 > /tmp/traza;

Generate regular traffic traces:

for alpha in 065 110 150 200; do for i in 1 2 3; do ./build_regulartraffic.sh examples/compare_caching/reg_106_$alpha\_waypoint.ini /data/caching/reg_106_$alpha\_waypoint.trace.$i; done; done

Contributing
------------
If you have a Github account please fork the repository,
create a topic branch, and commit your changes.
Then submit a pull request from that branch.

License
-------
Written by César Bernardini <mesarpe@gmail.com>  
Copyright (C) 2014 César Bernardini.
You can contact us by email (mesarpe@gmail.com).  



References
----------
[1] Cesar Bernardini, Thomas Silverston, Olivier Festor. SONETOR: a Social Network Traffic Generator. IEEE ICC 2014.
