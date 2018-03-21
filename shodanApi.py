import shodan
from supervisor_poc import *

SHODAN_API_KEY = "HXJBiaL2JIx5uGsZAd3fS4kiRlfjQHwv"

query = 'wordpress'
api = shodan.Shodan(SHODAN_API_KEY)

results = api.search(query)
print(results)
shodan_res = []

for target in results['matches']:
    port = target['port']
    # if port == 9001:
    ip = target['ip_str']+':'+str(port)
    url = 'http://'+ip
    shodan_res.append(url)

file_content = json.dumps(shodan_res)
with open(query+'.json','w') as supervisor_file:
    supervisor_file.write(file_content)
with open(query+'-original.json','w') as supervisor_file:
    supervisor_file.write(file_content)

print(shodan_res)