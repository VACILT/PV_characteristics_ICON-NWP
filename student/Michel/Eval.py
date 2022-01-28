import numpy as np
import xarray as xr
import cfgrib

import os
from PIL import Image

import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.colors as colors
plt.rcParams.update({'font.size': 16, "axes.labelsize":16, "axes.titlesize":16,
                     "font.weight": "bold","axes.labelweight":"bold","axes.titleweight":"bold",
                    "figure.titleweight":"bold", "figure.titlesize":"large" })

from aostools import climate


tt_SSW = np.datetime64('2021-01-04T18')
tt_GWF = np.datetime64('2020-12-26T00')



results_dir = {
    'icon':'/home/ap1_12/Michalkow/polar_vortex/results/icon/',
    'era5':'/home/ap1_12/Michalkow/polar_vortex/results/era5/',
    'geos':'/home/ap1_12/Michalkow/polar_vortex/results/geos/'
}

results_dir_vid = {
    'icon':'/home/ap1_12/Michalkow/polar_vortex/results/icon/gifs/',
    'era5':'/home/ap1_12/Michalkow/polar_vortex/results/era5/gifs/',
    'geos':'/home/ap1_12/Michalkow/polar_vortex/results/geos/gifs/'
}

dateset_name = {
    'icon':'ICON',
    'era5':'ERA5',
    'geos':'GEOS-FP',
    'geos_vmfc':'GEOS-FP'
}

var_info = {
    'z':{
        'unit':r'$[\: \frac{m^2}{s^2} \:]$',
        'title':'Geopotential'
        },
    't':{
        'unit':r'$[\: K \:]$',
        'title':'Temperature'
        },
    'tc':{
        'unit':r'$[\: ^\circ C \:]$',
        'title':'Temperature'
        },
    'u':{
        'unit':r'$[\: \frac{m}{s} \:]$',
        'title':'Zonal Wind'
        },
    'v':{
        'unit':r'$[\: \frac{m}{s} \:]$',
        'title':'Meridional Wind'
        },
    'w':{
        'unit':r'$[\: \frac{m}{s} \:]$',
        'title':'Vertical Wind'
        },
    'EP1':{
        'unit':r'$[\: \frac{m^3}{s^2} \:]$',
        'title':'EP Flux 1'
        },
    'EP2':{
        'unit':r'$[\: \frac{m^3}{s^2} \:]$',
        'title':'EP Flux 2'
        },
    'EP1_div':{
        'unit':r'$[\: \frac{m}{s \, d} \:]$',
        'title':'EP Flux 1 Div'
        },
    'EP2_div':{
        'unit':r'$[\: \frac{m}{s \, d} \:]$',
        'title':'EP Flux 2 Div'
        },
    'EP_div':{
        'unit':r'$[\: \frac{m}{s \, d} \:]$',
        'title':r'$(\nabla \cdot F)_m + (\nabla \cdot F)_v$'
        },
    'vmfc':{
        'unit':r'$[\: \frac{m}{s \, d} \:]$',
        'title':'Vertical Momentum Flux Convergence'
        }
}


coord_info = {
    'icon':{
        'time':'time',
        'lat':'latitude',
        'lon':'longitude',
        'p':'isobaricInhPa'
    },
    'era5':{
        'time':'time',
        'lat':'latitude',
        'lon':'longitude',
        'p':'isobaricInhPa'
    },
    'geos':{
        'time':'time',
        'lat':'lat',
        'lon':'lon',
        'p':'lev'
    },
    'geos_vmfc':{
        'time':'time',
        'lat':'latitude',
        'lon':'longitude',
        'p':'isobaricInhPa'
    }
}


def plot_map_xr(arr, date, dataset,
             levels=10, cmap=plt.cm.Blues,
             norm=False, norm_bound=None, norm_type='linear',
             projection=ccrs.Robinson(-180),
             gridlines=True, figsize=(12 ,9), save=False):
    
    fig = plt.figure (figsize = figsize, constrained_layout=True)
    ax = fig.add_subplot(1, 1, 1, projection=projection)
    
    arr_name = arr.name
    p_level = arr[coord_info.get(dataset).get('p')].data
    
