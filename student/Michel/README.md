# Polar Vortex: SSW 20/21, Bouyancywave model resolution & Model comparison

Here are the scripts developed for the students project. 

https://user-images.githubusercontent.com/42503231/151681552-29c70c59-35f5-4e73-aa3e-93ba0e253151.mp4

https://user-images.githubusercontent.com/42503231/151682178-33e94486-a2d5-462b-a7cb-4954c2048a13.mp4


There is a plain python script [Eval.py](https://github.com/VACILT/PV_characteristics_ICON-NWP/blob/main/student/Michel/Eval.py), containing plotting routines to plot climate data:
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
    
