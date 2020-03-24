import pandas as pd
import time
import requests
import os
from bs4 import BeautifulSoup
import pickle
from datetime import date



#%%
save_name = os.path.join('saved_data', 'padova_full.pickle')


with open(save_name, 'rb') as fh:
    full_dataset = pickle.load(fh)



#%%

provincia = 'padova'

year_range = range(2013,2020+1,1)
month_range = range(1,12+1,1)
day_range = range(1,31+1,1)

#%%
key_list = []
for month_n in month_range:
    for year_n in year_range:
        for day_n in day_range:
            key_list.append((year_n,month_n,day_n))
        
foo = [k for k in key_list if k not in full_dataset.keys()]

foo

#%%

today = date.today()

for month_n in month_range:
    for year_n in year_range:
        for day_n in day_range:
            print(F'Year: {year_n}, Month: {month_n}, Day: {day_n}')
            
            if (year_n,month_n,day_n) in full_dataset.keys():
                continue
            else:
                
                if (year_n >= today.year) and (month_n >= today.month) and (day_n > today.day):
                    continue
                else:
                
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
                        time.sleep(2)


#%%
# save
save_name = os.path.join('saved_data', 'padova_full.pickle')
with open(save_name, 'wb') as filehandler:
    pickle.dump(full_dataset, filehandler)
    
#%%




