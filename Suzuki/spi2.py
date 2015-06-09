import requests
from lxml import html

page = html.parse("http://www.suzukimotorcycle.co.in/tab1.aspx").getroot()
form = page.forms[0]

form.fields = {
	"ddlZone" : "3",
	"ddlstate" : "2",
	"ddlcity" : "408",
	"Submit" : "Go"
}

page2 = html.parse(html.submit_form(form)).getroot()
print html.tostring(page2)