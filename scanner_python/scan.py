##########################
#                        #
# Scanner python NMAP    #
#                        #
##########################

from termcolor import colored
from datetime import datetime
import sys
import nmap
import time
import mysql.connector

############################################
#                                          #
# Classe Host definissant                  #
# une machine (ip, service, fqdn, date)    #
#                                          #
############################################

class Host:

    def __init__(self):
        self._ip=''
        self._serv=[]
        self._fqdn=''    
        self._date=time.strftime('%Y-%m-%d %H:%M:%S')
       
    @property
    def ip(self):
        return self._ip
    @property
    def serv(self):
        return self._serv   
    @property
    def date(self):
        return self._date
    @property
    def fqdn(self):
        return self._fqdn
    @ip.setter
    def ip(self, i):
        self._ip = i
    @fqdn.setter
    def ip(self, f):
        self._fqdn = f
    @serv.setter
    def serv(self, s):
        self._serv = p

    def appendserv(self, s):
        self._serv = self._serv + [s]
        return self._serv
    @date.setter
    def date(self, d):
        self._date = d

############################################
#                                          #
# Classe Service definissant               #
# un service (port, nom du service, state, #
# banner)                                  #
#                                          #
############################################

class Service:
    def __init__(self):
        self._port=0
        self._version=''
        self._nomservice=''
        self._state=''
        self._banner=''
    @property
    def port(self):
        return self._port
    @property
    def version(self):
        return self._version
    @property
    def nomservice(self):
        return self._nomservice
    @property
    def state(self):
        return self._state
    @property
    def banner(self):
        return self._banner
    @port.setter
    def port(self, p):
        self._port = p
    @version.setter
    def version(self, v):
        self._version = v
    @nomservice.setter
    def nomservice(self, n):
        self._nomservice = n
    @state.setter
    def state(self, s):
        self._state = s
    @state.setter
    def state(self, b):
        self._banner = b

################################################
#                                              #
# Fonction inserport                           #
# Insert les ports et les services dans la BDD #
# S'ils ne sont pas connus                     #
#                                              #
################################################

def insertport(mid, listport, date, cursor):
    rows = returnportmid(mid, cursor)
    for actuport in listport:
        if (actuport.port,) not in rows:
            try:
                print colored('\t\tInsertion du port %s...' % actuport.port, 'blue')
                cursor.execute("""
                INSERT INTO services (mid, port, proto, state, banner, version, last_view) VALUES(%s, %s, %s, %s, %s, %s, %s)""", (mid, actuport.port, actuport.nomservice, actuport.state, actuport.banner, actuport.version, date))
            except mysql.connector.Error, e:
                print colored('Error INSERT PORT %s:' % e.args[0], 'red')
                sys.exit(4)
            bdd.commit()
        else:
            try:
                print colored('\t\tUpdate du port %s...' % actuport.port, 'blue')
                cursor.execute("""
                UPDATE services SET last_view = %s WHERE port = %s""", (date, actuport.port))
                bdd.commit()
            except mysql.connector.Error, e:
                print colored('Error UDPATE PORT %s:' % e.args[0], 'red')
                sys.exit(4)
    print('\n')

############################################
#                                          #
# Fonction insermachine                    #
# Insert les machines dans la BDD          #
# Si la machine est deja presente, on met  #
# a jour l heure                           #
#                                          #
############################################

def insertmachine(machine, cursor):
    cursor.execute("""SELECT ip FROM machines""")
    rows = cursor.fetchall()
    if (machine.ip,) not in rows:
        try:
            print colored('\tInsertion de la machine %s...' % machine.ip, 'blue')
            cursor.execute("""
            INSERT INTO machines(fqdn, ip, last_view) VALUES(%s, %s, %s)""", (machine.fqdn, machine.ip, machine.date))
        except mysql.connector.Error, e:
            print colored('Error INSERT MACHINE %s:' % e.args[0], 'red')
            sys.exit(2)
    else:
        try:
            print colored('\tUpdate date de la machine %s...' % machine.ip, 'blue')
            cursor.execute("""
            UPDATE machines SET last_view = %s WHERE ip = %s""", (machine.date, machine.ip))
        except mysql.connector.Error, e:
            print colored('Error UPDATE MACHINE %s:' % e.args[0], 'red')
            sys.exit(3)
    bdd.commit()

