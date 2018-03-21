import requests

cookies = dict(__jsluid='8ff06ac0a9144d3f1c6f7b8a8cde6d9f', Hm_lvt_e58da53564b1ec3fb2539178e6db042e='1503766924,1504513500,1505383493', __jsl_clearance='1509287096.097|0|ANd5Pcqt6cA%2B0fCdTT3zBLIQNc0%3D', Hm_lvt_3c8266fabffc08ed4774a252adcb9263='1509286729,1509286800', Hm_lpvt_3c8266fabffc08ed4774a252adcb9263='1509287433')

headers = {'cube-authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Ik5vbmUiLCJ1dWlkIjoiZDIyOWU4MmNhZjgyN2JiNmY4MTdkMWFlNjdiNzlkN2QiLCJpYXQiOjE1MDkyODczMzYsImV4cCI6MTUwOTM3MzczNn0.P8Y10Ak7BsmjtMrSKtPuVh8dVdq_GeTOthkw2XCf9gA'}

print(cookies,headers)

response = requests.get('https://www.zoomeye.org/api/search?q=%20supervisor%20%2Bport%3A%229001%22&t=all&p=1', cookies=cookies, headers=headers)

print(response.text)