# Polar Vortex: SSW 20/21, Bouyancywave model resolution & Model comparison

Here are the scripts developed for the students project. 

There is a plain python script Eval.py, containing plotting routines to plot climate data:
- on a map
- meridional profile
- time evolution profiles
- and a function to create animated gifs from a directory containing the corresponding pictures

The main Evaluation is then done in the following jupyter notebooks:
- 3 equivalent notebooks for different datesets
  - [Evaluation_ICON.ipynb](https://github.com/VACILT/PV_characteristics_ICON-NWP/blob/main/student/Michel/Evaluation_ICON.ipynb) | just for the icon dataset(s). animated gifs for variety of quantities, EP Flux, VMFC
  - [Evaluation_ERA5.ipynb](https://github.com/VACILT/PV_characteristics_ICON-NWP/blob/main/student/Michel/Evaluation_ERA5.ipynb) | just for the era5 dataset(s). animated gifs for variety of quantities, EP Flux, VMFC
  - [Evaluation_GEOS.ipynb](https://github.com/VACILT/PV_characteristics_ICON-NWP/blob/main/student/Michel/Evaluation_GEOS.ipynb) | just for the geos dataset(s). animated gifs for variety of quantities, EP Flux, VMFC
- 1 notebook for all datasets, if one wishes to plot direct comparisons in one plot. 
  - [Evaluation_Combined.ipynb](https://github.com/VACILT/PV_characteristics_ICON-NWP/blob/main/student/Michel/Evaluation_Combined.ipynb)
  - basically same Quantities as in the other notebooks. 
  - this is the newest state of the art, so here is some new features as:
    - EP_div vector sum
    - symlog colorbars
- 1 notebook for image manipulation
  - [Picture_Manipulation.ipynb](https://github.com/VACILT/PV_characteristics_ICON-NWP/blob/main/student/Michel/Picture_Manipulation.ipynb)
  - take a set (directory) of pictures and arrange them in a grid
    
