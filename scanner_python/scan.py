import nmap

class Host:

    def __init__(self):
        self._ip=''
        self._port=[]

    @property
    def ip(self):
        return self._ip
    @property
    def port(self):
        return self._port

    @ip.setter
    def ip(self, i):
        self._ip = i

    @port.setter
    def port(self, p):
        self._port = p

    def append(self, p):
        self._port = self._port + [p]
        return self._port

mon_host = Host()

print('Scan en cours...')

nm = nmap.PortScanner()
nm.scan('192.168.20.0/24', '22-443')
print('\nAnalyse des machines...')

for host in nm.all_hosts():

    print('------------------------------------')
    print('Host : %s' % host)
    print('State : %s' % nm[host].state())
    for proto in nm[host].all_protocols():

        print('Protocol : %s' % proto)
        lport = nm[host][proto].keys()
        lport.sort()
        for port in lport:
            mon_host.ip=host
            mon_host.append(port)
            print('port : %s\tstate : %s' % (port, nm[host][proto][port]['state']))
