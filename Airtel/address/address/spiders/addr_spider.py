import scrapy
import re
from address.items import AddressItem, AirtItem

rePin = re.compile('[0-9]{3}\s?[0-9]{3}')
reLmark = re.compile(r'(?:Opp|near|next to|beside|diagonal|lm\s?:?)[^0-9]+?(?=[,0-9])', re.IGNORECASE)
reCity = re.compile('[a-z]+(?=\s+[0-9]{3}\s?[0-9]{3})', re.IGNORECASE)

class AddrSpider(scrapy.Spider):
	name = 'addr'
	start_urls = ["http://www.airtel.in/personal/internet/4g/store-locator?&utm_source=airtel_4g_dr_google_search&utm_medium=cpc&utm_lp=4g_new_url&utm_content=selected_location_ad&utm_campaign=srch%20-%20dsa&cid=ps"]

	def parse(self, response):
	    for sel in response.xpath("//table[@class='table1 hidden']"):
		for x in sel.xpath("tr"):
			Item = AddressItem()

			#Shop name
			Item['title'] = x.xpath("td[1]/text()").extract()[0]

			saddr = x.xpath("td[2]/text()").extract()


			#Extract and remove landmark from saddr
			pureaddr = "GAK"
			if re.search(reLmark,saddr[0]):
				lmlist = re.findall(reLmark,saddr[0])
				Item['lmark'] = ",".join(lmlist)
				pureaddr = saddr[0].replace(lmlist[0], "")
				for l in lmlist[1:]:
					pureaddr = pureaddr.replace(l, "")
			else:
				pureaddr = saddr[0]

			Item['pureaddr'] = pureaddr

			#Extract pure address
			addr = pureaddr.split(",")
			addr = [x for x in addr if re.search(r'\S', x)]

			#pin
			Item['pin'] = re.search(rePin, addr[-1]).group()

			#city
			if re.search(reCity,addr[-1]):
				Item['city'] = re.search(reCity,addr[-1]).group()
			else:
				Item['city'] = sel.xpath("@id").extract()[0]

			addr.reverse()
			addr.append("")
			addr.append("")

			#Location
			Item['loc'] = addr[1]

			#Sublocation
			subloc = " "
			for i in addr[-1:1:-1]:
				subloc += i
			Item['subloc'] = subloc

			yield Item