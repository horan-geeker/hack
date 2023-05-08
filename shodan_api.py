import shodan
from supervisor_poc import *

SHODAN_API_KEY = ""

def SearchShodan(query):
    api = shodan.Shodan(SHODAN_API_KEY)
    results = api.search(query)
    return results

def ExportShodanResultToFile(results):
    urls = []
    for target in results['matches']:
        port = target['port']
        # if port == 9001:
        ip = target['ip_str'] + ':' + str(port)
        url = 'http://' + ip
        urls.append(url)

    file_content = json.dumps(urls)
    with open('shodan.json', 'w') as f:
        f.write(file_content)

if __name__ == '__main__':
    result = SearchShodan("redis")
    ExportShodanResultToFile(result)