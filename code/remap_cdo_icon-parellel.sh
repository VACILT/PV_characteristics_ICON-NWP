#!/bin/bash

invar=$1
root_path="/projekt4/hochatm/akuchar/ICON/dwd/icon/u/opendata.dwd.de/weather/nwp/icon/grib/06/"
infiles=${root_path}${invar}/*.grib2
TARGET_GRID_DESCRIPTION=ICON_GLOBAL2WORLD_025_EASY/target_grid_world_025.txt
WEIGHTS_FILE=ICON_GLOBAL2WORLD_025_EASY/weights_icogl2world_025.nc

for i in $(ls ${infiles}); do out="${root_path}${invar}/nc/$(basename "$i" .grib2).nc"; echo "cdo -f nc remap,${TARGET_GRID_DESCRIPTION},${WEIGHTS_FILE} $i $out"; done | parallel -v -j 12

#


