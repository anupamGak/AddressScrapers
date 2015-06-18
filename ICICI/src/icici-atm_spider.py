import requests
from json import dump

data = {
	"latLongString" : "21.1458004,79.08815460000005",
	"Radius" : "500.0",
	"BranchServices" : "",
	"ATMServices" : ""
}

atmdump = []
def spider():
	total = 0
	resp = requests.post("http://maps.icicibank.com/mobile/LEPTON/Handlers/SVCHandler.ashx?Task=GetATMData", data=data)
	page = resp.text.encode("ascii", 'ignore')
	page = page.replace("<br/>", "")
	page = page.replace("^^", "^")
	details = page.split("$")

	total += len(details)
	print total

	for detail in details:
		detail = detail.replace("ICICI Bank Ltd. - ", "")
		detail = detail.split("^")[:-2]

		atm = {}
		atm['pincode'] = detail.pop()
		atm['state'] = detail.pop()
		atm['city'] = detail.pop()
		atm['lat'] = detail.pop(0)
		atm['long'] = detail.pop(0)
		detail.pop(0)

		detail = detail[0].split(",")
		atm['locality'] = detail.pop()
		atm['sublocality'] = ",".join(detail)

		atmdump.append(atm)



spider()


data["latLongString"] = "12.9715987,77.59456269999998"
spider()



with open('../addresses/icici-atm_addr.json', 'w') as f:
	dump(atmdump, f, indent=1)