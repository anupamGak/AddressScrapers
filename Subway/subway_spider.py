from lxml import html
import re
from json import dump

reLmark = re.compile("(?:next to|near|beside| opp).+?(?=,|$)", re.IGNORECASE)

page = html.parse("http://www.subway.co.in/page_restaurant_locator.aspx").getroot()
form = page.forms[0]

#form.fields['ctl00$ContentPlaceHolder1$txtState'] = ""

page = html.parse(html.submit_form(form)).getroot()
datas = page.xpath("//td[@class='df']")

shopdump = []
state = "Andhra Pradesh"
print "Processing State : " + state
for data in datas:
	shop = {}
	shop['address'] = data.xpath("span/text()")[0]
	line2 = data.xpath("text()")[1]
	line2 = re.sub(" {2,}", "", line2)
	line2 = line2.split("\r\n")
	shop['city'] = line2[-3]
	shop['state'] = line2[-2]
	shop['pincode'] = line2[-1]

	shop['landmark'] = ",".join(re.findall(reLmark, shop['address']))
	addr = re.sub(reLmark, "", shop['address'])
	addr  = addr.split(",")
	address = [x for x in addr if re.search("\w", x)]
	shop['locality'] = address[-1]
	try:
		shop['sublocality'] = address[-2]
	except IndexError:
		shop['sublocality'] = ""

	if not state == shop['state']:
		state = shop['state']
		print "Processing State : " + state

	shopdump.append(shop)

with open('subway_addr.json', 'w') as f:
	dump(shopdump, f, indent=1)

print "Done!"