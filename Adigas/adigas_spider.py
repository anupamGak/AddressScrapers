from lxml import html
import requests
from json import dump

data = { "locid" : "1"}

shopdump = []
for i in range(1,35):
	data['locid'] = i
	resp = requests.post("http://adigas.in/wp-content/themes/twentyeleven/process.php", data=data)
	shop = resp.json()['address_arr']
	print "*************************************"
	print i
	if shop:
		if shop['type'] == None or "urant" in shop['type']:
			shop.pop("id")
			shop.pop("phone")
			shop.pop("delivery")
			shop.pop("type")
			shop.pop("mapurl")
			shopdump.append(shop)
		else:
			print "Not a Restaurant"
		print shop['location']
	else:
		print "Invalid ShopID"

with open('adigas_addr.json', 'w') as f:
	dump(shopdump, f, indent=1)