#     arr = arr[...]
    lats=arr[coord_info.get(dataset).get('lat')]
    lons=arr[coord_info.get(dataset).get('lon')]
    # add cyclic point
    arr, lons_m = add_cyclic_point(arr, coord=lons)

    # generate 2-d arrays from 1-d arrays
    # lon2d, lat2d = np.meshgrid (lon_m , lat )
    
    if norm:
        if norm_type == 'linear':
            if norm_bound is None:
                vvmin = arr.min()
                vvmax = arr.max()
                vnorm = mpl.colors.Normalize(vmin=vvmin, vmax=vvmax)
            else:
                vvmin = norm_bound[0]
                vvmax = norm_bound[1]
                vnorm = mpl.colors.Normalize(vmin=vvmin, vmax=vvmax)

        if norm_type == 'diverging':
            if norm_bound is None:
                vvmin = arr.min()
                vvmax = arr.max()
                vnorm = colors.TwoSlopeNorm(vmin=vvmin, vcenter=0, vmax=vvmax )
            else:
                vvmin = norm_bound[0]
                vvmedi = norm_bound[1]
                vvmax = norm_bound[2]

                vnorm = colors.TwoSlopeNorm(vmin=vvmin, vcenter=vvmedi, vmax=vvmax )
        
        cs = ax.contourf(lons_m, lats, arr, levels,
                            transform=ccrs.PlateCarree(),
                            cmap=cmap,
                            norm=vnorm,
                      )
    else:
        cs = ax.contourf(lons_m, lats, arr, levels,
                            transform=ccrs.PlateCarree(),
                            cmap=cmap,
                            #norm=vnorm,
                      )
    
    ax.set_global()
    ax.coastlines('110m')
    if gridlines:
        gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                      linewidth=1, color='gray', alpha=0.5,
                          #linestyle='--',
                         )
        gl.top_labels = False
        gl.bottom_labels = False
    
    # add colorbar
    if norm:
#         cb = fig.colorbar(cs ,orientation='horizontal', pad=0.06, aspect=50)
#         cb = fig.colorbar(cs ,orientation='horizontal', pad=0.06, aspect=50, norm=vnorm)
        cb = fig.colorbar(
               mpl.cm.ScalarMappable(norm=vnorm, cmap=cmap),
               ticks=np.linspace(vvmin, vvmax, 10),
               orientation='horizontal', pad=0.06, aspect=50, extend='max'
            )


    else:
        cb = fig.colorbar(cs ,orientation='horizontal', pad=0.06, aspect=50, extend='max')
    
    
    
    if max(abs(arr.min()),abs(arr.max())) > 9999:
        f = mticker.ScalarFormatter(useOffset=False, useMathText=True)
        g = lambda x1, pos: "${}$".format(f._formatSciNotation('%1.3e' % x1))
        cb.ax.xaxis.set_major_formatter(mticker.FuncFormatter(g))

    for label in cb.ax.xaxis.get_ticklabels():
        label.set_rotation(45)
        label.set_ha('right')

        
    # naming
    title = dateset_name.get(dataset) + ': ' + var_info.get(arr_name).get('title') + ': ' + str(int(p_level )) + ' hPa' + '\n' 
    title += str(date.data).split(':')[0]
    cb_label = arr_name + ' ' + var_info.get(arr_name).get('unit')
    
    cb.ax.set_title(cb_label)
    ax.set_title(title)
    
    
    if save:
        save_name = arr_name + '_' + str(int(p_level)) + 'hPa/' + arr_name + '_' + str(int(p_level)) + 'hPa_' 
        save_name += str(date.data).split(':')[0].replace('-','_')
        
        plt.savefig(results_dir.get(dataset) + "/" + save_name, dpi=100)
        plt.close(fig)
    else:
        plt.show()
       
    
