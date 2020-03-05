import pandas as pd
import time
import calendar
import requests
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
import pickle


provincia = 'padova'

year_range = range(2015,2020+1,1)
month_range = range(1,12+1,1)
day_range = range(1,31+1,1)

full_dataset = {}

for month_n in month_range:
    for year_n in year_range:
        for day_n in day_range:
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
            
                full_dataset[(year_n,month_n,day_n)] = df_view
                        
                print(F'Year: {year_n}, Month: {month_n}, Day: {day_n}')
                time.sleep(10)
    
#%%
month_n = 2
day_range = np.arange(1,28+1,1)
year_range = np.arange(2018,2019+1)
month_range = np.arange(1,12+1)

quality_idx = 'PM10'
location = 'PD - Arcella'

year_data = {}

for year in year_range:
    y = []
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
                y.append(float(idx_value))
            else:
                y.append(np.nan)
            
    year_data[year] = y
    

    
plt.figure()
for year in year_data:
    x = np.arange(0,len(year_data[year]),1)
    plt.plot(x, year_data[year], '-o', label=year)

plt.ylabel(F'{quality_idx} (ug/m^3)');
month_str = calendar.month_name[month_n]
plt.title(F'{quality_idx} in {location} | {month_str}')
plt.grid()
plt.legend()
plt.xticks(day_range);


#%%

# save
save_name = os.path.join('saved_data', 'padova.pickle')
with open(save_name, 'wb') as filehandler:
    pickle.dump(full_dataset, filehandler)



