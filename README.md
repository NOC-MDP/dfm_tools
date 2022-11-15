dfm_tools
=========

A Python package for pre- and postprocessing D-FlowFM model input and output files. Contains convenience functions built on top of other packages like [xarray](https://github.com/pydata/xarray), [hydrolib-core](https://github.com/Deltares/HYDROLIB-core) and many more.

Information and examples
--------
- [pdf with dfm_tools features and examples](https://nbviewer.org/github/openearth/dfm_tools/raw/pptx/docs/dfm_tools.pdf?flush_cache=true)
- [html documentation of docstrings](https://htmlpreview.github.io/?https://github.com/openearth/dfm_tools/blob/master/docs/dfm_tools/index.html)
- [jupyter notebook with example code](https://github.com/openearth/dfm_tools/blob/master/notebooks/postprocessing_readme_example.ipynb)
- [more example scripts on github](https://github.com/openearth/dfm_tools/tree/master/tests/examples)


Installation
--------
- download and install Anaconda 64 bit (with Python 3.8 or later) from https://www.anaconda.com/distribution/#download-section
- open Anaconda prompt
- ``conda create --name dfm_tools_env -c conda-forge python=3.8 git spyder -y`` (you can also install a newer python version)
- ``conda activate dfm_tools_env``
- ``conda install -c conda-forge shapely cartopy pyepsg geopandas contextily xarray dask netcdf4 bottleneck cdsapi pydap" -y`` (installs conda-forge requirements)
- ``python -m pip install git+https://github.com/openearth/dfm_tools`` (this command installs dfm_tools and all required non-conda packages, also use to update)
- long paths error? Check last comment in https://github.com/Deltares/HYDROLIB-core/issues/327
- to remove environment when necessary: ``conda remove -n dfm_tools_env --all``
