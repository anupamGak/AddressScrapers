import requests
import re
import itertools
from hetph_item import Address
import json

addump = []

jsc = requests.get("http://www.heteropharmacy.com/jScript/myScript.js")
code = jsc.text

reCity = re.compile("(?<=\[')[a-z]+(?='\])", re.IGNORECASE)		#16
reCitygrp = re.compile('(?<=]= new Array)[\w\W]+?(?=\);)')		#15
reAddr = re.compile('(?<=")[A-Z].+#.+(?=")')

cities = re.findall(reCity, code)
cities.pop(-1)

citygrps = re.findall(reCitygrp, code)

for city, citygrp in itertools.izip(cities,citygrps):
	addrs = re.findall(reAddr, citygrp)
	print city
	for addr in addrs:
		shop = Address()
		pcs = addr.split("#")
		shop.addr = pcs[-1]
		shop.area = pcs[0]
		shop.city = city
		addump.append(shop.__dict__)

f = open('hetph_addr.json', 'w')
json.dump(addump, f, indent=1)