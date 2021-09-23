#!/usr/bin/env python
# coding: utf-8

# In[ ]:


####################################
######## ASSIGNMENT 2 ##############
####################################
######### EXCERCISE 3 ##############
####################################
import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
### To show all columns of dataset
pd.get_option("display.max_columns")
import numpy as np
from time import sleep
from random import randint


### To get English Translated version
headers = {"Accept-Language": "en-US, en;q=0.5"}

### Initialize empty variables to store data for each prisoner
name = []
legal_status = []
residence = []
profession = []
date_arrest = []

pages = np.arange(0, 7, 1)
pages


for page in pages: 
### Getting the all the contents of website
  results = requests.get("https://www.addameer.org/prisoner?field_type_of_prisoner_target_id=All&page="+str(page), headers=headers)
  soup = BeautifulSoup(results.text, 'html.parser')
  prisoner_div = soup.find_all('div', class_='views-field views-field-nothing')
  sleep(randint(5,10))
### Initiate the for loop - iterate through every div container
  for container in prisoner_div:
    ### Name
    person = container.find('div', class_='title').a.text if container.find('div', class_='title') else '-'
    name.append(person)
    ### Legal Status
    status = container.find('div', class_='status').text if container.find('div', class_='status') else '-'
    legal_status.append(status)
    ### Residence
    place = container.find('div', class_='residence').text if container.find('div', class_='residence') else '-'
    residence.append(place)
    ### Profession 
    job = container.find('div', class_='prof').text if container.find('div', class_='prof') else '-'
    profession.append(job)
    ### Date of arrest
    date = container.find('div', class_='date date-a').text if container.find('div', class_='date date-a') else '-'
    date_arrest.append(date)
    

### Saving the dataset
dataset_arrest = pd.DataFrame({
'name': name,
'legal_status': legal_status,
'residence': residence,
'profession': profession,
'date_of_arrest': date_arrest,
})

### To have a first look at the dataset
dataset_arrest.head()
print(dataset_arrest.dtypes)

### Cleaning the data
dataset_arrest['legal_status']  = dataset_arrest['legal_status'].apply(lambda x: x[13:] if x!='-' else '-')
dataset_arrest['residence']  = dataset_arrest['residence'].apply(lambda x: x[10:] if x!='-' else '-')
dataset_arrest['profession']  = dataset_arrest['profession'].apply(lambda x: x[11:] if x!='-' else '-')
dataset_arrest['date_of_arrest']  = dataset_arrest['date_of_arrest'].apply(lambda x: x.strip('Date of Arrest\n'))

### Have a look at cleaned data
dataset_arrest
dataset_arrest.iloc[37]


dataset_arrest.to_csv('dataset_arrest.csv')