##################################################################
def plot_profile_xr(arr, date, dataset, mode='meridional' ,norm_bound=None, average = True,
                    save=False, norm_type='diverging', cmap=plt.cm.PuOr, levels=50):
    
    if average:
        if mode == 'meridional': 
            arr = arr.mean(dim = coord_info.get(dataset).get('lon'))
        elif mode == 'zonal': 
            coslat_weights = np.cos(np.deg2rad(var_coarse[coord_info.get(dataset).get('lat')]))
            coslat_weights.name = "weights"
            arr = arr.weighted(coslat_weights)
            arr = arr.mean(dim = coord_info.get(dataset).get('lat'))

    if norm_bound is None:
        vvmin = arr.min().data
        vvmax = arr.max().data
    else:
        vvmin = norm_bound[0]
        vvmax = norm_bound[1]
        
        
    if norm_type == 'diverging':
        vnorm = mpl.colors.TwoSlopeNorm(vmin=vvmin, vcenter=0, vmax=vvmax)
    elif norm_type == 'linear':
        vnorm = mpl.colors.Normalize(vmin=vvmin, vmax=vvmax)
        

    fig, ax = plt.subplots(figsize=(10,7), constrained_layout=True)
    
    if mode == 'meridional':
        ax.contourf(arr[coord_info.get(dataset).get('lat')], arr[coord_info.get(dataset).get('p')],
                    arr.data, cmap=cmap, levels=levels, norm=vnorm,
                    )
    elif mode == 'zonal':
        ax.contourf(arr[coord_info.get(dataset).get('lon')], arr[coord_info.get(dataset).get('p')],
                    arr.data, cmap=cmap, levels=levels, norm=vnorm,
                    )
        

    ax.set_yscale('log')
    ax.invert_yaxis()

    ax.grid()


    cb = fig.colorbar(
                   mpl.cm.ScalarMappable(norm=vnorm, cmap=cmap),
                   ticks=np.linspace(vvmin, vvmax, 10),
                   orientation='horizontal', pad=0.06, aspect=50, extend='max'
                )

    if max(abs(vvmin),abs(vvmax)) > 9999:
        f = mticker.ScalarFormatter(useOffset=False, useMathText=True)
        g = lambda x1, pos: "${}$".format(f._formatSciNotation('%1.3e' % x1))
        cb.ax.xaxis.set_major_formatter(mticker.FuncFormatter(g))

    for label in cb.ax.xaxis.get_ticklabels():
        label.set_rotation(45)
        label.set_ha('right')
    
    ############
    if mode == 'meridional':
        x_label = coord_info.get(dataset).get('lat')
    elif mode == 'zonal':
        x_label = coord_info.get(dataset).get('lon')
        
    title = dateset_name.get(dataset) + ': ' + var_info.get(arr.name).get('title') + ': ' + mode +' Profile' + '\n' 
    title += str(date.data).split(':')[0]
    y_label = r'p $[hPa]$' 
    cb_label = arr.name + ' ' + var_info.get(arr.name).get('unit')
        
        
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    cb.ax.set_title(cb_label)

    if save:
        save_name = arr.name + '_' + mode + '_profile/' + arr.name + '_' + mode + '_profile_'
        save_name += str(date.data).split(':')[0].replace('-','_')
        
        plt.savefig(os.path.join(results_dir.get(dataset), save_name), dpi=100)
        plt.close(fig)
    else:
        plt.show()

        
