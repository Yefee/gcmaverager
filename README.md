# About GCMAverager

GCMAverger is a lightweight parallel post process package designed for large amount general circulation model(GCM) outputs.
It was originally designed to post process a long run from the community earth system model (CESM), who genreated hundreds of TBs data.
NCAR has developed two fancy tools: pyAverager and pyReshaper, which are do the samething as GAMAverager do, however, they are pooly maintained and not easy to use.
GCMAverager is a [xarray-based](https://github.com/pydata/xarray) project, and more features will be added in the future.
Right now, GCMAverager primarily can 
* extract variables from time slice history files into time seris files;
* compute annual (decadal) and seasonal mean for model outputs. 



# Installation
1. using github
```
git clone https://github.com/Yefee/gcmaverager.git
cd gcmaverager
python setup.py install
```

2. using pip
```

```

# Get started