############################################
#                                          #
# Fonction returnmid                       #
# Retourne le mid en fonction d'une        #
# adresse ip                               #
#                                          #
############################################

def returnmid(ip, cursor):
    try:
        cursor.execute("""
        SELECT mid
        FROM machines
        WHERE ip = '%s'""" % ip)
        result = cursor.fetchone()
        return result[0]
    except mysql.connector.Error, e:
        print colored('Error SELECT MID %s:' % e.args[0], 'red')
        sys.exit(7)

############################################
#                                          #
# Fonction returnsid                       #
# Retourne le mid en fonction d'un port    #
#                                          #
############################################

def returnsid(port, cursor):
    try:
        cursor.execute("""
        SELECT sid
        FROM services
        WHERE port = '%s'""" % port)
        return cursor.fetchone()
    except mysql.connector.Error, e:
        print colored('Error SELECT SID %s:' % e.args[0], 'red')
        sys.exit(7)

############################################
#                                          #
# Fonction returnportmid                   #
# Retourne les port en fonction d'une      #
# adresse ip                               #
#                                          #
############################################

def returnportmid(mid, cursor):
    try:
        cursor.execute("""
        SELECT port FROM services WHERE mid = '%s'""" % mid)
        return cursor.fetchall()
    except mysql.connector.Error, e:
        print colored('Error SELECT ALL SID %s:' % e.args[0], 'red')
        sys.exit(8)

############################################
#                                          #
# Retourne date HH:MM:SS en String         #
#                                          #
############################################

def datestr(tmp_time):
    tmp_time = str(tmp_time.hour)+':'+str(tmp_time.minute)+':'+str(tmp_time.second)
    return tmp_time

############################################
#                                          #
# Programme principal                      #
#                                          #
############################################

if(len(sys.argv)<3):
	print colored('Usage : scan.py @IP portdeb-portfin', 'red')
	sys.exit(0)

startTime = datetime.now()

print colored('Connexion a la BDD... (%s)' % datestr(datetime.now()), 'yellow')

try:
    bdd = mysql.connector.connect(host="127.0.0.1",user="scanner_user",password="user@pass", database="Scanner")
    cursor = bdd.cursor()
except mysql.connector.Error, e:
    print colored('Error %s:' % e.args[0], 'red')
    sys.exit(1)

print colored('Connexion reussi! (%s)\n' % datestr(datetime.now()), 'green')

print colored('Scan en cours... (%s)' % datestr(datetime.now()), 'yellow')

listhost=[]
nm = nmap.PortScanner()
nm.scan(sys.argv[1], sys.argv[2], arguments='-sV --script banner')

print colored('Scan termine!(%s)\n' % datestr(datetime.now()), 'green')

print colored('Analyse des machines...(%s)' % datestr(datetime.now()), 'yellow')

for host in nm.all_hosts():
    mon_host = Host()
    mon_host.ip=host
    mon_host.fqdn=nm[host].hostname()
    for proto in nm[host].all_protocols():
        lport = nm[host][proto].keys()
        lport.sort()
        for port in lport:
            servi = Service()
            servi.nomservice=nm[host][proto][port]['name']
            if 'script' in nm[host][proto][port]:
                dic=nm[host][proto][port]['script']
                scriptvalue=dic.values()
                servi.banner=scriptvalue[0]
            if 'version' in nm[host][proto][port]:
                v = nm[host][proto][port]['version']
                servi.version = v
            servi.port=port
            servi.state=nm[host][proto][port]['state']
            mon_host.appendserv(servi)
        listhost.append(mon_host)

print colored('Analyse terminee!(%s)\n' % datestr(datetime.now()), 'green')

print colored('Insertion dans la BDD...(%s)\n' % datestr(datetime.now()), 'yellow')

for currenthost in listhost:
    insertmachine(currenthost, cursor)
    insertport(returnmid(currenthost.ip, cursor), currenthost.serv, currenthost.date, cursor)

try:
	bdd.commit()
except mysql.connector.Error, e:
    print colored('Error COMMIT %s:' % e.args[0], 'red')
    sys.exit(5)

print colored('\nInsertion terminee!(%s)' % datestr(datetime.now()), 'green')
bdd.close()

temp_exec = datetime.now() - startTime

print ('Temps d execution total : %s' % temp_exec)