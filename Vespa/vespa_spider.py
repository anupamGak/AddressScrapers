from lxml import html
import requests
import json
import re

reLmark = re.compile(r'(?:Opp|near|next to|beside|nr|adj to|diagonal|lm\s?:?)[^0-9]+?,', re.IGNORECASE)

headers = {
	"Content-type" : "application/json"
}
data = {}
page = requests.post("http://www.vespa.in/our-store/ourstore.aspx/Getstate", data=data, headers=headers)
statedicts = page.json()['d']

dealerdump = []

for statedict in statedicts:
	if not statedict['State']:
		continue
	print statedict['State']
	data = {
		"State" : statedict['State']
	}
	page = requests.post("http://www.vespa.in/our-store/ourstore.aspx/Getcity", data=json.dumps(data), headers=headers)
	citydicts = page.json()['d']
	for citydict in citydicts:
		data = {
			"city" : citydict['City']
		}
		page = requests.post("http://www.vespa.in/our-store/ourstore.aspx/Getdealers", data=json.dumps(data), headers=headers)
		dealerdicts = page.json()['d']

		for dealerdict in dealerdicts:
			dealerdict.pop("__type")
			dealerdict.pop("Dealer_id")
			dealerdict.pop("contact")
			dealerdict["Landmark"] = " ".join(re.findall(reLmark, dealerdict["Address"]))
			dealerdict["Address"] = re.sub(reLmark, "", dealerdict["Address"])
			try:
				dealerdict["Location"] = dealerdict["Address"].split(",")[-2]
			except IndexError:
				dealerdict["Location"] = dealerdict["Address"].split(",")[-1]

			try:
				dealerdict["Sublocation"] = dealerdict["Address"].split(",")[-3]
			except IndexError:
				dealerdict["Location"] = ""
			dealerdict['State'] = statedict['State']
			dealerdict['City'] = citydict['City']

			dealerdump.append(dealerdict)

with open('vespa_addr.json', 'w') as f:
	json.dump(dealerdump, f, indent=1)