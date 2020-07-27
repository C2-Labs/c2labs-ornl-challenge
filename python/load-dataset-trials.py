import json
import csv
import pgeocode
import sys
import requests
from requests.auth import HTTPBasicAuth

api_header = {'accept': 'application/json'}

def get_coordinates(zipcode):
    nomi = pgeocode.Nominatim('us')
    results = nomi.query_postal_code(zipcode)

    return results


def insert_es_data(idx, data):

    url = 'https://datawookies.c2labs.com/es/trials/_doc/' + idx +'_update/'
    headers = {'accept': '*/*'}
    response = requests.post(url, json=data, headers=headers)
    print(response.content)

def import_list_data(input_file):
    with open(input_file) as f:
        results = f.read().splitlines()

    return results



#Import the dataset1 trial nci_id's
trials_list = import_list_data("../datasets/dataset1_trials.txt")

#Query the clinical trials api for each nci_id in the list
for trial in trials_list:
    url = "https://clinicaltrialsapi.cancer.gov/v1/clinical-trial/" + trial
    response = requests.get(url, headers=api_header)

    if (response.status_code == 200):
        res = response.json()
        print (res['nct_id'])
        insert_es_data(res['nct_id'], res)






