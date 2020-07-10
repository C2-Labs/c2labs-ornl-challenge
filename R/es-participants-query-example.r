library(httr)
library(jsonlite)

url = "http://20.42.25.27:9200/participants/_search"

# query = '{"_source": ["nci_id","eligibility","anatomic_sites"],"query": {"bool" : {"must" : {"match_all" : {}},"filter" : {"geo_distance" : {"distance" : "50km","sites.org_coordinates" : "40,-90"}}}}}'

res = GET(url)

participantsRaw<-fromJSON(rawToChar(res$content))

participants<-participantsRaw[['hits']][['hits']]

participants