import requests
import re
from json import dump

reLmark = re.compile(ur"(?<![a-z])(?:next to|near|beside|opp).+?(?=,|$)", re.IGNORECASE)

data = {
	"latLongString" : "21.1458004,79.08815460000005",
	"Radius" : "1500.0",
	"BranchServices" : "",
	"ATMServices" : ""
}

resp = requests.post("http://maps.icicibank.com/mobile/LEPTON/Handlers/SVCHandler.ashx?Task=GetBranchData", data=data)
page = resp.text.encode("ascii", 'ignore')
page = page.replace("<br/>", "")
page = page.replace("^^", "^")
details = page.split("$")

branchdump = []
for detail in details:
	branch = {}

	detail = detail.split("^")
	while len(detail) < 12:
		detail.append('')
	detail = detail[:-4]
	
	branch['lat'] = detail.pop(0)
	branch['long'] = detail.pop(0)
	branch['name'] = detail.pop(0)
	branch['address'] = detail
	branch['address'].pop(-3)
	branch['address'] = ", ".join(branch['address'])

	branch['pincode'] = detail.pop()
	branch['state'] = detail.pop()
	branch['city'] = detail.pop()

	branch['locality'] = detail.pop()
	branch['landmark'] = "".join(re.findall(reLmark, branch['locality']))
	branch['locality'] = re.sub(reLmark, "", branch['locality'])

	try:
		branch['sublocality'] = detail.pop()
		branch['landmark'] += "".join(re.findall(reLmark, branch['sublocality']))
		branch['sublocality'] = re.sub(reLmark, "", branch['sublocality'])
	except IndexError:
		branch['sublocality'] = ""

	branchdump.append(branch)

with open('../addresses/icici-branch_addr.json', 'w') as f:
	dump(branchdump, f, indent=1)

print "Branches done!"