library(httr)
library(jsonlite)

url = "http://20.42.25.27:9200/trials/_doc/NCT00392327_update"

# query = '{"_source": ["nci_id","eligibility","anatomic_sites"],"query": {"bool" : {"must" : {"match_all" : {}},"filter" : {"geo_distance" : {"distance" : "50km","sites.org_coordinates" : "40,-90"}}}}}'

res = GET(url)

# res = GET(url, body=query, encode = 'json')

# rawToChar(res$content)
data = fromJSON(rawToChar(res$content))

data