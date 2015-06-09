import requests
import re
from json import dump

reCity = re.compile(r'(?<=\\")[\(\) A-Z]+(?=\\")')
reUni = re.compile('&\w+;')
reLmark = re.compile(r'(?<=[^A-Z])(?:OPP|NEAR|NXT|NEXT|NR).+?(?=,|$)')

shopdump = []
baseURL = "http://www.benetton.com/storelocator/map_ajax.php?country=India&city=%s&adutl=+01&kids=+02&undercolor=+06&togetmap=mapdata"

page = requests.get("http://world.benetton.com/storelocator/map_ajax.php?country_code=India&toget=citylist")
cities = re.findall(reCity, page.text)

for city in cities:
	print "Processing city : " + city
	cityurl = city.replace(" ", "+")
	page = requests.get(baseURL % cityurl)
	annealed = page.text.replace("\/", "")
	annealed = re.sub(reUni, "", annealed)
	modcity = city.replace("(", "\(")
	modcity = modcity.replace(")", "\)")
	addresses = re.findall('(?<=%sbbr).+?(?=br)' % modcity, annealed)

	for address in addresses:
		shop = {}
		shop['address'] = address
		if re.search(reLmark, address):
			shop['landmark'] = " ".join(re.findall(reLmark, address))
			address = re.sub(reLmark, "", address)
		else:
			shop['landmark'] = ""

		arr = address.split(",")
		farr = []
		for x in arr:
			if re.search(r"\w", x):
				farr.append(x)

		shop['location'] = farr[-1]
		shop['sublocation'] = ",".join(farr[:-1])
		shop['city'] =  city
		shopdump.append(shop)

with open('ucb_addr.json', 'w') as f:
	dump(shopdump, f, indent=1)