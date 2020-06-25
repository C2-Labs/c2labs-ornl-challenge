import requests
import json
import csv


api_header = {'accept': 'application/json'}

trial_ids = ["NCT00392327","NCT00632853","NCT00719303","NCT00492778","NCT00001337","NCT00576654","NCT01012817","NCT00956007",\
    "NCT00887146","NCT00983697","NCT00980954","NCT00981656","NCT00980460","NCT01013649","NCT02085408","NCT01042522","NCT01096368",\
    "NCT01118026","NCT01101451","NCT02589938","NCT01366144","NCT01051635","NCT01226940","NCT01386385","NCT01381718","NCT01190930",\
    "NCT01231906","NCT01272037","NCT01275664","NCT01359592","NCT01368588","NCT01434316","NCT02883049","NCT01497444","NCT01503632",\
    "NCT01503086","NCT01515787","NCT01333046","NCT01556243","NCT01573442","NCT01587352","NCT01585805","NCT01638533","NCT01775475",\
    "NCT01695941","NCT01595061","NCT01602666","NCT01622868","NCT01649089","NCT01674140"]

results = []

for item in trial_ids:
    url = "https://clinicaltrialsapi.cancer.gov/v1/clinical-trial/" + item
    response = requests.get(url, headers=api_header)
    if (response.status_code == 200):
        results.append(response.json())

outfile = "../datasets/trials.json" 
file = open(outfile, "w")
file.write(json.dumps(results, indent=2))  
file.close()

