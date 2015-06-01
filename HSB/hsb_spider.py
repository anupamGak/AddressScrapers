from lxml import html
from json import dump
import re
from hsb_items import Address

cnURL = "http://www.saravanabhavan.com/restaurants.php?cn=India"
baseURL = "http://www.saravanabhavan.com/"

rePIN = re.compile("(?<=\D)\d{3}\s?\d{3}(?=\D)")

shopdump = []

main_page = html.parse(cnURL).getroot()

cityDivs = main_page.xpath("//div[@id='cityDiv']")
cities = cityDivs[1].xpath("//a/@id")

for city in cities:
	area_page = html.parse(cnURL + "&cy=%s" % city).getroot()
	areaclks = area_page.xpath("//div[@id='branchDiv']//span/@onclick")
	areanames = area_page.xpath("//div[@id='branchDiv']//span/text()")
	print "Processing city : " + city

	for i in range(len(areanames)):
		arealink = re.findall("(?<=').+(?=')", areaclks[i])[0]
		addr_page = html.parse(baseURL + arealink).getroot()
		shop = Address()

		table = addr_page.xpath("//table[@width='355']")[1]
		addr = table.xpath("tr[1]/td/text()")
		addr.pop(-1)

		try:
			if re.search(rePIN, addr[0]):
				shop.pin = re.search(rePIN, addr[0]).group()
			else:
				shop.pin = re.search(rePIN, addr[-1]).group()
		except AttributeError:
			print "PIN N/A : " + areanames[i]

		shop.city = city
		shop.area = areanames[i]
		shop.fulladd = addr[0]

		shopdump.append(shop.__dict__)

f = open('hsb_addr.json', 'w')
dump(shopdump, f, indent=1)