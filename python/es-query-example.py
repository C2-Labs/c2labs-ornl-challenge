import json
import requests
from requests.auth import HTTPBasicAuth



url = "https://datawookies.c2labs.com/es/trials/_search"

headers = {'accept': '*/*'}

data = {"_source": ["nct_id","nci_id","eligibility","sites","brief_title"],"query": {"bool" : {"must" : {"match_all" : {}},"filter" : {"geo_distance" : {"distance" : "500km","sites.org_coordinates" : "40,-90"}}}}}

response = requests.get(url, json=data, headers=headers)


trials = []
if (response.status_code == 200):
    results = response.json()['hits']['hits']
    
    for item in results:
        trials.append({"nci_id": item['_source']['nci_id'], \
            "nct_id": item['_source']['nct_id'], \
            "title": item['_source']['brief_title'], \
            "location": item['_source']['sites'][0]['org_name'], \
            "contact_email": item['_source']['sites'][0]['contact_email'], \
            "contact_phone": item['_source']['sites'][0]['contact_phone'], \
            })

else:
    print ("No Data")


print(json.dumps(trials))
