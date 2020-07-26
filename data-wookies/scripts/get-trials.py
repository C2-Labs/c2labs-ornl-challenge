#!/usr/bin/python

import sys, getopt, time
import json
import requests
import pgeocode
import trialnlp

def get_coordinates(zipcode):
    nomi = pgeocode.Nominatim('us')
    results = nomi.query_postal_code(zipcode)

    return results

def main(argv):
    arguments = ''
    usage = 'usage: get-trials.py <gender> <age> <zipcode> <distance> <cancerType> <cancerSite> <cancerStage>'
    try:
        opts, args = getopt.getopt(argv,"hf:",["gender=", "age=", "zipcode=", "distance=", "cancerType=", "cancerSite=", "cancerStage="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-f", "--gender", "--age", "--zipcode", "--distance", "--cancerType", "--cancerSite", "--cancerStage" ):
            arguments = arg

    url = "https://datawookies.c2labs.com/es/trials/_search"

    headers = {'accept': '*/*'}
    result_max = 300
    

    gender = sys.argv[1]
    age = sys.argv[2]
    zipcode = sys.argv[3]
    distance = sys.argv[4]
    cancerType = sys.argv[5]
    cancerSite = sys.argv[6]
    cancerStage = sys.argv[7]
    
    #get latitude and longitude from postal code
    search_coordinates = get_coordinates(zipcode)

    query = {"_source": ["nct_id","nci_id","eligibility","anatomic_sites","brief_title"], "size": result_max, "query": {"bool": {"must": [{"range": {"eligibility.structured.min_age_in_years": {"lte": str(age)}}},{"range": {"eligibility.structured.max_age_in_years": {"gte": str(age)}}}], "should": [{"match": {"eligibility.structured.gender": "BOTH"}},{"match": {"eligibility.structured.gender": gender}}],"filter": {"geo_distance" : {"distance" : distance + "mi", "sites.org_coordinates" : "" + str(search_coordinates["latitude"]) + "," + str(search_coordinates["longitude"]) + ""}}}}}

    response = requests.get(url, json=query, headers=headers)
    
    results = []
    trials = []

    if (response.status_code == 200):
        results = response.json()['hits']['hits']

        for item in results:

            anatomic_sites_list = item['_source']['anatomic_sites']

            desc_list = []
            for desc in item['_source']['eligibility']['unstructured']:
                desc_list.append(trialnlp.remove_punc_stopwords(desc.get('description', '')))

            # for desc in desc_list:
            #     print(desc)

            score = trialnlp.get_trial_score(cancerType, cancerSite, cancerStage, anatomic_sites_list, desc_list)
            # print("SCORE=" + str(score))

            trials.append({"nci_id": item['_source']['nci_id'], \
                "nct_id": item['_source']['nct_id'], \
                "title": item['_source']['brief_title'], \
                "score": score, \
                "gender": item['_source']['eligibility']['structured']['gender'], \
                })
    else:
        print ("No Results")

    sorted_trials = sorted(trials, reverse=True, key=lambda i: i['score']) 

    max_res_records = 25
    res_idx = 0
    trial_results = []
    for trial in sorted_trials:
        if res_idx < max_res_records and trial['score'] > .5:
            trial_results.append(trial)
            res_idx = res_idx+1
        

    print (json.dumps(trial_results))

if __name__ == "__main__":
    main(sys.argv[7:])
