from lxml import html
import requests
from json import dump

data = { "locid" : "27"}
resp = requests.post("http://adigas.in/wp-content/themes/twentyeleven/process.php", data=data)
print resp.json()