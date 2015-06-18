import requests
from lxml import html
import re

reStateid = re.compile(r'StatePKID="(\d+)"')
reCityid = re.compile(r'CityPKID="(\d+)"')

dataURL = "http://www.syndicatebank.in/webservices/Services.asmx"
data = """<soap:Envelope xmlns:xsi='http://wwww.w3.org/XMLSchema-instance' xmlns:xsd='http://www.w3.org/XMLSchema' xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'><soap:Body><s:Execute xmlns:s='http://tempuri.org/'><s:xml>&lt;Root&gt;&lt;SP&gt;&lt;EncryptedChiper type='attribute' name='name'&gt;&lt;ChiperText&gt;&lt;ChiperValue&gt;Z2ZTbn9qf1h/bkx8MTE=&lt;/ChiperValue&gt;&lt;/ChiperText&gt;&lt;/EncryptedChiper&gt;&lt;/SP&gt;&lt;/Root&gt;</s:xml></s:Execute></soap:Body></soap:Envelope>"""

headers = {
	"Content-Type" : "text/xml",
	"SOAPAction" : "http://tempuri.org/Execute"
}

data = """<soap:Envelope xmlns:xsi='http://wwww.w3.org/XMLSchema-instance' xmlns:xsd='http://www.w3.org/XMLSchema' xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'><soap:Body><s:Execute xmlns:s='http://tempuri.org/'><s:xml>&lt;Root&gt;&lt;SP&gt;&lt;EncryptedChiper type='attribute' name='name'&gt;&lt;ChiperText&gt;&lt;ChiperValue&gt;fXxJdGVwZUJoU2hleFJldFZ8NzE=&lt;/ChiperValue&gt;&lt;/ChiperText&gt;&lt;/EncryptedChiper&gt;&lt;Param value='%s' &gt;&lt;EncryptedChiper type='attribute' name='name'&gt;&lt;ChiperText&gt;&lt;ChiperValue&gt;TUBCWWx9aH1afDk=&lt;/ChiperValue&gt;&lt;/ChiperText&gt;&lt;/EncryptedChiper&gt;&lt;/Param&gt;&lt;/SP&gt;&lt;/Root&gt;</s:xml></s:Execute></soap:Body></soap:Envelope>"""

locatorURL = "http://www.syndicatebank.in/scripts/BranchLocatorUser.aspx?StateId=%s&CityName=%s"

page = html.parse(locatorURL % (8, 295)).getroot()
form = page.forms[0]
form.fields['__EVENTTARGET'] = "dgbranchlocator:_ctl27:Title"

page = html.parse(html.submit_form(form)).getroot()
print page.xpath("//span[@id='txtBranchName']/text()	")