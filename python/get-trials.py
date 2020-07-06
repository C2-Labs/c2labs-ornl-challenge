import requests
import json
import csv
import pgeocode
import sys

def get_coordinates(zipcode):
    nomi = pgeocode.Nominatim('us')
    results = nomi.query_postal_code(zipcode)

    return results

def import_csv_data(input_file):
    input_file = csv.DictReader(open(input_file))
    results = []
    for row in input_file:
        results.append(row)

    return results

def get_clinical_trials(age, gender, postal_code, distance):

    #get latitude and longitude from postal code
    coordinates = get_coordinates(postal_code)

    #limit the amount of results a supplied amount (default is 10, max is 50)
    results_size = 50
    #start the results from a supplied starting point (default is 0)
    results_idx = 0
    #total count of matching results
    results_cnt = 0
    #results list
    results = []
    #trials list 
    trials = []

    url = "https://clinicaltrialsapi.cancer.gov/v1/clinical-trials?size=" + str(results_size) + "&from=" + str(results_idx) + "&include=nct_id&include=eligibility&include=phase&include=diseases&include=arms&current_trial_status=Active&eligibility.structured.gender=BOTH&eligibility.structured.gender=" + gender + "&eligibility.structured.max_age_in_years_gte=" + age + "&eligibility.structured.min_age_in_years_lte=" + age + "&sites.org_coordinates_lat=" + str(coordinates["latitude"]) + "&sites.org_coordinates_lon=" + str(coordinates["longitude"]) + "&sites.org_coordinates_dist=" + distance

    #get the total results count and first 50 records
    response = requests.get(url, headers=api_header)
    if (response.status_code == 200):
        results_cnt = int(response.json()['total'])
        print (str(results_cnt))
        results = response.json()['trials']
        for item in results:
            trials.append(item)

        while (results_idx <= results_cnt):
            results_idx = results_idx + 50
            response = requests.get(url, headers=api_header)
            results_cnt = int(response.content[0])
            results = response.json()['trials']
            for item in results:
                trials.append(item)

    return trials

api_header = {'accept': 'application/json'}

#Import the participates data
participants_file = "../datasets/participants_small.csv"
participants = import_csv_data(participants_file)

distance = '100mi'
participant_trials = []

#Get intial list trials for each participant that meet the basic eligbility requirements 
for item in participants:
    results = {}
    results = {item['particpant_id']: get_clinical_trials(item['age'], item['gender'], item['zipcode'], distance)}
    participant_trials.append(results)


outfile = "../datasets/participant_trials.json" 
file = open(outfile, "w")
file.write(json.dumps(participant_trials, indent=2))  
file.close()

# csv_columns = ["nci_id","nct_id","protocol_id","ccr_id","ctep_id","dcp_id","other_ids__name","other_ids__value","associated_studies__study_id","associated_studies__study_id_type","outcome_measures__name","outcome_measures__description","outcome_measures__timeframe","outcome_measures__type_code","amendment_date","current_trial_status","current_trial_status_date","start_date","start_date_type_code","completion_date","completion_date_type_code","record_verification_date","brief_title","official_title","acronym","keywords","brief_summary","detail_description","classification_code","interventional_model","study_source","accepts_healthy_volunteers_indicator","study_protocol_type","study_subtype_code","study_population_description","study_model_code","study_model_other_text","sampling_method_code","bio_specimen__f1","bio_specimen__f2","bio_specimen__f3","bio_specimen__f4","primary_purpose__primary_purpose_code","primary_purpose__primary_purpose_other_text","primary_purpose__primary_purpose_additional_qualifier_code","phase__phase","phase__phase_other_text","phase__phase_additional_qualifier_code","masking__masking","masking__masking_allocation_code","masking__masking_role_investigator","masking__masking_role_outcome_assessor","masking__masking_role_subject","masking__masking_role_caregiver","principal_investigator","central_contact__central_contact_email","central_contact__central_contact_name","central_contact__central_contact_phone","central_contact__central_contact_type","lead_org","collaborators__name","collaborators__functional_role","sites__contact_email","sites__contact_name","sites__contact_phone","sites__recruitment_status","sites__recruitment_status_date","sites__local_site_identifier","sites__org_address_line_1","sites__org_address_line_2","sites__org_city","sites__org_country","sites__org_email","sites__org_family","sites__org_fax","sites__org_name","sites__org_to_family_relationship","sites__org_phone","sites__org_postal_code","sites__org_state_or_province","sites__org_status","sites__org_status_date","sites__org_tty","sites__org_va","sites__org_coordinates__lat","sites__org_coordinates__lon","anatomic_sites__-","diseases__inclusion_indicator","diseases__lead_disease_indicator","diseases__nci_thesaurus_concept_id","diseases__preferred_name","diseases__display_name","diseases__paths__direction","diseases__paths__concepts__idx","diseases__paths__concepts__label","diseases__paths__concepts__code","diseases__type__001","diseases__type__002","diseases__synonyms__-","diseases__synonyms","diseases__parents__001","diseases__parents__002","diseases__parents__003","biomarkers","minimum_target_accrual_number","eligibility__structured__gender","eligibility__structured__max_age","eligibility__structured__max_age_number","eligibility__structured__max_age_unit","eligibility__structured__min_age","eligibility__structured__min_age_number","eligibility__structured__min_age_unit","eligibility__structured__max_age_in_years","eligibility__structured__min_age_in_years","eligibility__unstructured__display_order","eligibility__unstructured__inclusion_indicator","eligibility__unstructured__description","number_of_arms","arms__arm_name","arms__arm_type","arms__arm_description","arms__interventions__intervention_name","arms__interventions__intervention_type","arms__interventions__intervention_code","arms__interventions__intervention_description","arms__interventions__parents__001","arms__interventions__parents__002","arms__interventions__parents__003","arms__interventions__inclusion_indicator","arms__interventions__synonyms__-","arms__interventions__synonyms","arms__interventions__intervention_category"]

# csv_file = "../dataset/trials.csv"


# try:
#     with open(csv_file, 'w') as csvfile:
#         writer = csv.DictWriter(csvfile)
#         writer.writeheader()
#         for data in results:
#             writer.writerow(data)
# except IOError:
#     print("I/O error" + IOError)