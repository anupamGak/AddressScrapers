from lxml import html
import requests
from json import dump

URL = "https://www.nissan.in/content/nissan/en_IN/index/find-a-dealer/jcr:content/freeEditorial/columns12/col1-par/find_a_dealer.extended_dealers_by_location.json?_charset_=utf-8&page=1&size=179"
dealerdump = []

resp = requests.get(URL)
details = resp.json()['dealers']

for detail in details:
	dealer = {}
	dealer['name'] = detail['tradingName']
	dealer['address'] = detail['address']
	dealer['lat'] = detail['geolocation']['latitude']
	dealer['long'] = detail['geolocation']['longitude']
	dealerdump.append(dealer)

with open('nissan_addr.json', 'w') as f:
	dump(dealerdump, f, indent=1)