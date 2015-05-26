from lxml import html
import requests
from item import address
from time import sleep
import json

states = []
cities = []
neighbours = []

dumpfile = open('scraped.json', 'w')

main_page = requests.get("http://www.medplusindia.com/locations.jsp")
tree = html.fromstring(main_page.text)

states = tree.forms[0].inputs['displaystate'].value_options
states.pop(0)

for state in states:
	page = requests.get("http://www.medplusindia.com/locationSearch.jsp?state=%s" % state)
	tree = html.fromstring(page.text)
	print "Processing state: " + state

	cities = tree.xpath("//option/@value")
	cities.pop(0)
	cities.pop(-1)

	for city in cities:
		page = requests.get("http://www.medplusindia.com/locationSearch.jsp?city=%s" % city)
		tree = html.fromstring(page.text)

		neighbours = tree.xpath("//option/@value")
		neighbours.pop(0)

		for neighbour in neighbours:
			shop = address()
			neighbour.replace(" ", "+")
			try:
				page = requests.get("http://www.medplusindia.com/searchList.jsp?neighbour=%s" % neighbour)
			except requests.exceptions.ConnectionError:
				sleep(1)
				page = requests.get("http://www.medplusindia.com/searchList.jsp?neighbour=%s" % neighbour)

			tree = html.fromstring(page.text)

			try:
				shop.location = tree.xpath("//td[1]/text()")[0]
			except IndexError:
				shop.location = ""

			try:
				shop.complete = tree.xpath("//td[2]/text()")[0]
			except IndexError:
				shop.complete = ""
			
			try:
				shop.phone = tree.xpath("//td[3]/text()")[0]
			except IndexError:
				shop.phone = ""

			try:
				shop.locality = tree.xpath("//td[4]/text()")[0]
			except IndexError:
				shop.locality = ""

			try:
				shop.landmark = tree.xpath("//td[5]/text()")[0]
			except IndexError:
				shop.landmark = ""

			shop.city = city
			shop.state = state

			json.dump(shop.__dict__, dumpfile)