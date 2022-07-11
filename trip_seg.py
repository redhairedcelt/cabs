#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 17 05:21:04 2022

@author: patrickmaus
"""
import pandas as pd
import matplotlib.pyplot as plt
path = '/Users/patrickmaus/Documents/projects/cabs/'
# read in cabs data
df_full = pd.read_csv(path+'cabs_10.csv')
df_full = df_full.sort_values(['cab_name', 'time']).reset_index(drop=True)
df_full['fare_next'] = df_full['fare'].shift(-1)
df_full['fare_prev'] = df_full['fare'].shift(1)
#%%
pickups = df_full[(df_full['fare']==1) & (df_full['fare_prev']==0)]
dropoffs = df_full[(df_full['fare']==1) & (df_full['fare_next']==0)]

pickups.drop(['fare', 'fare_prev', 'fare_next'], axis=1, inplace=True)
dropoffs.drop(['fare', 'fare_prev', 'fare_next'], axis=1, inplace=True)
#%%
