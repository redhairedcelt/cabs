#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 13 08:12:32 2022

@author: patrickmaus
"""
#%%
import h3
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import contextily as cx
import folium

path = '/Users/patrickmaus/Documents/projects/cabs/'

#%%
def plot_scatter(df, metric_col, x='lon', y='lat', marker='.', alpha=1, colormap='viridis'):    
    df.plot.scatter(x=x, y=y, c=metric_col, title=metric_col
                    , edgecolors='none', colormap=colormap, marker=marker, alpha=alpha);
    plt.xticks([], []); plt.yticks([], [])
# read in cabs data
df_full = pd.read_csv(path+'cabs_10.csv')
#%% remove the one outlier thats an error
df_full.drop(30248, axis=0, inplace=True)
# convert to gdf 
gdf = gpd.GeoDataFrame(df_full, geometry=gpd.points_from_xy(df_full.lon, df_full.lat), crs='EPSG:4326')
#%% plot the points
ax = gdf.plot(figsize=(10, 10))
cx.add_basemap(ax, zoom=12, crs='EPSG:4326', source=cx.providers.CartoDB.Voyager)

#%% sort by time and name, get prev/next fare
gdf = gdf.sort_values(['cab_name', 'time']).reset_index(drop=True)
gdf['fare_next'] = gdf['fare'].shift(-1)
gdf['fare_prev'] = gdf['fare'].shift(1)

#%% determine pickups and dropoffs
pickups = gdf[(gdf['fare']==1) & (gdf['fare_prev']==0)]
dropoffs = gdf[(gdf['fare']==1) & (gdf['fare_next']==0)]

pickups.drop(['fare', 'fare_prev', 'fare_next'], axis=1, inplace=True)
dropoffs.drop(['fare', 'fare_prev', 'fare_next'], axis=1, inplace=True)
#%%

def convert_hex(df, hex_size):
    hex_size = 8
    hex_col = 'hex'+str(hex_size)
    
    # find hexs containing the points
    df[hex_col] = df.apply(lambda x: h3.geo_to_h3(x.lat,x.lon,hex_size),1)
    
    # aggregate the points
    dfg = df.groupby(hex_col).size().to_frame('cnt').reset_index()
    
    #find center of hex for visualization
    dfg['lat'] = dfg[hex_col].apply(lambda x: h3.h3_to_geo(x)[0])
    dfg['lon'] = dfg[hex_col].apply(lambda x: h3.h3_to_geo(x)[1])
    return dfg

hex_pickups = convert_hex(pickups, 8)
hex_dropoffs = convert_hex(dropoffs, 8)
hex_full = convert_hex(df_full, 8)
    
#%%  
# pltot the hexs
ax=plot_scatter(hex_pickups, metric_col='cnt', marker='o')
cx.add_basemap(ax, zoom=12, crs='EPSG:4326', source=cx.providers.CartoDB.Voyager)
plt.title('hex-grid: pickups')
#%%
plot_scatter(hex_dropoffs, metric_col='cnt', marker='o')
plt.title('hex-grid: dropoffs')

#%% look at one driver
for cab in df_full['cab_name'].unique():
    df_full[df_full['cab_name']==cab].plot(x='lon',y='lat',style='.',alpha=1)
    plt.title(cab)
    

    df_full['fare_next'] = df_full['fare'].shift(-1)
    df_full['fare_prev'] = df_full['fare'].shift(1)
    
    # make pickups and drops offs
    pickups = df_full[(df_full['fare']==1) & (df_full['fare_prev']==0)]
    dropoffs = df_full[(df_full['fare']==1) & (df_full['fare_next']==0)]   
   
    # convert to hex
    hex_pickups = (convert_hex(pickups, 8))
    hex_dropoffs = (convert_hex(dropoffs, 8))
        
    # pltot the hexs
    plot_scatter(hex_pickups, metric_col='cnt', marker='o')
    plt.title('hex-grid: pickups')

    plot_scatter(hex_dropoffs, metric_col='cnt', marker='o')
    plt.title('hex-grid: dropoffs')


