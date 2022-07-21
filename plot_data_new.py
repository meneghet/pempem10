import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
sns.set(style='whitegrid', context='notebook')

#%%

provincia = 'padova'
location = 'PD - Arcella'

#%% retrieve last update day

# load last saved dataset (just one)
save_dir = os.path.join('datasets',provincia)
fnames = os.listdir(save_dir)
df = pd.read_csv(os.path.join(save_dir, F'{location}.csv'), index_col=0)

#%%
df.index = pd.to_datetime(df.index)

all_idx = [x for x in df.index.values]

year_idx = pd.to_datetime(all_idx).year.values

year_range = np.unique(year_idx)

#%%
year_range = np.arange(2013,2022+1)

quality_idx = 'PM10'

TW = 30

my_data = {}
my_t = {}

for year in year_range:
    
    # data from this year
    df_ = df.loc[year_idx == year, quality_idx]
    
    # convert to numeric
    df_ = pd.to_numeric(df_, errors='coerce')
    
    my_data[year] = df_.values
    my_t[year] = df_.index


#%%
fig, ax = plt.subplots(1,1)
for year in my_data:
    
    t = my_t[year]
    
    y = my_data[year]
    y = pd.Series(y)
    y = y.fillna(method='backfill')
    
    y = y.rolling(TW).mean()
    
    x = np.arange(0,len(y),1)
    
    if year == 2021:
        plt.plot(x, y, 'k-.', label=year)
    else:
        plt.plot(x, y, '-', label=year)

# plt.ylabel(F'{quality_idx} ($\mu g/m^3$)', usetex=True);
plt.title(F'{quality_idx} in {location} | moving average over {TW} days')
# plt.grid()
plt.legend()


t = my_t[2013]
t = t.strftime('%d-%b')
x = np.arange(0,len(t),1)

plt.xticks(x[0:-1:5]);
ax.set_xticklabels(t[0:-1:5]);

for tick in ax.get_xticklabels():
    tick.set_rotation(90)

plt.show()









