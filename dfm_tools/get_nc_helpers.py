# -*- coding: utf-8 -*-
"""
dfm_tools are post-processing tools for Delft3D FM
Copyright (C) 2020 Deltares. All rights reserved.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  if not, see <http://www.gnu.org/licenses/>.

All names, logos, and references to "Deltares" are registered trademarks of
Stichting Deltares and remain full property of Stichting Deltares at all times.
All rights reserved.


INFORMATION
This script is part of dfm_tools: https://github.com/openearth/dfm_tools
Check the README.rst on github for other available functions
Check the tests folder on github for example scripts (this is the dfm_tools pytest testbank)
Check the pptx and example figures in (created by the testbank): N:/Deltabox/Bulletin/veenstra/info dfm_tools

Created on Fri Feb 14 12:43:19 2020

@author: veenstra

helper functions for functions in get_nc.py
"""

import xarray as xr
import xugrid as xu
import pandas as pd


def get_ncvarproperties(data_xr):
    if not isinstance(data_xr,(xr.Dataset,xu.UgridDataset)):
        raise Exception('data_xr should be of type xr.Dataset or xu.UgridDataset')
    nc_varkeys = data_xr.variables.mapping.keys()
    
    list_varattrs_pd = []
    for varkey in nc_varkeys:
        varattrs_pd = pd.DataFrame({varkey:data_xr.variables.mapping[varkey].attrs}).T
        varattrs_pd[['shape','dimensions']] = 2*[''] #set dtype as str (float will raise an error when putting tuple in there)
        varattrs_pd.at[varkey,'shape'] = data_xr[varkey].shape
        varattrs_pd.at[varkey,'dimensions'] = data_xr.variables[varkey].dims
        varattrs_pd.loc[varkey,'dtype'] = data_xr.variables[varkey].dtype
        list_varattrs_pd.append(varattrs_pd)
    
    vars_pd = pd.concat(list_varattrs_pd,axis=0)
    vars_pd[vars_pd.isnull()] = '' #avoid nan values
    
    data_xr.close()

    return vars_pd


def get_varnamefromattrs(data_xr, varname):
    
    # check if requested variable is in netcdf
    varlist = list(data_xr.variables.keys())
    if varname in varlist:
        return varname
    
    #check if requested varname is in standard_name attrs of ncvars
    ds_stdname = data_xr.filter_by_attrs(standard_name=varname)
    varlist_stdname = list(ds_stdname.data_vars.keys())
    if len(varlist_stdname)==1:
        varname_matched = varlist_stdname[0]
        print(f'requested varname "{varname}" found in standard_name attribute of variable {varname_matched}')
        return varname_matched
    elif len(varlist_stdname)>1:
        raise Exception(f'ERROR: requested variable {varname} is in netcdf not 1 but {len(varlist_stdname)} times: {varlist_stdname}')
    
    #check if requested varname is in long_name attrs of ncvars
    ds_longname = data_xr.filter_by_attrs(long_name=varname)
    varlist_longname = list(ds_longname.data_vars.keys())
    if len(varlist_longname)==1:
        varname_matched = varlist_longname[0]
        print(f'requested varname "{varname}" found in long_name attribute of variable {varname_matched}')
        return varname_matched
    elif len(varlist_longname)>1:
        raise Exception(f'ERROR: requested variable {varname} is in netcdf not 1 but {len(varlist_longname)} times: {varlist_longname}')
    
    #if not returned above, the varname was not found so raise exception
    raise Exception(f'ERROR: requested variable {varname} not in netcdf, available are: {varlist} and the standard_name and long_name attrs in dfm_tools.get_nc_helpers.get_ncvarproperties(file_nc=file_nc)')    
    return varname_matched