###############################################################################################
def plot_time_profile_xr(arr, dataset, mode='meridional' ,norm_bound=None, average = True,
                    save=False, norm_type='diverging', cmap=plt.cm.PuOr, levels=50, title=None, mark_time=True,
                         linthresh=0.5, linscale=1.0, base=np.e):
    
    if average:
        if mode == 'meridional': 
            arr = arr.mean(dim = coord_info.get(dataset).get('lon'))
        elif mode == 'zonal': 
            coslat_weights = np.cos(np.deg2rad(var_coarse[coord_info.get(dataset).get('lat')]))
            coslat_weights.name = "weights"
            arr = arr.weighted(coslat_weights)
            arr = arr.mean(dim = coord_info.get(dataset).get('lat'))

    if norm_bound is None:
        vvmin = arr.min().data
        vvmax = arr.max().data
    else:
        vvmin = norm_bound[0]
        vvmax = norm_bound[1]
        
        
    if norm_type == 'diverging':
        vnorm = mpl.colors.TwoSlopeNorm(vmin=vvmin, vcenter=0, vmax=vvmax)
    elif norm_type == 'symlog':
        vnorm = mpl.colors.SymLogNorm(linthresh=linthresh, linscale=linscale, vmin=vvmin, vmax=vvmax, base=base)
    elif norm_type == 'linear':
        vnorm = mpl.colors.Normalize(vmin=vvmin, vmax=vvmax)
        
    
    fig, ax = plt.subplots(figsize=(10,7), constrained_layout=True)
    
    time_arr = [np.datetime64(t.data) for t in arr.time]
    
    ax.contourf(time_arr, arr[coord_info.get(dataset).get('p')],
                arr.transpose(), cmap=cmap, levels=levels, norm=vnorm,
                )
    
    if mark_time:
        ax.axvline(x = tt_SSW, color = 'r', label = 'SSW')
        ax.axvline(x = tt_GWF, color = 'g', label = 'GWF')
        
        ax.legend()
        

    ax.set_yscale('log')
    ax.invert_yaxis()

    ax.grid()


    cb = fig.colorbar(
                   mpl.cm.ScalarMappable(norm=vnorm, cmap=cmap),
                   ticks=np.linspace(vvmin, vvmax, 10),
                   orientation='vertical', pad=0.06, aspect=50, extend='max'
                )

    if max(abs(vvmin),abs(vvmax)) > 9999:
        f = mticker.ScalarFormatter(useOffset=False, useMathText=True)
        g = lambda x1, pos: "${}$".format(f._formatSciNotation('%1.3e' % x1))
        cb.ax.xaxis.set_major_formatter(mticker.FuncFormatter(g))

    for label in ax.xaxis.get_ticklabels():
        label.set_rotation(45)
        label.set_ha('right')
    
    ############
    if mode == 'meridional':
        x_label = coord_info.get(dataset).get('lat')
    elif mode == 'zonal':
        x_label = coord_info.get(dataset).get('lon')
    
    if title is None:
        title = dateset_name.get(dataset) + ': ' + var_info.get(arr.name).get('title') + ': ' + 'time' +' Profile' + '\n' 
        #title += str(date.data).split(':')[0]
    else:
        pass
    
    y_label = r'p $[hPa]$' 
    cb_label = arr.name + ' ' + var_info.get(arr.name).get('unit')
        
        
    ax.set_title(title)
    #ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    cb.ax.set_title(cb_label)

    if save:
        save_name = arr.name + '_' + 'Time' + '_profile/' + arr.name + '_' + 'time' + '_profile_'
        #save_name += str(date.data).split(':')[0].replace('-','_')
        
        plt.savefig(os.path.join(results_dir.get(dataset), save_name), dpi=100)
        plt.close(fig)
    else:
        plt.show()

        
#################################################
def make_gif(file_folder, dataset, duration=100):

    files_img_list = os.listdir(file_folder)
    files_img_list.sort()
    save_name = '_'.join(files_img_list[0].split('_')[:-3])

    images = []
    rez_images = []
    for file in files_img_list:
        img = Image.open(os.path.join(file_folder, file))
        images.append(img)
        basewidth = 600
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img_rez = img.resize((basewidth,hsize), Image.ANTIALIAS)
        #print(img.size, img_rez.size)
        #img = img.resize((basewidth,hsize))
        rez_images.append(img_rez)
        img_rez.save(os.path.join(file_folder, file)) # !!!

    rez_images[0].save(os.path.join(results_dir_vid.get(dataset), save_name + '_small.gif'),
               save_all=True, append_images=rez_images[1:], optimize=False, duration=duration, loop=0)
        
        