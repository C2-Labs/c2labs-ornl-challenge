import json
import csv
import pgeocode
import sys
import requests
from requests.auth import HTTPBasicAuth

def get_coordinates(zipcode):
    nomi = pgeocode.Nominatim('us')
    results = nomi.query_postal_code(zipcode)

    return results


def insert_es_data(idx, data):

    url = 'http://20.42.25.27:9200/trials/_doc/' + idx +'_update/'
    headers = {'accept': '*/*'}
    response = requests.post(url, json=data, headers=headers, auth=HTTPBasicAuth('elastic', 'pzs5iFdMGK5jS8U84akV'))
    print(response.content)

api_header = {'accept': 'application/json'}

#limit the amount of results a supplied amount (default is 10, max is 50)
results_size = 10
#start the results from a supplied starting point (default is 0)
results_idx = 0
#total count of matching results
results_cnt = 0
url = "https://clinicaltrialsapi.cancer.gov/v1/clinical-trials?size=" + str(results_size) + "&from=" + str(results_idx) + "&current_trial_status=Active"
#get the total results count and first 50 records
response = requests.get(url, headers=api_header)

if (response.status_code == 200):
    # results_cnt = int(response.json()['total'])
    results_cnt = int(response.json()['total'])
    print(results_cnt)
   
    results = response.json()['trials']
    for item in results:
        insert_es_data(item['nct_id'], item)

    while (results_idx <= results_cnt):
        results_idx = results_idx + 10
        url = "https://clinicaltrialsapi.cancer.gov/v1/clinical-trials?size=" + str(results_size) + "&from=" + str(results_idx) + "&current_trial_status=Active"
        print(url)
        response = requests.get(url, headers=api_header)
        results = response.json()['trials']
        for item in results:
            insert_es_data(item['nct_id'], item)





