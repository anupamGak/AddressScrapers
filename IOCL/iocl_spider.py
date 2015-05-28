from lxml import html
from urllib2 import urlopen
from iocl_item import Address
import json

states = []
districts = []
pumpdump = []

jsonfile = open("address2.json", 'w')

opener = urlopen("https://www.iocl.com/Retails.aspx")
mainpage = html.parse(opener).getroot()

states = mainpage.xpath("//select[@id='cmbState']/option/@value")
states.pop(0)

for state in states:
	mainpage.forms[0].fields['cmbState'] = state
	distpage = html.parse(html.submit_form(mainpage.forms[0])).getroot()
	print "Processing state: " + state

	districts = distpage.xpath("//select[@id='cmbDistrict']/option/@value")
	districts.pop(0)

	for district in districts:
		distpage.forms[0].fields['cmbDistrict'] = district
		try:
			resultpage = html.parse(html.submit_form(distpage.forms[0])).getroot()
		except UnicodeEncodeError:
			print "!!!!!ERROR!!!!!" + state + district
			break;

		for row in range(1,50):
			pump = Address()
			try:
				pump.name = resultpage.xpath("//table[@id='grdRetail2']/tr[%d]/td[1]/text()" % row)[0]
				pump.owner = resultpage.xpath("//table[@id='grdRetail2']/tr[%d]/td[2]/text()" % row)[0]
				pump.address = resultpage.xpath("//table[@id='grdRetail2']/tr[%d]/td[3]/text()" % row)[0]
				pump.town = resultpage.xpath("//table[@id='grdRetail2']/tr[%d]/td[4]/text()" % row)[0]
				pump.district = resultpage.xpath("//table[@id='grdRetail2']/tr[%d]/td[5]/text()" % row)[0]
				pump.pin = resultpage.xpath("//table[@id='grdRetail2']/tr[%d]/td[6]/text()" % row)[0]
				pump.state = resultpage.xpath("//table[@id='grdRetail2']/tr[%d]/td[7]/text()" % row)[0]
				pump.phone = resultpage.xpath("//table[@id='grdRetail2']/tr[%d]/td[8]/text()" % row)[0]
				pumpdump.append(pump.__dict__)
			except IndexError:
				break;

json.dump(pumpdump, jsonfile, indent=1)