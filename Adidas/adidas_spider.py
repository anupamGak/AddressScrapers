import requests
from json import dump

params = {
	"brand" : "adidas",
	"category" : "store",
	"fields" : "name,street1,street2,addressline,buildingname,postal_code,city,state,country,state",
	"format" : "json",
	"geoengine" : "google",
	"method" : "get",
	"page" : "1",
	"pagesize" : "600",
	"storetype" : "",
	"latlng" : "21.16108585,79.07251014999997,4770"
}

resp = requests.get("http://placesws.adidas-group.com/API/search", params=params)
shopdicts = resp.json()['wsResponse']['result']

shopdump = []
for shopdict in shopdicts:
	if shopdict['country'] == 'IN':
		shop = {}

		addr = shopdict['addressline'].split(",")
		shop['state'] = shopdict['state']
		shop['city'] = shopdict['city']
		shop['location'] = shopdict['street1']
		shop['sublocation'] = ",".join(addr[:-2])
		shop['address'] = shopdict['addressline']
		shop['pincode'] = shopdict['postal_code']

		shopdump.append(shop)

with open('adidas_addr.json', 'w') as f:
	dump(shopdump, f, indent=1)