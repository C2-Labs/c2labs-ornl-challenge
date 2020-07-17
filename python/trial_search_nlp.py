#!/usr/bin/env python
# coding: utf-8

# In[1]:


from fuzzywuzzy import fuzz, process

# Install the genism Library to help remove stopwords to make analysis easier and faster and possibly more accurate
get_ipython().system('python -m pip install -U gensim')
from gensim.parsing.preprocessing import remove_stopwords


# In[2]:


# Importing the NCT00719303 trial, in the future let's import trials by NCI ID.

import json
import requests 
from requests.auth import HTTPBasicAuth


#url = "http://20.42.25.27:9200/trials/_search"

#Url for connecting to the ELK stack to retrieve the JSON data
url = "http://20.42.25.27:9200/trials/_doc/NCT00719303_update"

headers = {'accept': '*/*'}

#data = {"_source": ["nct_id","eligibility"],"query": {"bool" : {"must" : {"match_all" : {}},"filter" : {"geo_distance" : {"distance" : "50km","sites.org_coordinates" : "40,-90"}}}}}
# add anatomic sites^

# Getting the JSON data
response = requests.get(url, headers=headers)

# Instantiate an empty list so that we can load the trials inclusion criteria descriptions
descriptions = []

# The if statement is used to catch data in the case no data is loaded. Status code 200 = data was found
# The results variable is the set of descriptions extracted from the original JSON data structure. 
# We access it by accessing each specific key within the nested dictionaries and when they are assigned to this variabe,
# they are still in JSON format
if (response.status_code == 200):
    results = response.json()['_source']['eligibility']['unstructured'] 
    
    # Here we extract the values from the descriptions key in the results variable and add each value to a list to make it 
    # easier to navigate through the data structure
    for item in results:
        descriptions.append(item.get('description', ''))

# This is what prints if there is no data
else:

    print ("No Data")


#print(json.dumps(descriptions, indent=2))


# In[3]:


# Remove the punctuation from each description so when we use fuzzy matching it will be more accurate. If we compare
# bob to bob, they are dissimilar by the comma, so this can help with accuracy, and help reducing the number of tokens 
punctuation = '''!()-[]{};:'"\,./?@#$%^&*_~'''
desc_no_punc = []

for desc in descriptions:
    
    desc_np = ''
    
    for ch in desc:
        
        if ch not in punctuation:
            desc_np = desc_np + ch
            
    desc_no_punc.append(desc_np)
    
print(desc_no_punc)


# In[4]:


# Now we should remove the stopwords from each description, this will help filter out words so we can get better matches
filtered_desc = []
for desc in desc_no_punc:
    df = remove_stopwords(desc)
    filtered_desc.append(df)
print(filtered_desc)


# In[5]:


#Url for connecting to the ELK stack to retrieve the JSON data
url = "http://20.42.25.27:9200/trials/_doc/NCT00719303_update"

headers = {'accept': '*/*'}


response = requests.get(url, headers=headers)

# Instantiate an empty site list to add the site values
sites = []

#The results variable is the set of anatomic site(s) extracted from the original JSON data structure. 
# We access it by accessing each specific key within the nested dictionaries and when they are assigned to this variabe,
# they are still in JSON format, but anatomic sites is a list so it's a more simple structure to access
if (response.status_code == 200):
    results = response.json()['_source']['anatomic_sites']   
    
    # Add each anatomic site
    for item in results:
        sites.append(item)
        
else:

    print ("No Data")


print(json.dumps(sites, indent=2))


# In[6]:


# Let a user enter their personal data to make a list of things to search and match with in trial data
patient_data = []
def get_data():
    p_age = input("Enter your age: ")
    p_gender = input("Enter your gender: ")
    c_location = input("Where is the cancer located? ")
    c_type = input("What is the cancer type? (If cancer's location is skin, is it squamous cell carcinoma or basal cell carcinoma?): ")
    c_stage = input("What is the cancer's stage? ")
    p_zip_code = input("What is your zip code? ")
    max_dis = input("How far are you willing to travel? (miles): ")


# In[12]:


patient_cancer_data = [c_location, c_type, 'stage II' + c_stage]


# In[13]:


scores = []
for desc in filtered_desc:
    
    desc_scores = []
    
    for item in patient_cancer_data:
        
        desc_score = fuzz.token_set_ratio(item,desc)
        
        desc_scores.append(desc_score)        
    #print(desc_scores)
    scores.append(desc_scores)    
print(scores)


# In[15]:


cdm = 0
for row in scores:
    
    for score in row:
        
        if score >= 70:
            cdm += 0.1
print(cdm)


# In[11]:


csm = 0
loc_scores = []
for site in sites:

    site_score = fuzz.token_set_ratio(c_location,site)
    loc_scores.append(site_score)
    if site_score > 65:
        csm += 1
print(csm)


# In[16]:


final = csm + cdm
print(final)


# In[ ]:




