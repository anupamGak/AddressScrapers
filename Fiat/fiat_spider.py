import requests
import json
import re

reState = re.compile('(?<="state": ")[\w\s]*')
reCity = re.compile('(?<="city": ")[\w\s]*')
reName = re.compile('(?<="dealer_name": ")[\w\s]*')
rePin = re.compile('(?<="pincode": ")[\d\s]*')
rePinadd = re.compile('\d{3}\s?\d{3}')
reAddr1 = re.compile('(?<="address1": ").*')
reAddr2 = re.compile('(?<="address2": ").*')
reAddr3 = re.compile('(?<="address3": ").*')
reAddr4 = re.compile('(?<="address4": ").*')
reLat = re.compile('(?<="latitude": ").*')
reLong = re.compile('(?<="longitude": ").*')

dealerdump = []

resp = requests.get("http://www.fiat-india.com/data/dealers.js")
jsdata = resp.text.replace(" var DealersList =", "")
jsondata = json.loads(jsdata)
jsondata = jsondata['city']

states = re.findall(reState, jsdata)
cities = re.findall(reCity, jsdata)
names = re.findall(reName, jsdata)
pins = re.findall(rePin, jsdata)
addr1 = re.findall(reAddr1, jsdata)
addr2 = re.findall(reAddr2, jsdata)
addr3 = re.findall(reAddr3, jsdata)
addr4 = re.findall(reAddr4, jsdata)
lats = re.findall(reLat, jsdata)
longs = re.findall(reLong, jsdata)

for i in range(173):
	dealer = {}
	dealer['state'] = states[i]
	dealer['name'] = names[i]
	if pins[i]:
		dealer['pin'] = pins[i]
	elif re.search(rePinadd, addr1[i]):
		dealer['pin'] = re.findall(rePinadd, addr1[i])[0]
	elif re.search(rePinadd, addr2[i]):
		dealer['pin'] = re.findall(rePinadd, addr2[i])[0]
	elif re.search(rePinadd, addr3[i]):
		dealer['pin'] = re.findall(rePinadd, addr3[i])[0]
	elif re.search(rePinadd, addr4[i]):
		dealer['pin'] = re.findall(rePinadd, addr4[i])[0]
	else:
		dealer['pin'] = ""

	dealer['city'] = cities[i]
	dealer['address'] = addr1[i] + addr2[i] + addr3[i] + addr4[i]
	dealer['lat'] = lats[i]
	dealer['long'] = longs[i]
	dealerdump.append(dealer)

with open('addr.json', 'w') as f:
	json.dump(dealerdump, f, indent=1)