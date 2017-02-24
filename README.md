# About GCMAverager

GCMAverger is a lightweight parallel post process package designed for large amount general circulation model(GCM) outputs.
It was originally designed to post process a long run from the community earth system model (CESM), who genreated hundreds of TBs data.
NCAR has developed two fancy tools: pyAverager and pyReshaper, which are do the samething as GAMAverager do, however, they are pooly maintained and not easy to use.

GCMAverager is a [xarray-based](https://github.com/pydata/xarray) project, therefore python 2.7+ and 3.x are supported.
Right now, GCMAverager primarily can 
* extract variables from time slice history files into time seris files;
* compute annual (decadal) and seasonal mean for model outputs from time slice or time series files. 



# Installation
### using github
```
git clone https://github.com/Yefee/gcmaverager.git
cd gcmaverager
python setup.py install
```

### using pip
```
pip install gcmaverager
```

# Get started
GCMAverager supports sereral kinds of average method:
* ANN (annual mean)
* MAM (March-April-May, annual mean) 
* JJA (June-July-August, annual mean) 
* SON (September-October-November, annual mean) 
* DJF (December-January-February, annual mean) 
* decadal-ANN (decadal annual mean)
* decadal-MAM (March-April-May, decadal annual mean) 
* decadal-SON (June-July-August, decadal annual mean) 
* decadal-JJA (September-October-November, decadal annual mean) 
* decadal-DJF (December-January-February, decadal annual mean) 

* TS (extract time series file from original GCM outputs)

### Extract time series file from time slice files
This featre only suppport Py 3.x.

```
    import gcmaverager as ga
    import xarray as xr

    rootDir = '/Volumes/Chengfei_Data_Center/iTrace/test/'
    tarDir = '/Volumes/Chengfei_Data_Center/iTrace/output/'
    prefix = 'test'
    suffix = '0001-0999'
    method = ['TS']

    # get file list and create an xarray object
    fl = ga.getFilelist(rootDir)
    ds = xr.open_mfdataset(fl, decode_times=False)

    # derive time dependent variables
    varList = ds.variables.keys()
    varList = [v for v in varList if "time" in ds[
        v].dims and len(ds[v].dims) > 2]

    # feed it to GAMAverager
    fl = [ds[var] for var in varList]
    ga.averager(fl, tarDir, prefix, suffix,  method)
```

The outputs are in tarDir, which has pattern prefix+variable+suffix+'.nc'(e.g. test.TEMP.0001-0999.nc)


### Compute average from time slice files
This featre only suppport Py 3.x.

```

    import gcmaverager as ga
    import xarray as xr

    rootDir = '/Volumes/Chengfei_Data_Center/iTrace/test/'
    tarDir = '/Volumes/Chengfei_Data_Center/iTrace/output/'
    prefix = 'test'
    suffix = '0001-0999'
    method = ['ANN', 'decadal-ANN']

    # get file list and create an xarray object
    fl = ga.getFilelist(rootDir)
    ds = xr.open_mfdataset(fl, decode_times=False)

    # derive time dependent variables
    varList = ds.variables.keys()
    varList = [v for v in varList if "time" in ds[
        v].dims and len(ds[v].dims) > 2]

    # feed it to GAMAverager
    fl = [ds[var] for var in varList]
    ga.averager(fl, tarDir, prefix, suffix,  method)

```
The outputs are in tarDir, which has pattern prefix+variable+suffix+'ANN.nc'(e.g. test.TEMP.0001-0999.ANN.nc)


### Compute average from time series files

```

    import gcmaverager as ga
    import xarray as xr

    rootDir = '/Volumes/Chengfei_Data_Center/iTrace/test/'
    tarDir = '/Volumes/Chengfei_Data_Center/iTrace/output/'
    prefix = 'test'
    suffix = '0001-0999'
    method = ['ANN', 'decadal-ANN']

    # get file list and create an xarray object
    fl = ga.getFilelist(rootDir)

    # feed it to GAMAverager
    ga.averager(fl, tarDir, prefix, suffix,  method)

```
