#!/usr/bin/env python
# coding: utf-8

# In[4]:


from fuzzywuzzy import fuzz, process
import json
import requests 
from requests.auth import HTTPBasicAuth

# Install the genism Library to help remove stopwords to make analysis easier and faster and possibly more accurate
get_ipython().system('python -m pip install -U gensim')
from gensim.parsing.preprocessing import remove_stopwords


# In[63]:


# Patient Data
# Let a user enter their personal data to make a list of things to search and match with in trial data

p_age = input("Enter your age: ")
p_gender = input("Enter your gender: ")
c_location = input("Where is the cancer located? ")
c_type = input("What is the cancer type? (If cancer's location is skin, is it squamous cell carcinoma or basal cell carcinoma?): ")
c_stage = input("What is the cancer's stage? ")
p_zip_code = input("What is your zip code? ")
max_dis = input("How far are you willing to travel? (miles): ")
patient_data = [p_age,p_gender,c_location,c_type,c_stage,p_zip_code,max_dis]
# create a subset of the patients' cancer data
patient_cancer_data = [c_location, c_type, 'stage ' + c_stage]


# In[64]:


# Importing the trials to test on the patient
url = "https://datawookies.c2labs.com/es/trials/_search"

#Url for connecting to the ELK stack to retrieve the JSON data
#url = "http://20.42.25.27:9200/trials/_doc/NCT00719303_update"

headers = {'accept': '*/*'}

data = {"_source": ["nci_id","eligibility", "anatomic_sites"],"size":50,"query": {"bool" : {"must" : {"match_all" : {}},"filter" : {"geo_distance" : {"distance" : "50km","sites.org_coordinates" : "40,-90"}}}}}


# Getting the JSON data
response = requests.get(url, json=data, headers=headers)

# Instantiate an empty list so that we can load the trials inclusion criteria descriptions
trials = []

# The if statement is used to catch data in the case no data is loaded. Status code 200 = data was found
# The results variable is the set of descriptions extracted from the original JSON data structure. 
# We access it by accessing each specific key within the nested dictionaries and when they are assigned to this variabe,
# they are still in JSON format
if (response.status_code == 200):
    results = response.json()['hits']['hits'] 
    
    # Here we extract the values from the descriptions key in the results variable and add each value to a list to make it 
    # easier to navigate through the data structure
    for item in results:
        trials.append(item)

# This is what prints if there is no data
else:

    print ("No Data")

print(json.dumps(trials, indent=2))


# In[73]:


a_sites = []
ids = []
all_descriptions = [] 
for trial in trials:
    nci_id = trial['_source']['nci_id']
    ids.append(nci_id) 
    sites = (trial['_source']['anatomic_sites'])
    results = trial['_source']['eligibility']['unstructured']
    descriptions = []
    a_sites.append(sites)
    for item in results:
        descriptions.append(item.get('description', ''))
    all_descriptions.append(descriptions)
    print(all_descriptions)
id_and_site = dict(zip(ids,sites))
#print(id_and_site)


# In[74]:


# Remove the punctuation from each description so when we use fuzzy matching it will be more accurate. If we compare
# bob to bob, they are dissimilar by the comma, so this can help with accuracy, and help reducing the number of tokens if
# we wanted to break down this data structure even further
punctuation = '''!()-[]{};:'"\,./?@#$%^&*_~'''
all_desc_no_punc = []

for trial in all_descriptions:
    
    descriptions = []
    
    for desc in trial:
    
        desc_np = ''

        for ch in desc:

            if ch not in punctuation:
                desc_np = desc_np + ch

        descriptions.append(desc_np)
        
    all_desc_no_punc.append(descriptions)

print(all_desc_no_punc)


# In[75]:


# Now we should remove the stopwords from each description, this will help filter out words so we can get better matches
all_filtered_desc = []
for trial in all_desc_no_punc:
    
    descriptions = []
    
    for desc in trial:
        
        df = remove_stopwords(desc)
        descriptions.append(df)
        
    all_filtered_desc.append(descriptions)
    
print(all_filtered_desc)


# In[76]:


# testing the length of each list to see if they can be matched for a dictionary comprehension later
print(len(all_filtered_desc))
print(len(ids))


# In[92]:


# instantiate an empty list to load each trial score to it. This is where we use fuzzy logic to compare strings
# the fuzz library has a few great functions like the token_set_ratio which does some text preprocessing to the strings
# that it is matching. It uses the levenshtein distance measure to calcuate the similarities between strings
# we then later say if the similarity between two strings is above a given threshold, then we will increse the metric by 0.1.
all_scores1 = []
for trial in all_filtered_desc:
    
    cdm = 0
    desc_trial_score = []
    
    for desc in trial:
        
        desc_score = []
        
        for item in patient_cancer_data:
            
            score = fuzz.token_set_ratio(item, desc)
            desc_score.append(score)
            
        desc_trial_score.append(desc_score)

    #print(desc_trial_score)
    
    
    
    for row in desc_trial_score:
        
        for score in row:
            
            if score>70:
                cdm+=0.1
                
    all_scores1.append(cdm)
    
print(all_scores1)
            
            
        
        


# In[93]:


len(all_scores)


# In[96]:


# Dictionary comprehension to link the scores to their respective trial so we can rank them and show the id as well
ids_and_scores = {k:v for (k,v) in zip(ids, all_scores1)}


# In[97]:


# sort the values and then print the key value pair. 
ranked_ids = sorted(ids_and_scores.items() , reverse=True, key=lambda x: x[1])
for elem in ranked_ids:
    print(elem[0] , ':', elem[1])


# In[98]:


# Create a similar data structure (2D array)
trial_c_sites = []
for item in a_sites:
    trial_c_sites.append(item)
print(trial_c_sites)


# In[90]:


# this is the same process we had used on the descriptions, but it's being applied to anatomic sites
all_scores = []
for trial in trial_c_sites:
    
    csm = 0
    trial_score = []
    
    for site in trial:
        
        c_score = fuzz.token_set_ratio(site, c_location)
        trial_score.append(c_score)
        
        if c_score > 65:
            csm+=1
    all_scores.append(csm)
print(all_scores)


# In[91]:


print(len(all_scores))


# In[99]:


# calculate the overall score of each trial by adding their metrics
overall_score = []
for i in range(0, len(all_scores)):
    overall_score.append( all_scores1[i] + all_scores[i])
print(overall_score)


# In[101]:


# this stores the scores and the trial ID into a dictionary and then prints out the trials in order. 
ids_and_overall_scores = {k:v for (k,v) in zip(ids, overall_score)}
ranked_overall_ids = sorted(ids_and_overall_scores.items() , reverse=True, key=lambda x: x[1])
for elem in ranked_overall_ids:
    print(elem[0] , ':', elem[1])


# In[ ]:




