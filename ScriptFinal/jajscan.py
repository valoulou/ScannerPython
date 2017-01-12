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
import smtplib
import signal
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

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
        self._proto=''
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
    def nomservice(self):
        return self._proto
    @property
    def state(self):
        return self._state
    @property
    def banner(self):
        return self._banner
    @port.setter
    def port(self, p):
        self._port = p
    @port.setter
    def port(self, p):
        self._proto = p
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
                INSERT INTO services (mid, proto, port, nom_service, state, banner, version, last_view) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)""", (mid, actuport.proto, actuport.port, actuport.nomservice, actuport.state, actuport.banner, actuport.version, date))
            except mysql.connector.Error, e:
                print colored('Error INSERT PORT %s:' % e.args[0], 'red')
                sys.exit(4)
            bdd.commit()
        else:
            try:
                print colored('\t\tUpdate du port %s...' % actuport.port, 'blue')
                cursor.execute("""
                UPDATE services SET last_view = %s WHERE port = %s AND mid = %s""", (date, actuport.port, mid))
                bdd.commit()
            except mysql.connector.Error, e:
                print colored('Error UDPATE PORT %s:' % e.args[0], 'red')
                sys.exit(4)

            check_element_service("nom_service", actuport.nomservice, actuport.port, mid, cursor)
            check_element_service("state", actuport.state, actuport.port, mid, cursor)
            check_element_service("banner", actuport.banner, actuport.port, mid, cursor)
            check_element_service("version", actuport.version, actuport.port, mid, cursor)

    print('\n')

############################################
#                                          #
# Verifie si la version est differente     #
# avec la bdd                              #
#                                          #
############################################

def check_element_service(check, newval, port, mid, cursor):
    try:
        query = 'SELECT '+check+' FROM services WHERE mid = '+str(mid)+' AND port = '+str(port)
        cursor.execute(query)
        result = cursor.fetchone()    
        if result[0] == newval:
            return
        print colored('\t\t\tUpdate %s...' % check, 'blue')
        query = 'UPDATE services SET '+check+' = "'+newval+'" WHERE port = '+str(port)+' AND mid = '+str(mid)
        cursor.execute(query)
        bdd.commit()
    except mysql.connector.Error, e:
        print colored('Error UDPATE PORT CHECK VERSION %s:' % e.args[0], 'red')
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
# Retourne les port en fonction du mid     #
#                                          #
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
    tmp_time = str(tmp_time.day)+'/'+str(tmp_time.month)+'/'+str(tmp_time.year)+' '+str(tmp_time.hour)+':'+str(tmp_time.minute)+':'+str(tmp_time.second)
    return tmp_time

############################################
#                                          #
# Retourne une list d host configure       #
# d'un point de vu structure               #
#                                          #
############################################

def analyze(nm):
    proto_yes=['tcp', 'udp']
    print colored('Analyse des machines...(%s)' % datestr(datetime.now()), 'yellow')
    writelog("Analyse des machines")
    listhost=[]
    for host in nm.all_hosts():
        mon_host = Host()
        mon_host.ip=host
        mon_host.fqdn=nm[host].hostname()
        for proto in nm[host].all_protocols():
            if proto not in proto_yes:
                continue 
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
                servi.proto=proto
                servi.state=nm[host][proto][port]['state']
                mon_host.appendserv(servi)
        listhost.append(mon_host)
    print colored('Analyse terminee!(%s)\n' % datestr(datetime.now()), 'green')
    start_insert(listhost)

############################################
#                                          #
# Lance et retourne le resultat du scan    #
#                                          #
############################################

def start_scan(ip, port, mode):
    print colored('Scan en cours... (%s)' % datestr(datetime.now()), 'yellow')
    nm = nmap.PortScanner()

    if port == 'all':
        if mode == 'fast':
            nm.scan(ip, arguments='-p- --max-parallelism=100 -T5 --max-hostgroup=256 --script banner -sV')
        else:
            try:
                nm.scan(ip, arguments='-sV --script banner -p-')
            except KeyboardInterrupt:
                onfaitcabien()
    else:
        if mode == 'fast':
            nm.scan(ip, port, arguments='--max-parallelism=100 -T5 --max-hostgroup=256 --script banner -sV')
        else:
            nm.scan(ip, port, arguments='-sV --script banner')
    

    print colored('Scan termine!(%s)\n' % datestr(datetime.now()), 'green')
    writelog("Scan fini")
    return nm

############################################
#                                          #
# Lance l insertion dans la base de donnees#
#                                          #
############################################

def start_insert(listhost):
    print colored('Insertion dans la BDD...(%s)\n' % datestr(datetime.now()), 'yellow')
    writelog("Insertion en base de donnees")

    for currenthost in listhost:
        insertmachine(currenthost, cursor)
        insertport(returnmid(currenthost.ip, cursor), currenthost.serv, currenthost.date, cursor)
    print colored('\nInsertion terminee!(%s)' % datestr(datetime.now()), 'green')

############################################
#                                          #
# Enregistre les resultats de la BDD       #
# dans un fichier                          #
#                                          #
############################################

def result_to_text_file(temptotal, cursor):
    sqlmachine = """SELECT DISTINCT ip, fqdn FROM machines"""
    file = open("result.txt", "w")
    cursor.execute(sqlmachine)
    machine = cursor.fetchall()
    for rowmac in machine:
        file.write(rowmac[0]+' '+rowmac[1]+' : \n')
        mid = returnmid(rowmac[0], cursor)
        sqlservice = 'SELECT DISTINCT port, proto, banner, version FROM services WHERE mid = '+str(mid)
        cursor.execute(sqlservice)
        service = cursor.fetchall()
        for rowserv in service:
            file.write('\t\t'+str(rowserv[0])+'\t'+rowserv[1]+'\t'+rowserv[2]+'\t'+str(rowserv[3])+'\t'+'\n')

    file.write("\n\nTemps total de l'execution : "+str(temptotal))
    file.close()

############################################
#                                          #
# Envoi le contenu de la BDD par mail      #
#                                          #
############################################

def send_result_mail(reseau):
    fromaddr = "trashliam39@gmail.com"
    #toaddr = ['valentin.chaigneau@gmail.com', 'dupin.raphael@gmail.com', 'aurelien.bourillon@gmail.com']
    toaddr = ['valentin.chaigneau@gmail.com']
 
    msg = MIMEMultipart()
 
    msg['From'] = fromaddr
    msg['To'] = ", ".join(toaddr)
    msg['Subject'] = "Resultat script"
 
    body = "Yolo, je suis le script python et voici les resultats pour le reseau "+reseau
 
    msg.attach(MIMEText(body, 'plain'))
 
    filename = "result.txt"
    attachment = open("./result.txt", "rb")
 
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 
    msg.attach(part)
 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "J@j&Comp.")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

############################################
#                                          #
# Ecriture dans les log                    #
#                                          #
############################################

def writelog(chaine):
    fic = open("/var/log/pythonnmap/pythonnap.log", "a")
    fic.write(datestr(datetime.now())+" : "+chaine+"\n")
    fic.close()

############################################
#                                          #
# Interruption du programme                #
#                                          #
############################################

def onfaitcabien(*args):
    writelog("Interruption")
    try:
        bdd.close()
    except NameError:
        print "BDD non connectee"
    exit(0)

############################################
#                                          #
# Programme principal                      #
#                                          #
############################################

if(len(sys.argv)<4):
    writelog("Probleme nombre argument")
    print colored('Usage : scan.py @IP portdeb-portfin [mode] fast\slow', 'red')
    sys.exit(0)

startTime = datetime.now()

writelog("Service lance")

while True:

    try:
        writelog("Scan en cours pour le reseau "+sys.argv[1]+" pour les port "+sys.argv[2]+" en mode "+sys.argv[3])
        resultscan = start_scan(sys.argv[1], sys.argv[2], sys.argv[3])
        #if len(sys.argv) == 4:
        #    resultscan = start_scan(sys.argv[1], sys.argv[2], "fast")
        #else:
        #    resultscan = start_scan(sys.argv[1], sys.argv[2], "slow")
    except KeyboardInterrupt:
        onfaitcabien()

    print colored('Connexion a la BDD... (%s)' % datestr(datetime.now()), 'yellow')

    try:
        if len(sys.argv) == 8:
            bdd = mysql.connector.connect(host=sys.argv[4],user=sys.argv[5],password=sys.argv[6], database=sys.argv[7])
        else:
            bdd = mysql.connector.connect(host="127.0.0.1",user="scanner_user",password="user@pass", database="Scanner")
        cursor = bdd.cursor()
    except mysql.connector.Error, e:
        print colored('Error %s:' % e.args[0], 'red')
        writelog("Erreur connexion BDD")
        sys.exit(1)

    print colored('Connexion reussi! (%s)\n' % datestr(datetime.now()), 'green')

    analyze(resultscan)

    bdd.close()

    temp_exec = datetime.now() - startTime

    print ('Temps d execution total : %s' % temp_exec)

    #result_to_text_file(temp_exec, cursor)

    #send_result_mail(sys.argv[1])

    writelog("Scan termine. Temps total : "+str(temp_exec))