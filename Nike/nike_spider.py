import requests
from json import dump

params = {
	"brandsExclude" : "JO,CI,CH,CT,CO",
	"format" : "JSON",
	"nike_owned_filter" : "true",
	"type" : "limited"
}

baseURL = "http://www.nike.com/store-locator/locations"

shopdump = []
lon = 68
while lon <= 93:
	params['sw_lon'] = lon
	params['ne_lon'] = lon + 4

	lat = 8
	while lat <= 34:
		params['sw_lat'] = lat
		params['ne_lat'] = lat + 2

		page = requests.get(baseURL, params=params)
		shopdicts = page.json()['locations']

		for shopdict in shopdicts:
			shop = {}
			address = shopdict['street']
			address = address.split(",")

			shop['state'] = shopdict['stateName']
			shop['city'] = shopdict['city']
			shop['address'] = shopdict['street']
			shop['pincode'] = shopdict['postalCode']
			shop['location'] = shopdict['name']
			shop['sublocation'] = ",".join(address[:-2])
			shop['latitude'] = shopdict['geoLat']
			shop['longitude'] = shopdict['geoLon']

			shopdump.append(shop)
		lat += 2

		try:
			print "Grazing somewhere around :" + shop['state']
		except NameError:
			print "Grazing in the ocean!"
	lon += 4

with open('nike_addr.json', 'w') as f:
	dump(shopdump, f, indent=1)