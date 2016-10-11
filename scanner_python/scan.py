import nmap
from datetime import datetime
import sqlite3

class Host:

    def __init__(self):
        self._ip=''
        self._port=[]
        self._nomservice=[]
        dateactu=datetime.now()
        self._date=str(dateactu.hour)+':'+str(dateactu.minute)+':'+str(dateactu.second)+' '+str(dateactu.day)+'/'+str(dateactu.month)+'/'+str(dateactu.year)

    @property
    def ip(self):
        return self._ip
    @property
    def port(self):
        return self._port
    @property
    def nomservice(self):
        return self._nomservice
    @property
    def date(self):
        return self._date
    @ip.setter
    def ip(self, i):
        self._ip = i

    @port.setter
    def port(self, p):
        self._port = p

    def appendport(self, p):
        self._port = self._port + [p]
        return self._port

    @nomservice.setter
    def nomservice(self, s):
        self._nomservice = s

    def appendservice(self, s):
        self._nomservice = self._nomservice + [s]
        return self._nomservice
    @date.setter
    def date(self, d):
        self._date = d

print('Scan en cours...')
listhost=[]
nm = nmap.PortScanner()
nm.scan('192.168.20.0/24', '22-443')
print('\nAnalyse des machines...')

for host in nm.all_hosts():

    #print('------------------------------------')
    #print('Host : %s' % host)
    #print('State : %s' % nm[host].state())
    for proto in nm[host].all_protocols():
        #print('Protocol : %s' % proto)
        lport = nm[host][proto].keys()
        lport.sort()
        mon_host = Host()
        mon_host.ip=host
        for port in lport:
            mon_host.appendport(port)
            mon_host.appendservice(nm[host][proto][port]['name'])
            #print('port : %s\tstate : %s\tname : %s' % (port, nm[host][proto][port]['state'], nm[host][proto][port]['name']))
        listhost.append(mon_host)

for currenthost in listhost:
    print('\n------------------------------------\n')
    print('IP : %s' % currenthost.ip)
    print('Port : %s' % currenthost.port)
    print('Service : %s' % currenthost.nomservice)
    print('Date : %s' % currenthost.date)