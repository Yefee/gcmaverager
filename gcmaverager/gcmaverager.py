import os
import sys
from functools import partial
from multiprocessing import Pool

import numpy as np
import xarray as xr


def getFilelist(rootDir):
    fileList = []
    list_dirs = os.walk(rootDir)
    for root, dirs, files in list_dirs:
        for f in files:
            fileList.append(os.path.join(root, f))
    return fileList


def _compMean(file, tarDir, prefix, suffix, method):

    if sys.version_info[0] < 3:
        if isinstance(file, basestring):
            ds = xr.open_dataset(file, decode_times=False)
        elif isinstance(file, xr.Dataset) or isinstance(file, xr.DataArray):
            ds = file
        else:
            raise ValueError("The file is not supported!")
    else:
        if isinstance(file, str):
            ds = xr.open_dataset(file, decode_times=False)
        elif isinstance(file, xr.Dataset) or isinstance(file, xr.DataArray):
            ds = file
        else:
            raise ValueError("The file is not supported!")

    # month index
    jan = np.arange(0, len(ds.time), 12)
    feb = np.arange(1, len(ds.time), 12)
    mar = np.arange(2, len(ds.time), 12)
    apr = np.arange(3, len(ds.time), 12)
    may = np.arange(4, len(ds.time), 12)
    jun = np.arange(5, len(ds.time), 12)
    jul = np.arange(6, len(ds.time), 12)
    aug = np.arange(7, len(ds.time), 12)
    sep = np.arange(8, len(ds.time), 12)
    oct = np.arange(9, len(ds.time), 12)
    nov = np.arange(10, len(ds.time), 12)
    dec = np.arange(11, len(ds.time), 12)

    # combine as seasonal index
    mam = np.hstack((mar, apr, may))
    mam.sort()

    jja = np.hstack((jun, jul, aug))
    jja.sort()

    son = np.hstack((sep, oct, nov))
    son.sort()

    djf = np.hstack((dec, jan, feb))
    djf.sort()

    # write out as TS file
    if "TS" in method and isinstance(ds, xr.DataArray):
        ds.to_netcdf(tarDir + prefix + '.' + ds.name + '.' + suffix + '.nc')


    # define time coordinate used for compute mean
    ds = ds.assign_coords(time_cp=ds.time)
    ds = ds.swap_dims({"time": "time_cp"})
    ds = ds.reset_coords('time')

    # get var list for dataset
    varList = ds.variables.keys()
    varList = [v for v in varList if "time_cp" in ds[
        v].dims and len(ds[v].dims) > 2]

    for var in varList:

        if any(name in ['decadal-ANN', 'decadal-MAM', 'decadal-SON', 'decadal-JJA', 'decadal-DJF'] for name in method):

            time = np.arange(0, len(ds.time_cp) / 120., 1).repeat(120)
            ds['time_cp'] = time[0:len(ds.time_cp)]
            time = ds.time.groupby('time_cp').mean('time_cp')
            time.values = np.round(time.values)
            time.attrs = ds.time.attrs

        if "decadal-ANN" in method:
            ann_decadal_mean = ds[var].groupby('time_cp').mean('time_cp')
            ann_decadal_mean = ann_decadal_mean.assign_coords(time=time)
            ann_decadal_mean = ann_decadal_mean.swap_dims({'time_cp': 'time'})
            ann_decadal_mean = ann_decadal_mean.drop('time_cp')
            ann_decadal_mean.attrs = ds[var].attrs
            ann_decadal_mean.to_netcdf(
                tarDir + prefix + '.' + var + '.' + suffix + '.DECADAL.ANN.nc')

        if "decadal-MAM" in method:
            mam_decadal_mean = ds[var].isel(
                time_cp=mam).groupby('time_cp').mean('time_cp')
            mam_decadal_mean = mam_decadal_mean.assign_coords(time=time)
            mam_decadal_mean = mam_decadal_mean.swap_dims({'time_cp': 'time'})
            mam_decadal_mean = mam_decadal_mean.drop('time_cp')
            mam_decadal_mean.attrs = ds[var].attrs
            mam_decadal_mean.to_netcdf(
                tarDir + prefix + '.' + var + '.' + suffix + '.DECADAL.MAM.nc')

        if "decadal-JJA" in method:
            jja_decadal_mean = ds[var].isel(
                time_cp=jja).groupby('time_cp').mean('time_cp')
            jja_decadal_mean = jja_decadal_mean.assign_coords(time=time)
            jja_decadal_mean = jja_decadal_mean.swap_dims({'time_cp': 'time'})
            jja_decadal_mean = jja_decadal_mean.drop('time_cp')
            jja_decadal_mean.attrs = ds[var].attrs
            jja_decadal_mean.to_netcdf(
                tarDir + prefix + '.' + var + '.' + suffix + '.DECADAL.JJA.nc')

        if "decadal-SON" in method:
            son_decadal_mean = ds[var].isel(
                time_cp=son).groupby('time_cp').mean('time_cp')
            son_decadal_mean = son_decadal_mean.assign_coords(time=time)
            son_decadal_mean = son_decadal_mean.swap_dims({'time_cp': 'time'})
            son_decadal_mean = son_decadal_mean.drop('time_cp')
            son_decadal_mean.attrs = ds[var].attrs
            son_decadal_mean.to_netcdf(
                tarDir + prefix + '.' + var + '.' + suffix + '.DECADAL.SON.nc')

        if "decadal-DJF" in method:
            djf_decadal_mean = ds[var].isel(
                time_cp=djf).groupby('time_cp').mean('time_cp')
            djf_decadal_mean = djf_decadal_mean.assign_coords(time=time)
            djf_decadal_mean = djf_decadal_mean.swap_dims({'time_cp': 'time'})
            djf_decadal_mean = djf_decadal_mean.drop('time_cp')
            djf_decadal_mean.attrs = ds[var].attrs
            djf_decadal_mean.to_netcdf(
                tarDir + prefix + '.' + var + '.' + suffix + '.DECADAL.DJF.nc')

        if any(name in ['ANN', 'MAM', 'SON', 'JJA', 'DJF'] for name in method):

            time = np.arange(0, len(ds.time_cp) / 12., 1).repeat(12)
            ds['time_cp'] = time[0:len(ds.time_cp)]
            time = ds.time.groupby('time_cp').mean('time_cp')
            time.values = np.round(time.values)
            time.attrs = ds.time.attrs
        # write out, prefix is used to indentify the filename
        if "ANN" in method:
            ann_mean = ds[var].groupby('time_cp').mean('time_cp')
            ann_mean = ann_mean.assign_coords(time=time)
            ann_mean = ann_mean.swap_dims({'time_cp': 'time'})
            ann_mean = ann_mean.drop('time_cp')
            ann_mean.attrs = ds[var].attrs
            ann_mean.to_netcdf(tarDir + prefix + '.' + var + '.' + suffix + '.ANN.MAM.nc')

        if "MAM" in method:
            mam_mean = ds[var].isel(time_cp=mam).groupby(
                'time_cp').mean('time_cp')
            mam_mean = mam_mean.assign_coords(time=time)
            mam_mean = mam_mean.swap_dims({'time_cp': 'time'})
            mam_mean = mam_mean.drop('time_cp')
            mam_mean.attrs = ds[var].attrs
            mam_mean.to_netcdf(tarDir + prefix + '.' +
                               var + '.' +suffix + '.ANN.MAM.nc')

        if "JJA" in method:
            jja_mean = ds[var].isel(time_cp=jja).groupby(
                'time_cp').mean('time_cp')
            jja_mean = jja_mean.assign_coords(time=time)
            jja_mean = jja_mean.swap_dims({'time_cp': 'time'})
            jja_mean = jja_mean.drop('time_cp')
            jja_mean.attrs = ds[var].attrs
            jja_mean.to_netcdf(tarDir + prefix + '.' +
                               var + '.' +suffix + '.ANN.JJA.nc')

        if "SON" in method:
            son_mean = ds[var].isel(time_cp=son).groupby(
                'time_cp').mean('time_cp')
            son_mean = son_mean.assign_coords(time=time)
            son_mean = son_mean.swap_dims({'time_cp': 'time'})
            son_mean = son_mean.drop('time_cp')
            son_mean.attrs = ds[var].attrs
            son_mean.to_netcdf(tarDir + prefix + '.' +
                               var + '.' +suffix + '.ANN.SON.nc')

        if "DJF" in method:
            djf_mean = ds[var].isel(time_cp=djf).groupby(
                'time_cp').mean('time_cp')
            djf_mean = djf_mean.assign_coords(time=time)
            djf_mean = djf_mean.swap_dims({'time_cp': 'time'})
            djf_mean = djf_mean.drop('time_cp')
            djf_mean.attrs = ds[var].attrs
            djf_mean.to_netcdf(tarDir + prefix + '.' +
                               var + '.' +suffix + '.ANN.DJF.nc')




