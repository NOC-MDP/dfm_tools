# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 15:20:06 2022

@author: veenstra
"""

import os
import xarray as xr
from dfm_tools.download import download_ERA5

basedir = '.'

# domain
longitude_min = -5 #-180
longitude_max = 6 #180
latitude_min = 45 #-90
latitude_max = 50 #90

#tstart and tstop as understood by pd.date_range with freq='MS' (month start)
tstart = '2021-01'
tstop = '2022-01'

# variables, supply arbitrary string to get error with available variable names
variables = ['v10n']

for varkey in variables:
    dir_output = os.path.join(basedir,varkey)
    if not os.path.isdir(dir_output):
        os.mkdir(dir_output)
    
    download_ERA5(varkey, tstart=tstart, tstop=tstop,
                  longitude_min=longitude_min, longitude_max=longitude_max, latitude_min=latitude_min, latitude_max=latitude_max,
                  dir_out=dir_output)

    #open mfdataset to check folder contents
    ds = xr.open_mfdataset(os.path.join(dir_output,f'era5_{varkey}_*.nc'))
    ds.close()

ds.v10n.isel(time=0).plot()