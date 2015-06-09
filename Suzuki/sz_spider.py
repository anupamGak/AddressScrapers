from lxml import html

page = html.parse("http://www.suzukimotorcycle.co.in/tab1.aspx").getroot()
targ = page.xpath("//input/@id")
print targ
form = page.forms[0]

zones = page.xpath("//select[@id='ddlZone']/option/@value")
zones.pop(0)

for zone in zones:
	form.fields['ddlZone'] = zone
	page = html.parse(html.submit_form(form)).getroot()
	states = {
		"val" : page.xpath("//select[@id='ddlstate']/option/@value"),
		"name" : page.xpath("//select[@id='ddlstate']/option/text()")
	}
	states['val'].pop(0)
	states['name'].pop(0)
	form = page.forms[0]

	for i in range(len(states['val'])):
		form.fields['ddlstate'] = states['val'][i]
		page = html.parse(html.submit_form(form)).getroot()

		cities = {
			"val" : page.xpath("//select[@id='ddlcity']/option/@value"),
			"name" : page.xpath("//select[@id='ddlcity']/option/text()")
		}
		cities['val'].pop(0)
		cities['name'].pop(0)
		form = page.forms[0]

		for j in range(len(cities['val'])):
			print states['name'][i] + cities['name'][j]
			targ = page.xpath("//input")
			print targ
			