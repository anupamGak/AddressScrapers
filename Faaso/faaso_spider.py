import requests
from lxml import html
import re
from json import dump

reLmark = re.compile("(?:next to|near|beside|(?<=[ ,])opp).+?(?=,|$)", re.IGNORECASE)

resp = requests.get("https://www.faasos.com/location.aspx")
page = html.fromstring(resp.text)

cities = page.xpath("//li[@class='rcbItem ']/text()")[1:9]

shopdump = []
for city in cities:
	print "Processing city : " + city

	resp = requests.get("https://www.faasos.com/%sstore.aspx" % city)
	page = html.fromstring(resp.text)

	loclist = page.xpath("//li[@class='rcbItem ']/text()")
	locs = []
	for x in loclist[-1::-1]:
		if not x == "Select Store":
			locs.append(x)
		else:
			break

	for loc in locs:
		resp = requests.get("https://www.faasos.com/%s.aspx" % loc)
		page = html.fromstring(resp.text)

		shop = {}
		shop['city'] = city
		shop['locality'] = loc

		addr = page.xpath("//span[@id='ctl00_ContentPlaceHolder1_lblAddress']/text()")

		if addr == [] or not re.search("\w", addr[0]):
			shop['address'] = "!! Address not available !!"
			shop['sublocality'] = ""
			shop['landmark'] = ""
		else:
			shop['address'] = addr[0]
			shop['landmark'] = ",".join(re.findall(reLmark, addr[0]))
			addr = re.sub(reLmark, "", addr[0])
			addr = addr.split(",")
			addr = [x for x in addr if re.search("\w", x)]
			shop['sublocality'] = addr[-1]

		shopdump.append(shop)

with open('faaso_addr.json', 'w') as f:
	dump(shopdump, f, indent=1)