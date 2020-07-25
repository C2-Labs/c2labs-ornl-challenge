#!/usr/bin/python

from fuzzywuzzy import fuzz, process
from gensim.parsing.preprocessing import remove_stopwords

# Remove the punctuation from each description so when we use fuzzy matching it will be more accurate. If we compare
# bob to bob, they are dissimilar by the comma, so this can help with accuracy, and help reducing the number of tokens if
# we wanted to break down this data structure even further
#
# Removing all stopwords as well
def remove_punc_stopwords(item):
    punctuation = '''!()-[]{};:'"\,./?@#$%^&*_~'''
    item_np = ""

    for ch in item:
        if ch not in punctuation:
            item_np = item_np + ch
    item_np = remove_stopwords(item_np)

    return item_np

def score_descriptions(participant_data, description_list):
    cdm = 0
    desc_scores = []
    
    for desc in description_list:
        
        desc_score = []
        
        for item in participant_data:
            
            score = fuzz.token_set_ratio(item, desc)
            desc_score.append(score)
            
        desc_scores.append(desc_score)


    for row in desc_scores:
        for score in row:
            if score>70:
                cdm+=0.1
                
    # print("CDM = " + str(cdm))
    
    return cdm

def score_anatomic_sites(cancer_site, anatomic_sites_list):
    csm = 0
    site_scores = []
    
    for site in anatomic_sites_list:
        
        score = fuzz.token_set_ratio(site, cancer_site)
        site_scores.append(score)
        
        if score > 65:
            csm+=1
                
    # print("CSM = " + str(csm))
    
    return csm


def get_trial_score(cancer_type, cancer_site, cancer_stage, anatomic_sites_list, description_list):
    participant_data = [cancer_site, cancer_type, cancer_stage]
    score = 0

    cdm = score_descriptions(participant_data, description_list)
    csm = score_anatomic_sites(cancer_site, anatomic_sites_list)
    
    score = cdm + csm

    return score