def averager(file, tarDir, prefix, suffix, method):

    # if python.version <3: time slice file are not supported!
    if sys.version_info[0] < 3 and (isinstance(file, xr.DataArray) or isinstance(file, xr.Dataset)):
        raise "xrarray object shall use Python 3.3+"
        sys.exit(-1)

    computeMean = partial(_compMean, tarDir=tarDir,
                          prefix=prefix, suffix=suffix, method=method)
    pool = Pool()
    pool.map(computeMean, file)
    pool.close()
    pool.join()

if __name__ == "__main__":
    # rootDir = '/Volumes/Chengfei_Data_Center/iTrace/test_ts/'
    # tarDir = '/Volumes/Chengfei_Data_Center/iTrace/output/'
    # prefix = 'b.123.test'
    # method = ['decadal-ANN', 'decadal-MAM']
    # fl = getFilelist(rootDir)
    # fl = [l for l in fl if '.nc' in l]

    # averager(fl, tarDir, method)

    rootDir = '/Volumes/Chengfei_Data_Center/iTrace/test/'
    tarDir = '/Volumes/Chengfei_Data_Center/iTrace/output/'
    prefix = 'b.123.test'
    suffix = 'time_bound'
    method = ['decadal-ANN']

    fl = getFilelist(rootDir)
    ds = xr.open_mfdataset(fl[0:12], decode_times=False)

    varList = ds.variables.keys()
    varList = [v for v in varList if "time" in ds[
        v].dims and len(ds[v].dims) > 2]

    fl = [ds[var] for var in varList]
    averager(fl, tarDir, prefix, suffix,  method)
