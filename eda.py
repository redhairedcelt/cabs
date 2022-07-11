#%%
import pandas as pd
from gnact import clust, network, utils

df = pd.read_csv('./cabspottingdata/new_enarwee.txt',
                 names=['lat', 'lon', 'fare', 'time'],
                 delimiter=' ')
df['time'] = pd.to_datetime(df['time'], unit='s')
name = 'enarwee'
df['cab_name'] = name
df['id'] = 1


df_clusts = clust.calc_clusts(df, method='optics', eps_km=3, min_samp=25)