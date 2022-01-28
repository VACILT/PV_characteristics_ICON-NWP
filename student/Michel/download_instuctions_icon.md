
# Download data with icon-globe:
### create conda environment nwp-py2 for downloading
`conda create -n nwp-py2 python=3.6`

Modules necessary for download:
- requests
- beautifulsoup4
- cdo (!)

### create conda environment nwp-py3 for evaluation
- numpy
- pandas
- xarray
- dask
- netCDF4
- cfgrib
- matplotlib
- cartopy (conda-forge)
- (ipywidgets | not used)
- aostools
	- (windspharm | not used)
- (ambiance | standart atmosphere)
- PIL (for image manipulation and gif creation)

## download icon grids & weights
- 13 km resolution
  - http://icon-downloads.mpimet.mpg.de/dwd_grids.xml#grid26
- ICON_GLOBAL2WORLD_0125_EASY.tar.bz2  
  - https://opendata.dwd.de/weather/lib/cdo/
- adjust filenames in functions_download_dwd.sh
- adjust hights levels in functions_download_dwd.sh
 
## changes variables in copy_data.run
`export MODEL_DATA_FOLDER="./tmp/icon-globe/"`<br>
`DATA_PLOTTING=false`<br>
`DATA_UPLOAD=false`<br>
- dont download 2D variables (# `parallel -j 8 --delay 1 download_merge_2d_variable_icon_globe ::: "${variables[@]}"`
- activate and deactivate the conda environment
  - `source /opt/miniconda3/etc/profile.d/conda.sh`
  - `conda activate nwp-py2`
  - `conda deactivate`

## changes in get_last_run.py
- modified var_2d_list
- modified var_3d_list

## make a cronjob shedule
- adjust cron.tab file properly
- absolute path names !
- start the shedule
  - crontab -u ap1_12 cron.tab


to do:
=============================
- put output into seperate directory with datename | outdated
- merge nc files | outdated
- interpolate | outdated
	- delete old files to save disk space

Problems:
=============================

