import json
import requests
from requests.auth import HTTPBasicAuth



url = "http://20.42.25.27:9200/trials/_search"

headers = {'accept': '*/*'}

data = {"_source": ["nci_id","eligibility"],"query": {"bool" : {"must" : {"match_all" : {}},"filter" : {"geo_distance" : {"distance" : "50km","sites.org_coordinates" : "40,-90"}}}}}

response = requests.get(url, json=data, headers=headers)

descriptions = []
if (response.status_code == 200):
    results = response.json()['hits']['hits']
    
    for item in results:
        desc_list = []
        nci_id = item['_source']['nci_id']
        desc_list = item['_source']['eligibility']['unstructured'][0]['description']
        descriptions.append({nci_id: desc_list})
        # print (json.dumps(t1, indent=2))
else:

    print ("No Data")


print(json.dumps(descriptions, indent=2))
