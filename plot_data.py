import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
import calendar
import pandas as pd

save_name = os.path.join('saved_data', 'padova.pickle')
    
with open(save_name, 'rb') as fh:
    full_dataset = pickle.load(fh)
    
    
#%%
    
day_range = np.arange(1,28+1,1)
year_range = np.arange(2017,2020+1)
year_range = np.arange(2015,2020+1)
month_range = np.arange(1,12+1)

#year_range = [2019, 2020]

quality_idx = 'O3_max'
location = 'PD - Arcella'
location = 'PD - Via G. Carli'

TW = 10

my_data = {}
my_t = {}

for year in year_range:
    y = []
    x = []
    for month_n in month_range:
        for day_n in day_range:
            
            key = (year,month_n,day_n)
            
            if key in full_dataset:
                df_day = full_dataset[(year,month_n,day_n)]
                df_city = df_day.loc[location,:]
                idx_value = df_city[quality_idx]
            else:
                idx_value = None
                
            if idx_value:
                if idx_value.isnumeric():
                    y.append(float(idx_value))
                else:
                    y.append(np.nan)
            else:
                y.append(np.nan)
                
            x.append(F'{day_n}/{month_n}')
        
    my_data[year] = y
    my_t[year] = x

    
fig, ax = plt.subplots(1,1)
for year in my_data:
    
    y = my_data[year]
    y = pd.Series(y)
    y = y.fillna(method='backfill')
    
    y = y.rolling(TW).mean()
    
    x = np.arange(0,len(y),1)
#    plt.plot(x, y, '-o', label=year)
    plt.plot(x, y, '-', label=year)

plt.ylabel(F'{quality_idx} (ug/m^3)');
month_str = calendar.month_name[month_n]
plt.title(F'{quality_idx} in {location} | moving average over {TW} days')
plt.grid()
plt.legend()
plt.xticks(x[0:-1:5]);
ax.set_xticklabels(my_t[year][0:-1:5]);
for tick in ax.get_xticklabels():
    tick.set_rotation(90)

