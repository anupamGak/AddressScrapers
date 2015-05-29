from lxml import html
import requests

page = requests.get("http://www.cafecoffeeday.com/ajax/getstoreslist.php")
tree = html.fromstring(page.text)

print page.text