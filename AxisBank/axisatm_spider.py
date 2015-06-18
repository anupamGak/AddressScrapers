import requests
from lxml import html
import sys
from json import dump
import re

rePin = re.compile(r"[^0-9](\d{3}\s?\d{3})[^0-9]")

url = "http://m.axisbank.com/smartphone/WebForms/mATM-Locator.aspx"
sess = requests.Session()


resp = sess.get(url)
page = html.fromstring(resp.text)

viewstate = page.xpath("//input[@id='__VIEWSTATE']/@value")[0]
eventvalidation = page.xpath("//input[@id='__EVENTVALIDATION']/@value")[0]

states = {
	"id" : page.xpath("//select[@id='locate_office_ddlState']/option/@value"),
	"name" : page.xpath("//select[@id='locate_office_ddlState']/option/text()")
}

states['id'].pop(0)
states['name'].pop(0)

branchdump = []
for i in  range(len(states['id'])):
	data = {
		"__EVENTTARGET" : "locate_office$ddlState",
		"__EVENTARGUMENT" : "",
		"__LASTFOCUS" : "",
		"__VIEWSTATE" : viewstate,
		"locate_office$txtSearch" : "",
		"locate_office$ddlState" : states['id'][i],
		"locate_office$ddlCity" : "0",
		"locate_office$ddlBranch" : "0",
		"locate_office$hdOffType" : "atms",
		"locate_office$hdnLatitude" : "",
		"locate_office$hdnLongitude" : "",
		"hdnLatitude" : "",
		"hdnLongitude" : "",
		"__EVENTVALIDATION" : eventvalidation
	}

	print "Processing State : " + states['name'][i]
	
	resp = sess.post(url, data=data)
	page = html.fromstring(resp.text)
	viewstate = page.xpath("//input[@id='__VIEWSTATE']/@value")[0]
	eventvalidation = page.xpath("//input[@id='__EVENTVALIDATION']/@value")[0]

	cities = {
		"id" : page.xpath("//select[@id='locate_office_ddlCity']/option/@value"),
		"name" : page.xpath("//select[@id='locate_office_ddlCity']/option/text()")
	}

	cities['id'].pop(0)
	cities['name'].pop(0)
	for j in range(len(cities['id'])):
		data.update({
			"__EVENTTARGET" : "locate_office$ddlCity",
			"__VIEWSTATE" : viewstate,
			"locate_office$ddlState" : states['id'][i],
			"locate_office$ddlCity" : cities['id'][j],
			"locate_office$ddlBranch" : "0",
			"__EVENTVALIDATION" : eventvalidation
		})

		resp = sess.post(url, data=data)
		page = html.fromstring(resp.text)
		viewstate = page.xpath("//input[@id='__VIEWSTATE']/@value")[0]
		eventvalidation = page.xpath("//input[@id='__EVENTVALIDATION']/@value")[0]

		areas = {
			"id" : page.xpath("//select[@id='locate_office_ddlBranch']/option/@value"),
			"name" : page.xpath("//select[@id='locate_office_ddlBranch']/option/text()")
		}

		areas['id'].pop(0)
		areas['name'].pop(0)

		for k in range(len(areas['id'])):
			data.update({
				"__EVENTTARGET" : "locate_office$ddlBranch",
				"__VIEWSTATE" : viewstate,
				"locate_office$ddlState" : states['id'][i],
				"locate_office$ddlCity" : cities['id'][j],
				"locate_office$ddlBranch" : areas['id'][k],
				"locate_office$btnAddress" : "SUBMIT",
				"__EVENTVALIDATION" : eventvalidation
			})

			resp = sess.post(url, data=data)
			page = html.fromstring(resp.text)

			branch = {
				"state" : states['name'][i],
				"city" : cities['name'][j],
				"locality" : areas['name'][k]
			}
			addr = "".join(page.xpath("//table[@class='result']//tr[2]/td[2]/span[1]/text()"))
			branch['address'] = re.sub(r"\s{3,}", "", addr)
			try:
				branch['pincode'] = re.findall(rePin, addr)[0]
			except IndexError:
				branch['pincode'] = ""
			branch['sublocality'] = ",".join(addr.split(",")[:-3])
			branch['sublocality'] = re.sub(r"\s{3,}", "", branch['sublocality'])

			branchdump.append(branch)

with open('axisatm_addr.json', 'w') as f:
	dump(branchdump, f, indent=1)