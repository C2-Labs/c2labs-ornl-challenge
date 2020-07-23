import json
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import csv
from itertools import zip_longest



url = "https://datawookies.c2labs.com/es/trials/_search"

headers = {'accept': '*/*'}

search_coordinates = "37.7402,-122.171"

data = {"_source": ["nct_id","nci_id","eligibility","anatomic_sites"],"size": "250","query": {"bool" : {"must" : {"match_all" : {}},"filter" : {"geo_distance" : {"distance" : "2000mi","sites.org_coordinates" : "37.7402,-122.171"}}}}}

response = requests.get(url, json=data, headers=headers)


results = []
trials = []
if (response.status_code == 200):
    results = response.json()['hits']['hits']
    
    for item in results:
        nci_id = item['_source']['nci_id']
        
        # nct_id = item['_source']['nct_id']
        # anatomic_site = item['_source']['anatomic_sites']
        # anatomic_sites.append({nci_id: anatomic_site})
        # desc_list = item['_source']['eligibility']['unstructured'][0]['description']
        # descriptions.append({nci_id: desc_list})
        # anatomic_sites = item['_source']['anatomic_sites']
        # descriptions = item['_source']['eligibility']['unstructured'][0]['description']
        # trial([nci_id]['anatomic_sites']).update(anatomic_sites)
        # print(trial)

        d_list = item['_source']['eligibility']['unstructured']
        description_list = {}

        a_list = item['_source']['anatomic_sites']
        anatomic_site_list = {}
  
        for index, a in enumerate(a_list):
            anatomic_site_list["anatomic_site_" + str(index)] = a
        
        for index, d in enumerate(d_list):
            description_list["description_" + str(index)] = d.get("description", "")

        trial = {"nci_id": nci_id}
        trial.update(anatomic_site_list)
        trial.update(description_list)
            

        trials.append(trial)


        


else:

    print ("No Data")


print(json.dumps(trials, indent=2))

# df = pd.read_json (trials)
df = pd.DataFrame(trials).fillna(0)
# df = pd.DataFrame(trials)
pd.DataFrame()
# df = df.T
export_csv = df.to_csv (r'../datasets/trials_flatten.csv', index = False, header=True)
# outfile = "../datasets/trials_filtered.json" 
# file = open(outfile, "w")
# file.write(json.dumps(trials, indent=2))  
# file.close()

