import requests
from json import dump
import re

reLmark = re.compile("(?:next to|near|beside| opp).+?(?=,|$)", re.IGNORECASE)

params = {
	"method" : "get",
	"brand" : "reebok",
	"category" : "store",
	"latlng" : "20.646919,81.471062,1964",
	"geoengine" : "google",
	"pagesize" : "500",
	"page" : "1",
	"format" : "json"
}

resp = requests.get("https://placesws.adidas-group.com/API/search", params=params)
storedicts = resp.json()['wsResponse']['result']

shopdump = []
for sdict in storedicts:
	if sdict['country'] == "IN":
		shop = {}
		shop['state'] = sdict['state']
		shop['name'] = sdict['name']
		shop['city'] = sdict['city']
		shop['sublocality'] = sdict['street1']

		try:
			shop['pincode'] = sdict['postal_code']
		except KeyError:
			shop['pincode'] = ""

		try:
			shop['address'] = sdict['addressline']

		except KeyError:
			shop['address'] = sdict['street1']
			shop['locality'] = sdict['street1']

		address = shop['address']
		shop['landmark'] = ", ".join(re.findall(reLmark, address))
		address = re.sub(reLmark, "", address)
		addr = address.split(", ")
		addarr = []
		for a in addr:
			if re.search("\w", a):
				addarr.append(a)
		try:
			shop['locality'] = addarr[-1]
		except IndexError:
			shop['locality'] = ""
		shop['address'] = ", ".join(addarr)

		shopdump.append(shop)

with open('rbk_addr.json', 'w') as f:
	dump(shopdump, f, indent=1)
print "Done!"