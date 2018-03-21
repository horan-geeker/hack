import json
import requests

urls = []

with open('struts2.json','r') as file:
    urls = file.read()

urls = json.loads(urls)

for url in urls:
    url = url+'/integration/editGangster.action'
    response = requests.get(url, timeout=10)
    print(url, response.status_code)