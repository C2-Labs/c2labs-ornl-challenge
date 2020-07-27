import json
import csv
import sys
import re
import pgeocode
import requests
from requests.auth import HTTPBasicAuth



def import_csv_data(input_file):
    input_file = csv.DictReader(open(input_file))
    results = []
    for row in input_file:
        results.append(row)

    return results

def get_coordinates(zipcode):
    nomi = pgeocode.Nominatim('us')
    results = nomi.query_postal_code(zipcode)
    return results

def clean(val):
    res_list = []
    t1 = val.split('OR')
    for item in t1:
        t2 = item.split('=')
        if (len(t2) > 0):
            res_list.append(t2[0].strip().replace('(', ''))
    res = ','.join(res_list)
    return res

def clean_history(val):
    res_list = []
    t1 = val.split(';')
    for item in t1:
        if ("YES" in item):
            t2 = item.split('=')
            if (len(t2) > 0):
                res_list.append(t2[0].strip().replace('(', '').replace(')', '').replace('PRIOR ', ''))
    res = ','.join(res_list)
    return res

def clean_hb(val):
    res = ""
    t1 = val.split('=')
    if (len(t1) > 0):
        res = t1[1].strip().replace('(', '').replace(')', '')
    return res

def clean_ps(val):
    res = {}
    if ("ECOG" in val):
        ps_type = "ECOG"
    elif ("Karnofsky" in val):
        ps_type = "Karnofsky"
    elif ("Zubrod" in val):
        ps_type = "Zubrod"
    else:
        ps_type = ""
    
    ps_comparator = re.findall(r'([<>]=?|=|[<>])', val)
    ps_value = re.findall(r'(\d+)', val)
    res.update({'ps_type': ps_type, 'ps_comparator': ''.join(ps_comparator), 'ps_value': ''.join(ps_value)})

    return res

def clean_ps_code(val):
    res = ""
    t1 = val.split(' ')
    if (len(t1) > 0):
        res = t1[0].strip().replace('(', '').replace(')', '')
    return res

def clean_zipcode(val):
    res = {}
    t1 = val.split('=')
    if (len(t1) > 0):
        res.update({'zipcode_code': t1[0].strip().replace('(', '').replace(')', '')})
        res.update({'zipcode': t1[1].strip().replace('(', '').replace(')', '')})
    return res

def clean_specific_treatment(val):
    res = ""
    t1 = val.split('=')
    if (len(t1) > 0):
        res = t1[0].strip().replace('(', '').replace(')', '')
    return res

def insert_es_data(id_idx, data):
  
    url = 'https://datawookies.c2labs.com/es/participants/_doc/' + str(id_idx) + '_update/'
    headers = {'accept': '*/*'}
    # response = requests.post(url, json=data, headers=headers, auth=HTTPBasicAuth('elastic', 'pzs5iFdMGK5jS8U84akV'))
    response = requests.post(url, json=data, headers=headers)

    print (response.content)

#Import the participates data
participants_file = "../datasets/participants.csv"
participants = import_csv_data(participants_file)

participants_data = []
id_idx = 1
for item in participants:
    details = {}

    cancer_site = clean(item['Cancer Site 1 text'])
    cancer_site_code = clean(item['Cancer Site 1 Boolean'])
    stage = clean(item['Stage Text'])
    stage_code = clean(item['Stage Boolean'])
    treatment_history = clean_history(item['Treatment History Text'])
    treatment_history_code = clean_history(item['Treatment History Boolean'])
    gender = clean(item['Gender'])
    gender_code = clean(item['Gender Boolean'])
    age = int(item['AGE'].strip())
    hb = int(clean_hb(item['HB Text']))
    hb_code = clean(item['HB Boolean'])
    hb_code_value = clean_hb(item['HB Boolean'])
    platelet = int(item['Platelet Text'].strip().replace(',',''))
    platelet_code = clean(item['Platelet Boolean'])
    platelet_code_value = clean_hb(item['Platelet Boolean'])
    wbc = int(item['WBC Text'].strip().replace(',',''))
    ps_data = clean_ps(item['Performance Status (PS)'])
    ps_code = clean_ps_code(item['PS Boolean'])
    postal_code_data = clean_zipcode(item['Synthetic Zip Code Boolean'])
    specific_treatment = clean(item['Specific treatment/trial text'])
    specific_treatment_code = clean(item['Specific treatment trial Boolean'])
    trial_type = clean(item['Type of Trial Text'])
    trial_type_code = clean(item['Type of Trial Boolean'])
    coordinates = get_coordinates(postal_code_data['zipcode'].strip())
    location = {'lat': coordinates["latitude"], 'lon': coordinates["longitude"] }


    details = { 'particpant_id': id_idx, \
        'cancer_site': cancer_site, \
        'cancer_site_code': cancer_site_code, \
        'stage': stage, \
        'stage_code': stage_code, \
        'treatment_history': treatment_history, \
        'treatment_history_code': treatment_history_code, \
        'gender': gender, \
        'gender_code': gender_code, \
        'age': age, \
        'hb': hb, \
        'hb_code': hb_code,\
        'hb_code_value': hb_code_value, \
        'platelet': platelet,\
        'platelet_code': platelet_code,\
        'platelet_code_value': platelet_code_value, \
        'wbc': wbc, \
        'ps_type': ps_data['ps_type'], \
        'ps_comparator': ps_data['ps_comparator'], \
        'ps_value': ps_data['ps_value'], \
        'ps_code': ps_code, \
        'zipcode': postal_code_data['zipcode'].strip(), \
        'zipcode_code': postal_code_data['zipcode_code'], \
        'specific_treatment': specific_treatment, \
        'specific_treatment_code': specific_treatment_code, \
        'trial_type': trial_type, \
        'trial_type_code': trial_type_code,\
        'location': location}

    insert_es_data(id_idx, details)

    id_idx = id_idx + 1
    participants_data.append(details)

print(json.dumps(participants_data, indent=2))

json_file = "../datasets/participants_clean.json" 
file = open(json_file, "w")
file.write(json.dumps(participants_data, indent=2))  
file.close()

# fields = ['particpant_id','cancer_site','cancer_site_code','stage','stage_code','treatment_history','treatment_history_code','gender','gender_code','age','hb','hb_code','hb_code_value','platelet','platelet_code','platelet_code_value','wbc','ps_type','ps_comparator','ps_value','ps_code','zipcode','zipcode_code','specific_treatment','specific_treatment_code','trial_type','trial_type_code']

# csv_file = "../datasets/participants_clean.csv"

# # writing to csv file  
# with open(csv_file, 'w') as csvfile:  
#     # creating a csv dict writer object  
#     writer = csv.DictWriter(csvfile, fieldnames = fields)  
        
#     # writing headers (field names)  
#     writer.writeheader()  
        
#     # writing data rows  
#     writer.writerows(participants_data)  