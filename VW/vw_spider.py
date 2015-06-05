from lxml import html
from json import dump
import re

dealerdump = []
reUnicode = re.compile("\\u\w+")
rePin = re.compile("\d{3} ?\d{3}")

main_page = html.parse("http://www.volkswagenlive.in/listdealers.aspx").getroot()

states = {
	"name" : main_page.xpath("//select[@id='ddlstates']/option/text()"),
	"value" : main_page.xpath("//select[@id='ddlstates']/option/@value")
}
states["name"].pop(0)
states["value"].pop(0)

form = main_page.forms[0]

for i in range(len(states["name"])):
	print "*************************************************"
	print "Processing state: " + states["name"][i]
	form.fields["ddlstates"] = states["value"][i]

	citypage = html.parse(html.submit_form(form)).getroot()
	cities = {
		"name" : citypage.xpath("//select[@id='ddlcities']/option/text()"),
		"value"	: citypage.xpath("//select[@id='ddlcities']/option/@value")
	}
	cities["name"].pop(0)
	cities["value"].pop(0)

	for j in range(len(cities["name"])):
		form = citypage.forms[0]
		form.fields["ddlcities"] = cities["value"][j]

		typepage = html.parse(html.submit_form(form)).getroot()
		types = {
			"name" : typepage.xpath("//select[@id='ddlnetwork']/option/text()"),
			"value" : typepage.xpath("//select[@id='ddlnetwork']/option/@value")
		}
		types["name"].pop(0)
		types["value"].pop(0)

		for k in range(len(types["name"])):
			form = typepage.forms[0]
			form.fields["ddlnetwork"] = types["value"][k]

			result = html.parse(html.submit_form(form)).getroot()
			details = result.xpath("//table[@id='dglist']/tr[@valign='top']/td[2]")
			for detail in details:
				dealer = {}
				rawdeal = detail.xpath("text()")
				rawdeal[0] = rawdeal[0].replace("\r\n                                                    ", "")
				rawdeal[-1] = rawdeal[-1].replace("\r\n                                                    ", "")

				if not re.search('\d', rawdeal[0]):
					dealer['name'] = rawdeal[0]
				else:
					dealer['name'] = ""

				dealer['locality'] = rawdeal[-3]
				dealer['address'] = "".join(rawdeal)
				dealer['city'] = cities["name"][j]
				dealer['state'] = states["name"][i]
				dealer['type'] = types["name"][k]
				dealer['pin'] = re.findall(rePin, dealer['address'])[0]

				dealerdump.append(dealer)

with open('vw_addr.json', 'w') as f:
	dump(dealerdump, f, indent=1)