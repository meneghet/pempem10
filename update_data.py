import pandas as pd
import time
import requests
import os
from bs4 import BeautifulSoup

#%%

provincia = 'padova'

#%% retrieve last update day

# load last saved dataset (just one)
save_dir = os.path.join('datasets',provincia)
fnames = os.listdir(save_dir)
df = pd.read_csv(os.path.join(save_dir, fnames[0]), index_col=0)

# find last update day
last_day = df.index.values[-1]

# start from that day until today
time_range = pd.date_range(start=last_day, end=pd.datetime.today())
time_range = time_range[1:]

#%%

full_dataset = {}

for day in time_range:
    
    day_ = day.to_pydatetime()
    day_n = day_.day
    month_n = day_.month
    year_n = day_.year
    
    form_data = {'provincia': provincia,
                 'giorno': f'{day_n:02d}',
                 'mese': f'{month_n:02d}',
                 'anno': f'{year_n:02d}',
                 'Vai': 'Visualizza il bollettino'}
    
    # php form request
    url = "https://www.arpa.veneto.it/arpavinforma/bollettini/aria/aria_dati_validati_storico.php"
    response = requests.post(url, data=form_data)
    doc = BeautifulSoup(response.text, 'html.parser')
    
    # grab all rows
    row_tags = doc.find_all('tr')
    
    if len(row_tags) > 1:
    
        # make header
        header = row_tags[3].text.split('\n')
        df = pd.DataFrame(columns=header)
        
        # add rows
        for n in range(4,len(row_tags),1):
            row_full = row_tags[n].text.split('\n')
            row = pd.Series(row_full, index=header)
            row.name = row['Ubicazione']
            df = df.append(row)
        
        # data for the day
        df_view = df.iloc[:,[4,7,9,11,12,15]]
        df_view.columns = ['NO2','PM10','O3_max','O3_8h','SO2','CO']
    
        full_dataset[day] = df_view
                
        print(F'Year: {year_n}, Month: {month_n}, Day: {day_n}')
        time.sleep(1)

#%%

# save
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
        
all_days = [k for k in full_dataset.keys()]


all_locations = full_dataset[all_days[0]].index

for location in all_locations:

    loc_df = pd.DataFrame(columns=full_dataset[all_days[0]].columns)
    
    for d in all_days:
        df = full_dataset[d]
        sel = (df.index == location)
        loc_df.loc[d,:] = df.iloc[sel,:].values
    
    location_str = location.replace('.','')
    
    save_name = F'{location_str}.csv'
    old_df = pd.read_csv(os.path.join(save_dir, save_name), index_col=0)
    
    # concatenate with old dataset
    df_ = pd.concat([old_df, loc_df])
    
    df_.index = pd.to_datetime(df_.index, format='%Y-%m-%d')
    df_.to_csv(os.path.join(save_dir, save_name))
    
    
    
    
