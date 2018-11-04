import requests
import pprint

url = ('https://newsapi.org/v2/everything?'
       'q=Apple&'
       'from=2018-11-04&'
       'to=2018-11-04&'
       'sortBy=popularity&'
       'apiKey=secret')

r = requests.get(url)

pprint.pprint(r.json()['articles'][0])