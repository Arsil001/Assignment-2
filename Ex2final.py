#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install wptools')
get_ipython().system('pip install wikipedia')
get_ipython().system('pip install wordcloud')
get_ipython().system('pip install gdown')

import json
import wptools
import wikipedia
import pandas as pd
import requests
import io
import re 
from wordcloud import WordCloud
import urllib.request
import numpy as np
from bs4 import BeautifulSoup as bs



### Checking the version of wptools
print('wptools version : {}'.format(wptools.__version__))

### Importing the csv file from Github - Output of Excercise 1
url = "https://raw.githubusercontent.com/Arsil001/Assignment-2/main/israeli_wbsettlement.csv"
download = requests.get(url).content
df = pd.read_csv(io.StringIO(download.decode('utf-8')))
df.head()     # displaying the first 5 rows

### # converting the column of settlement into a list
settlements = df['name'].tolist()  

### Enumerating the list of settlements
for i, j in enumerate(settlements):   # looping through the list of settlements 
    print('{}. {}'.format(i+1, j))    # printing out the same

### Searching for each settlement in the Wikipedia - Approx 1 min
wiki_search = [{settlement : wikipedia.search(settlement)} for settlement in settlements]

### To get the list of suggestion of wikipedia for all the settlement names
for idx, settlement in enumerate(wiki_search):
    for i, j in settlement.items():
        print('{}. {} :\n{}'.format(idx+1, i ,', '.join(j)))
        print('\n')

### Getting the most probable search outcome for each of the settlement
most_probable = [(settlement, wiki_search[i][settlement][0]) for i, settlement in enumerate(settlements)]
settlements = [x[1] for x in most_probable]
print(most_probable)
print(settlements)

### Note that there are some mismatches, we identify those mismatches and replacing them with correct one (36)
settlements[settlements.index('She-Ra')]                =   'Adora, Har Hevron'
#settlements[settlements.index('Eylon Almog')]           =   'Almog'      
settlements[settlements.index('Almon')]                 =   'Almon, Mateh Binyamin'
settlements[settlements.index('Nadav Argaman')]         =   'Argaman'
settlements[settlements.index('Ariel')]                 =   'Ariel (city)'
settlements[settlements.index('ASFAR (football club)')] =   'Metzad'
settlements[settlements.index('Ateret Cohanim')]        =   'Ateret'
settlements[settlements.index('Ady Barkan')]            =   'Barkan'
settlements[settlements.index('Carmel')]                =   'Carmel, Mount Hebron'
settlements[settlements.index('Eleazar')]               =   'Elazar, Gush Etzion'
settlements[settlements.index('Eli')]                   =   'Eli, Mateh Binyamin'
settlements[settlements.index('Gilgal')]                =   "Gilgal, Bik'at HaYarden"
settlements[settlements.index('Gitit (software)')]      =   "Gitit, Bik'at HaYarden"
settlements[settlements.index('Hamra')]                 =   "Hamra, Bik'at HaYarden"
settlements[settlements.index('Hemdat Yamim')]          =   'Hemdat'
settlements[settlements.index('Shai Hermesh')]          =   'Hermesh'
settlements[settlements.index('Immanuel')]              =   'Immanuel (town)'
settlements[settlements.index('Kedar')]                 =   'Kedar, Gush Etzion'
settlements[settlements.index('Yair Lapid')]            =   'Lapid, Israel'
settlements[settlements.index('Maon')]                  =   "Ma'on, Mount Hebron"
settlements[settlements.index('Patience Masua')]        =   'Masua'
settlements[settlements.index('Josephus')]              =   'Matityahu, Mateh Binyamin'
settlements[settlements.index('Mehola Junction bombing')]=   'Mehola'
settlements[settlements.index('Nili')]                  =   'Nili, Mateh Binyamin'
settlements[settlements.index('Cyclone Niran')]         =   'Niran'
settlements[settlements.index('Ofra Haza')]             =   'Ofra'
settlements[settlements.index('Reihan Salam')]          =   'Reihan'
settlements[settlements.index('Rotem')]                 =   "Rotem, Bik'at HaYarden"
settlements[settlements.index('Alon Livne')]            =   'Livne'
settlements[settlements.index('Shiloh')]                =   'Shilo, Mateh Binyamin'
settlements[settlements.index('Susya')]                 =   'Susya, Har Hevron'
#settlements[settlements.index('Talmon Marco')]          =   'Talmon'
settlements[settlements.index('Tekoa')]                 =   'Tekoa, Gush Etzion'
settlements[settlements.index('Benjamin Telem')]        =   'Telem, Har Hevron'
settlements[settlements.index('TÖMER')]                 =   'Tomer'
settlements[settlements.index('G. Yafit')]              =   'Yafit'

### Final list of wikipedia article titles
print(settlements)                

