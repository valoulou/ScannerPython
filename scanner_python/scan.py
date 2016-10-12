##########################
#                        #
# Scanner python NMAP    #
#                        #
##########################

from termcolor import colored
from datetime import datetime
import sys
import nmap
import sqlite3

############################################
#                                          #
# Classe Host definissant                  #
# une machine (ip, port, service, date)    #
#                                          #
############################################

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

################################################
#                                              #
# Fonction inserport                           #
# Insert les ports et les services dans la BDD #
# S'ils ne sont pas connus                     #
#                                              #
################################################

def insertport(listport, cursor):
    cursor.execute("""SELECT port FROM services""")
    rows = cursor.fetchall()
    for actuport in listport:
        if (actuport,) not in rows:
            try:
                print colored('\tInsertion du port %s...' % actuport, 'blue')
                cursor.execute("""
                INSERT INTO services(port, proto, banner, version, last_view) VALUES(?, ?, ?, ?, ?)""", (actuport, "proto", "banner", "2", "12:12:12 12/12/12"))
            except sqlite3.Error, e:
                print colored('Error INSERT PORT %s:' % e.args[0], 'red')
                sys.exit(2)

############################################
#                                          #
# Fonction insermachine                    #
# Insert les machines dans la BDD          #
# Si la machine est déjà présente, on met  #
# à jour l'heure                           #
#                                          #
############################################

def insertmachine(machine, cursor):
    cursor.execute("""SELECT ip FROM machines""")
    rows = cursor.fetchall()
    if (machine.ip,) not in rows:
        try:
            print colored('\tInsertion de la machine %s...' % machine.ip, 'blue')
            cursor.execute("""
            INSERT INTO machines(fqdn, ip, last_view) VALUES(?, ?, ?)""", ("labellemachine.a2s", machine.ip, machine.date))
        except sqlite3.Error, e:
            print colored('Error INSERT MACHINE %s:' % e.args[0], 'red')
            sys.exit(2)
    else:
        try:
            print colored('\tUpdate date de la machine %s...' % machine.ip, 'blue')
            cursor.execute("""
            UPDATE machines SET last_view = ? WHERE ip = ?""", (machine.date, machine.ip))
        except sqlite3.Error, e:
            print colored('Error UPDATE MACHINE %s:' % e.args[0], 'red')
            sys.exit(2)

print colored('Connexion a la BDD...', 'yellow')

try:
    bdd=sqlite3.connect('scanner.db')
    cursor = bdd.cursor()
except sqlite3.Error, e:
    print colored('Error %s:' % e.args[0], 'red')
    sys.exit(1)

print colored('Connexion reussi!\n', 'green')

print colored('Scan en cours...', 'yellow')

listhost=[]
nm = nmap.PortScanner()
nm.scan('192.168.20.0/24', '22-443')

print colored('Scan termine!\n', 'green')

print colored('Analyse des machines...', 'yellow')

for host in nm.all_hosts():
    for proto in nm[host].all_protocols():
        lport = nm[host][proto].keys()
        lport.sort()
        mon_host = Host()
        mon_host.ip=host
        for port in lport:
            mon_host.appendport(port)
            mon_host.appendservice(nm[host][proto][port]['name'])
            #print('port : %s\tstate : %s\tname : %s' % (port, nm[host][proto][port]['state'], nm[host][proto][port]['name']))
        listhost.append(mon_host)

print colored('Analyse terminee!\n', 'green')

print colored('Insertion dans la BDD...\n', 'yellow')

for currenthost in listhost:
    insertmachine(currenthost, cursor)
    insertport(currenthost.port, cursor)

try:
	bdd.commit()
except sqlite3.Error, e:
    print colored('Error COMMIT %s:' % e.args[0], 'red')
    sys.exit(2)

print colored('\nInsertion terminee!', 'green')
bdd.close()