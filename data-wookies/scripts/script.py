#!/usr/bin/python

import sys, getopt, time
import json
import requests

def main(argv):
    argument = ''
    usage = 'usage: script.py -f <sometext>'
    try:
        opts, args = getopt.getopt(argv,"hf:",["foo="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-f", "--foo"):
            argument = arg

    url = "https://datawookies.c2labs.com/es/trials/_search"

    headers = {'accept': '*/*'}

    search_coordinates = "37.7402,-122.171"

    lat = "41.6103"
    lon = "-87.6534"
    gender = "FEMALE"
    age = 46

    data = {"_source": ["nct_id","nci_id","eligibility","anatomic_sites","sites","brief_title"], "size": 10, "query": {"bool" : {"must" : {"match_all" : {}},"filter" : {"geo_distance" : {"distance" : "1000mi","sites.org_coordinates" : "" + lat + "," + lon + ""}}}}}

    response = requests.get(url, json=data, headers=headers)
    
    results = []
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
                "matching_score": "", \
                })
    else:
        print ("No Data")

    print (json.dumps(trials))

if __name__ == "__main__":
    main(sys.argv[1:])
