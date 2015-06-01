from lxml import html
import re
from json import dump
from aab_items import *

main_page = html.parse("http://www.aabsweets.in/store.php").getroot()

shopdump = []

city = City()

for x in range(13):
	city.code = main_page.xpath("//select[@name='cat']/option[%s]/@value" % str(x+2))[0]
	city.name = main_page.xpath("//select[@name='cat']/option[%s]/text()" % str(x+2))[0]
	print "Processing city:" + city.name

	area_page = html.parse("http://www.aabsweets.in/dd.php?code=%s&sid=1" % city.code).getroot()
	areacodes = re.findall('(?<=")\d{1,2}', html.tostring(area_page))

	for areacode in areacodes:
		addr_page = html.parse("http://www.aabsweets.in/getuser.php?q=%s" % areacode).getroot()
		shop = Address()

		

		shop.city = city.name

		arealine = addr_page.xpath("//tr[1]/td/span/text()")[0]
		shop.area = arealine.replace(" SHOP", "")

		shop.loc = addr_page.xpath("//tr[2]/td[2]/text()")[0]

		try:
			pinline = addr_page.xpath("//tr[3]/td[2]/text()")[0]
			shop.pin = "".join(re.findall("\d+", pinline))
		except IndexError:
			shop.pin = ""
			print "PIN N/A : " + areacode

		shopdump.append(shop.__dict__)

f = open('aab_addr.json', 'w')
dump(shopdump, f, indent=1)