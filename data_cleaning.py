import pandas as pd
import os
#%%
files_list = list()
df_full = pd.DataFrame(columns=['lat', 'lon', 'fare', 'time','cab_name'])
# get all the txt files in the directory
for file in os.listdir('san_fran_cab'):
    if file[-3:] == 'txt':
        files_list.append(file)

count = 0
# iterate through each txt file, read it as a df, convert the time, add the cab name, and append to df_full
for file in files_list[:10]:
    df = pd.read_csv(f'./san_fran_cab/{file}', names=['lat', 'lon', 'fare', 'time'], delimiter=' ')
    df['time'] = pd.to_datetime(df['time'], unit='s')
    name = file[4:-4]
    df['cab_name'] = name
    df_full = pd.concat([df_full, df])
    count += 1
    print(f'{name} complete with {len(df)} rows. '
          f'{len(df_full)} total rows and {count} complete')

df_full.to_csv('cabs_10.csv', index=False)
