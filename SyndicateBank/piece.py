for i in range(31):
	j = i + 1
	datapage = requests.post(dataURL, data=data % j, headers=headers)
	xmldata = datapage.text

	cities = re.findall(reCityid, xmldata)

	for city in cities:
		page = html.parse(locatorURL % (i+1, city)).getroot()
		form = page.forms[0]
		form.fields['__EVENTTARGET'] = "dgbranchlocator:_ctl3:Title"

		page = html.parse(html.submit_form(form)).getroot()
		