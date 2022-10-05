# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 12:07:18 2022

@author: veenstra
"""

from pathlib import Path
from hydrolib.core.io.mdu.models import FMModel, NetworkModel, ExtModel, StructureModel
from dfm_tools.hydrolib_helpers import forcingobject_to_dataframe
import matplotlib.pyplot as plt
plt.close('all')
file_mdu = Path(r'p:\11206813-006-kpp2021_rmm-2d\C_Work\31_RMM_FMmodel\computations\model_setup\run_206_HYDROLIB\RMM_dflowfm.mdu') #model with all but one structure and all but one lateral commented, reduces validation errors from >200 to 5. TODO: resolve validation errors
#file_mdu = Path(r'c:\DATA\dfm_tools_testdata\DFM_3D_z_Grevelingen\computations\run01\Grevelingen-FM.mdu')
#fm = FMModel(file_mdu) #TODO: currently crashes on issues below, and is quite slow since all files are being read


file_struct = Path(r'p:\11206813-006-kpp2021_rmm-2d\C_Work\31_RMM_FMmodel\computations\model_setup\run_206_HYDROLIB\RMM_structures.ini')
#structs = StructureModel(file_struct)
#TODO: pli in structures.ini is currently not supported: https://github.com/Deltares/HYDROLIB-core/issues/353 (use *_original file to test after fix)
#TODO: single structure in structures.ini currently crashes because of missing make_list_validator: https://github.com/Deltares/HYDROLIB-core/pull/352 (use *_original file to test after fix)

file_extnew = Path(r'p:\11206813-006-kpp2021_rmm-2d\C_Work\31_RMM_FMmodel\computations\model_setup\run_206_HYDROLIB\RMM_bnd.ext')
#ext = ExtModel(fm.external_forcing.extforcefilenew) #TODO: also possible to read from FMmodel?
ext = ExtModel(file_extnew)
#TODO: laterals xycoordinates float is not yet supported (int is prescribed in ext model): https://github.com/Deltares/HYDROLIB-core/pull/351 (use *_original file to test after fix)

max_extforcings = 6 #None for all?

ext_boundaries = ext.boundary
for iEB, extbnd in enumerate(ext_boundaries): #TODO: waterlevelbnd for rivers are present three times: https://github.com/Deltares/HYDROLIB-core/issues/354
    extbnd_filepath = extbnd.forcingfile.filepath
    print(f'boundary {iEB+1} of {len(ext_boundaries)}: {extbnd_filepath}')
    extbnd_forcings = extbnd.forcingfile.forcing
    fig,ax = plt.subplots(figsize=(12,6))
    leglabels_new = []
    for iEBF, forcing in enumerate(extbnd_forcings[:max_extforcings]):
        print(f'forcing {iEBF+1} of {len(extbnd_forcings)}: {forcing.name} ({forcing.function}) ({forcing.quantityunitpair[1].quantity})')
        forcing_pd = forcingobject_to_dataframe(forcing)
        ax.set_title(f'{extbnd_filepath}')
        pc = forcing_pd.plot(ax=ax) #TODO: see CMEMS_interpolate_example.py for pcolormesh in case of verticalpositions
        leglabels = pc.get_legend_handles_labels()[1]
        leglabels_new.append(f'{forcing.name} ({forcing.function}) {leglabels[-1]}')
    ax.legend(leglabels_new)
    fig.tight_layout()


#dimr = DIMR("dimr_config.xml")
