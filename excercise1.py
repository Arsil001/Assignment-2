#!/usr/bin/env python
# coding: utf-8

# In[ ]:


####################################
######### EXCERCISE 1 ##############
####################################

### Import the Libraries
import requests
import pandas as pd
from bs4 import BeautifulSoup

### Defining URL for List of Israeli Settlements in West Bank
settlement_url = "https://en.wikipedia.org/wiki/List_of_Israeli_settlements"
response = requests.get(settlement_url)

### Checking the headers
response.headers

### Checking status code and content of the website
print('Status code\n', response.status_code)
print('\n--\n')
print('Content of the website\n', response.content[:2000])

### Soup Object to Present content in a better way
soup_settlement = BeautifulSoup(response.content)
soup_settlement

### Getting the table data
table_settlement = soup_settlement.find_all('table','wikitable')
### Table_settlement[0] - First Table as required
table_wbsettlement  = table_settlement[0]
table_settlement_wb = table_wbsettlement.find_all('tr')

### Inspecting number of rows and content of rows
len(table_settlement_wb)
### 
print(table_settlement_wb[0])
print('--')
print(table_settlement_wb[1])
print('--')
print(table_settlement_wb[128])


### Making Data Frame Empty and then filling the table
wbsettlement_df = pd.DataFrame(columns = ['name', 'hebrew', 'population 2019', 'established', 'council']) 
### Initialise index to zero
ix = 0    
for row in table_settlement_wb[1:]:
    values = row.find_all('td') # Extract all elements with tag <td>
    # Pick only the text part from the <td> tag
    name = values[0].text.strip()
    hebrew = values[1].text.strip()
    population = values[2].text.strip()
    established = values[3].text.strip()
    council = values[4].text.strip()

    ### Storing in the row of data frame
    wbsettlement_df.loc[ix] = [name, hebrew, population, established, council ]
    ix += 1

# Print the first and Last 5 rows of the dataframe including a missing pop. obs.
wbsettlement_df.head()
wbsettlement_df.tail()
wbsettlement_df.iloc[112]

### Saving into .CSV file
wbsettlement_df.to_csv('israeli_wbsettlement.csv', index=False)

