##########################
#                        #
# Scanner python NMAP    #
#                        #
##########################

from termcolor import colored
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
# un service (port, nom du service, state) #
#                                          #
############################################

class Service:
    def __init__(self):
        self._port=0
        self._nomservice=''
        self._state=''
    @property
    def port(self):
        return self._port
    @property
    def nomservice(self):
        return self._nomservice
    @property
    def state(self):
        return self._state
    @port.setter
    def port(self, p):
        self._port = port
    @nomservice.setter
    def nomservice(self, n):
        self._nomservice = n
    @state.setter
    def state(self, s):
        self._state = s

################################################
#                                              #
# Fonction inserport                           #
# Insert les ports et les services dans la BDD #
# S'ils ne sont pas connus                     #
#                                              #
################################################

def insertport(mid, listport, date, cursor):
    #cursor.execute("""SELECT port FROM services""")
    #rows = cursor.fetchall()
    rows = returnportmid(mid, cursor)
    print rows
    for actuport in listport:
        if (actuport.port,) not in rows:
            try:
                print colored('\tInsertion du port %s...' % actuport.port, 'blue')
                cursor.execute("""
                INSERT INTO services (port, proto, state, banner, version, last_view) VALUES(%s, %s, %s, %s, %s, %s)""", (actuport.port, actuport.nomservice, actuport.state, "banner", "2", date))
            except mysql.connector.Error, e:
                print colored('Error INSERT PORT %s:' % e.args[0], 'red')
                sys.exit(4)
            association(mid, returnsid(actuport.port, cursor))
        else:
            try:
                print colored('\tUpdate du port %s...' % actuport.port, 'blue')
                cursor.execute("""
                UPDATE services SET last_view = %s WHERE port = %s""", (date, actuport.port))
            except mysql.connector.Error, e:
                print colored('Error INSERT PORT %s:' % e.args[0], 'red')
                sys.exit(4)

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

############################################
#                                          #
# Fonction asociation                      #
# Defini l association entre une           #
# machine et un port dans la table         #
# association                              #
#                                          #
############################################

def association(Pmid, Psid):
    print('MID -> %s' % Pmid)
    print('SID -> %s' % Psid)
    try:
        cursor.execute("""
        INSERT INTO association(mid, sid) VALUES(%d, %d)""", (Pmid[0], Psid[0]))
    except mysql.connector.Error, e:
        print colored('Error INSERT ASSOCIATION %s:' % e.args[0], 'red')

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
        return cursor.fetchone()
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
        SELECT sid
        FROM association
        WHERE mid = '%s'""" % mid)
        listsid = [item[0] for item in cursor.fetchall()]
        format_strings = ','.join(['%s'] * len(listsid))
        if cursor.rowcount == 0:
            return []
        #return truc
    except mysql.connector.Error, e:
        print colored('Error SELECT ALL SID %s:' % e.args[0], 'red')
        sys.exit(8)
    try:
        placeholders= ', '.join([('%s')]*len(listsid))
        query = 'SELECT port FROM services WHERE sid IN ({})'.format(placeholders)
        cursor.execute(query, tuple(listsid))
        listport = [item[0] for item in cursor.fetchall()]
        print listport
        return listport
    except mysql.connector.Error, e:
        print colored('Error SELECT ALL PORT %s:' % e.args[0], 'red')
        sys.exit(8)

if(len(sys.argv)<3):
	print colored('Usage : scan.py @IP portdeb-portfin', 'red')
	sys.exit(0)

print colored('Connexion a la BDD...', 'yellow')

try:
    #bdd=sqlite3.connect('scanner.db')
    bdd = mysql.connector.connect(host="127.0.0.1",user="scanner_user",password="user@pass", database="Scanner")
    cursor = bdd.cursor()
except mysql.connector.Error, e:
    print colored('Error %s:' % e.args[0], 'red')
    sys.exit(1)

print colored('Connexion reussi!\n', 'green')

print colored('Scan en cours...', 'yellow')

listhost=[]
nm = nmap.PortScanner()
nm.scan(sys.argv[1], sys.argv[2])

print colored('Scan termine!\n', 'green')

print colored('Analyse des machines...', 'yellow')

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
            servi.port=port
            servi.state=nm[host][proto][port]['state']
            mon_host.appendserv(servi)
        listhost.append(mon_host)

print colored('Analyse terminee!\n', 'green')

print colored('Insertion dans la BDD...\n', 'yellow')

for currenthost in listhost:
    insertmachine(currenthost, cursor)
    insertport(returnmid(currenthost.ip, cursor), currenthost.serv, currenthost.date, cursor)

try:
	bdd.commit()
except mysql.connector.Error, e:
    print colored('Error COMMIT %s:' % e.args[0], 'red')
    sys.exit(5)

print colored('\nInsertion terminee!', 'green')
bdd.close()
