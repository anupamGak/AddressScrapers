import requests

data = {
	"city" : "Chennai"
}

resp = requests.post("http://www.vespa.in/our-store/ourstore.aspx/Getdealers", data=data)
print resp.text