from scapy.all import *
from netaddr import IPAddress,IPNetwork


subnet="172.20.10.0/28"
pre_ip="172.20.10."
for ip in IPNetwork(subnet):
    # ip=pre_ip+str(i)
    ip=str(ip)
    pkt=Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip)
    recv=srp1(pkt,timeout=2,verbose=0)
    if recv:
        print "[+]",recv.psrc

print 'end'