import requests
import pprint

map_key = "YOUR_API_KEY"

url = ("https://maps.googleapis.com/maps/api/place/findplacefromtext/json")
params = { "input" : "mckinsey" + " HQ california",
           "inputtype" : "textquery",
           "fields":"photos,formatted_address,name,rating,opening_hours,geometry",
           "key":map_key} 

r = requests.get(url, params=params)

pprint.pprint(r.json())

if r.json()['status'] == 'ZERO_RESULTS':
    print("Blah!")



# r2 = requests.get(url2)

# pprint.pprint(r2.json())

# if r2.json()['status'] == 'ZERO_RESULTS':
#     print("Blah!")