### Having a look at one of the page
page = wptools.page('Beit Aryeh-Ofarim')
page.get_parse() 
### To check infobox key
page.data.keys() 
### Looking at Infobox of the page
page.data['infobox']
page.data['wikidata_url']   ### Link for infobox table only
print(wikipedia.page("Beit Aryeh-Ofarim").url)

### What we need for each settlement, area, leader name, leader title, coordinates, and website from infobox
# website

wiki_data = []
features = ['leader_name', 'leader_title', 'area_total_dunam', 'coordinates' ]


#### Doing this for all of the settlements
for settlement in settlements:    
    page = wptools.page(settlement) # create a page object
    try:
        page.get_parse()            # call the API and parse the data
        if page.data['infobox'] != None:
            # if infobox is present
            infobox = page.data['infobox']
            # get data for the interested features/attributes
            data = { feature : infobox[feature] if feature in infobox else '' 
                         for feature in features }
        else:
            data = { feature : '' for feature in features }

        data['settlement_search_name'] = settlement
        wiki_data.append(data)

    except KeyError:
        pass
### Checking for a settlemet
wiki_data[25]

### Dumping as Json file
with open('infoboxes.json', 'w') as file:
    json.dump(wiki_data, file)


### Importing the JSON file from Github - Output of Excercise 1
url = "https://raw.githubusercontent.com/Arsil001/Assignment-2/main/infoboxes.json"
urllib.request.urlretrieve(url, 'infoboxes.json')

### Opening Json file
with open('infoboxes.json', 'r') as file:
    wiki_data = json.load(file)

### Having a look at data
wiki_data[25]
print(wiki_data[25]['coordinates'])

additional_data = []
for i, x in enumerate(wiki_data):
    y = x['area_total_dunam']
    z = x['leader_name']
    u = x['leader_title'] 
    v = x['coordinates']                     
    additional_data.append({'name_search' : x['settlement_search_name'], 'area (dunams)': y, 'leader_name' : z, 'leader_title':u, 'coordinates':v})

### Looking at additional data
additional_data

### Converting it to dataframe
df_add_settlement = pd.DataFrame(additional_data)
df_add_settlement.head()

### Importing earlier results for concatenation
url = 'https://raw.githubusercontent.com/Arsil001/Assignment-2/main/israeli_wbsettlement.csv'
urllib.request.urlretrieve(url, 'israeli_wbsettlement.csv')

### Reading previous work and concatenating both the datasets
df = pd.read_csv('israeli_wbsettlement.csv')
df = pd.concat([df, df_add_settlement], axis=1)     
### Just a look at one row and then data frame
df.iloc[49]
df

### Data Cleaning
### Area - dunams , Ottomons measure of distance
df['area (dunams)']  = df['area (dunams)'].apply(lambda x: x.lstrip('{formatnum:') if x!='-' else '-')
df['area (dunams)']  = df['area (dunams)'].apply(lambda x: x.rstrip('|R}') if x!='-' else '-')
df
df['area (dunams)']  = df['area (dunams)'].apply(lambda x: x.replace(',', '') if x!='-' else '-')
df

### Website
df['wikipedia_link'] = df.loc[:, 'name_search']
df['wikipedia_link'] = df['wikipedia_link'].apply(lambda x: "https://en.wikipedia.org/wiki/"+str(x))
df

### Coordinates - Probably an easier way rather than cleaning the messy coordinates column
def latitude(x):
   req = requests.get(str(x)).text
   soup = bs(req, 'lxml')
   latitude = soup.find("span", {"class": "latitude"})
   return latitude

def longitude(x):
   req = requests.get(str(x)).text
   soup = bs(req, 'lxml')
   longitude = soup.find("span", {"class": "longitude"})
   return longitude
### For Latitude of Settlement
df['settlement_latitude'] = df.loc[:, 'wikipedia_link']
df['settlement_latitude'] = df['settlement_latitude'].apply(lambda x: latitude(x) if x!='-' else '-' )
df['settlement_latitude'] = df['settlement_latitude'].astype(str)
df['settlement_latitude'] = df['settlement_latitude'].apply(lambda x: x[23:-7] if x!='-' else '-' )

### For longitude of Settlement
df['settlement_longitude'] = df.loc[:, 'wikipedia_link']
df['settlement_longitude'] = df['settlement_longitude'].apply(lambda x: longitude(x) if x!='-' else '-' )
df['settlement_longitude'] = df['settlement_longitude'].astype(str)
df['settlement_longitude'] = df['settlement_longitude'].apply(lambda x: x[24:-7] if x!='-' else '-' )
df

### Droping the coordinates column now to clean the data.
df.drop('coordinates', inplace=True, axis=1)
df
df.to_csv('israeli_wbsettlement2.csv', index=False)






