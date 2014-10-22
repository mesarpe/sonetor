Description
-----------


Installation
------------

setuptools - from Git repository

```bash
> apt-get install python-networkx python-scipy python-numpy
> git clone git://github.com/panisson/pymobility.git
> cd pymobility
> python setup.py install (run as admin/root)
> cd ..
> wget http://webloria.loria.fr/~bernardc/sonetor/src.tar.gz
> tar -xvzf
> cd sonetor
```

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
