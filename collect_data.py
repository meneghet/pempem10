import pandas as pd
import time
import requests
import os
from bs4 import BeautifulSoup

#%%

provincia = 'padova'

time_range = pd.date_range(start='1/1/2013', end=pd.datetime.today())
# time_range = pd.date_range(start='24/3/2020', end=pd.datetime.today())

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
save_dir = os.path.join('datasets',provincia)
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
    save_name = os.path.join(save_dir, F'{location_str}.csv')
    loc_df.to_csv(save_name)






