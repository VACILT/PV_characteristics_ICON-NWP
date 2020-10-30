#!/bin/bash

remote_location='http://dd.weather.gc.ca/ensemble/geps/grib2/raw'
maxhours=384 #768
run_time=00
init_date=20181222
for hour in `seq -f %03.0f 0 6 $maxhours`
 do
  infile=$remote_location'/'$run_time'/'$hour'/CMC_geps-raw_HGT_ISBL_0010_latlon0p5x0p5_'$init_date$run_time'_P'$hour'_allmbrs.grib2'
  echo $infile
  wget $infile
 done