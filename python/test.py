import pgeocode

zipcode = 78736

nomi = pgeocode.Nominatim('us')
results = nomi.query_postal_code(zipcode)

print (results)