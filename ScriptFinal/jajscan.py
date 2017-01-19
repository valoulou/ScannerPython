## @package scan_without_thread
#  Ce module permet de faire un scan reseau en python en ce basant sur l'API NMAP

from termcolor import colored
from datetime import datetime
import os, sys
import csv
import nmap
import time
import mysql.connector
import smtplib
import signal
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from netaddr import IPNetwork
import itertools

## Documentation de la class Host
#
#  Cette class defini une machine

class Host:

    ## Constructeur class Host
    def __init__(self):
        self._ip=''
        self._serv=[]
        self._fqdn=''    
        self._date=time.strftime('%Y-%m-%d %H:%M:%S')

    ## Definition de la propriete IP
    #  @param self Pointer sur IP.
    @property
    def ip(self):
        return self._ip

    ## Definition de la propriete des services
    #  @param self Pointer sur tableau des services.
    #  Cette propriete est defini par un tableau de services
    @property
    def serv(self):
        return self._serv   

    ## Definition de la propriete date
    #  @param self Pointer sur date.
    @property
    def date(self):
        return self._date

    ## Definition de la propriete FQDN
    #  @param self Pointer sur FQDN.
    @property
    def fqdn(self):
        return self._fqdn

    ## Setter IP
    #  @param self Pointer sur IP.
    #  @param i IP de la machine courante.
    @ip.setter
    def ip(self, i):
        self._ip = i

    ## Setter FQDN
    #  @param self Pointer sur FQDN.
    #  @param f FQDN de la machine courante.
    @fqdn.setter
    def fqdn(self, f):
        self._fqdn = f

    ## Setter Services
    #  @param self Pointer sur Service.
    #  @param s un des ports associe a la machine courante.
    @serv.setter
    def serv(self, s):
        self._serv = p

    ## Fonction d'ajout de services
    #  @param self Pointer sur Service.
    #  @param s service a ajouter a la machine courante.
    #  Cette fonction permet d'ajouter un service a la liste des services de la machine
    def appendserv(self, s):
        self._serv = self._serv + [s]
        return self._serv

    ## Setter Date
    #  @param self Pointer sur date.
    #  @param d date a laquelle le programme voit la machine.
    @date.setter
    def date(self, d):
        self._date = d

## Documentation de la class Service
#  Cette classe defini un service

class Service:

    ## Constructeur class Service
    def __init__(self):
        self._port=0
        self._version=''
        self._nomservice=''
        self._state=''
        self._banner=''
        self._proto=''

    ## Definition de la propriete port
    #  @param self port associe au service
    @property
    def port(self):
        return self._port

    ## Definition de la propriete version
    #  @param self version associe au service
    @property
    def version(self):
        return self._version

    ## Definition de la propriete nomservice
    #  @param self nom associe au service
    @property
    def nomservice(self):
        return self._nomservice

    ## Definition de la propriete port
    #  @param self protocol associe au service
    @property
    def proto(self):
        return self._proto

    ## Definition de la propriete state
    #  @param self etat associe au service
    @property
    def state(self):
        return self._state

    ## Definition de la propriete banner
    #  @param self banner associe au service
    @property
    def banner(self):
        return self._banner

    ## Setter Port
    #  @param self Pointer port
    #  @param p port du service
    @port.setter
    def port(self, p):
        self._port = p

    ## Setter Proto
    #  @param self Pointer proto
    #  @param p protocol du service
    @proto.setter
    def proto(self, p):
        self._proto = p

    ## Setter Version
    #  @param self Pointer version
    #  @param v version du service
    @version.setter
    def version(self, v):
        self._version = v

    ## Setter Nomservice
    #  @param self Pointer nomservice
    #  @param n nom du service
    @nomservice.setter
    def nomservice(self, n):
        self._nomservice = n

    ## Setter State
    #  @param self Pointer state
    #  @param s etat du service
    @state.setter
    def state(self, s):
        self._state = s

    ## Setter Banner
    #  @param self Pointer banner
    #  @param b banner du service
    @banner.setter
    def banner(self, b):
        self._banner = b

## Permet d'inserer les services associes a une machine dans la BDD
#  @param mid Identifiant de la machine en BDD
#  @param listport Liste des ports lies a la machine
#  @param date Date a laquelle la machine a ete vu
#  @param cursor Variable lie a l'ouverture de la bdd

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
                writelog("[!] Erreur insertion port")
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
                writelog("[!] Erreur update port")
                sys.exit(4)

            check_element_service("nom_service", actuport.nomservice, actuport.port, mid, cursor)
            check_element_service("state", actuport.state, actuport.port, mid, cursor)
            check_element_service("banner", actuport.banner, actuport.port, mid, cursor)
            check_element_service("version", actuport.version, actuport.port, mid, cursor)

    print('\n')

## Permet de verifier si les informations concernant le service sont connu. Si l information est erronee alors on la met a jour.
#  @param check Element que l on veut verifier (nom du service, etat, banner, version...)
#  @param newval Valeur que l on a detecte et que l on veut verifier
#  @param port Port associe au service
#  @param mid Identifiant de la machine en BDD
#  @param cursor Variable lie a l'ouverture de la bdd

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
        writelog("[!] Erreur update port check version")
        sys.exit(4)

## Permet d'inserer une machine dans la bdd en fonction d'un objet host
# @param machine Objet definissant la machine
# @param cursor Variable lie a l'ouverture de la bdd

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
            writelog("[!] Erreur insertion machine")
            sys.exit(2)
    else:
        try:
            print colored('\tUpdate date de la machine %s...' % machine.ip, 'blue')
            cursor.execute("""
            UPDATE machines SET last_view = %s WHERE ip = %s""", (machine.date, machine.ip))
        except mysql.connector.Error, e:
            print colored('Error UPDATE MACHINE %s:' % e.args[0], 'red')
            writelog("[!] Erreur update machine")
            sys.exit(3)
    bdd.commit()

## Permet de retourner le MID d'une machine en fonction de son IP
# @param ip IP de la machine que l'on recherche
# @param cursor Variable lie a l'ouverture de la bdd
# @return mid MID de la machine recherchee

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
        writelog("[!] Erreur select mid")
        sys.exit(7)

## Permet de retourner le SID d'un service en fonction de son port
# @param port Port du service recherche
# @param cursor Variable lie a l'ouverture de la bdd
# @return sid SID du service voulu

def returnsid(port, cursor):
    try:
        cursor.execute("""
        SELECT sid
        FROM services
        WHERE port = '%s'""" % port)
        return cursor.fetchone()
    except mysql.connector.Error, e:
        print colored('Error SELECT SID %s:' % e.args[0], 'red')
        writelog("[!] Erreur select sid")
        sys.exit(7)

## Permet de retourner les ports associe a une machine en fonction de son MID
# @param mid MID de la machine recherchee
# @param cursor Variable lie a l'ouverture de la bdd
# @return ports Ports associe au MID

def returnportmid(mid, cursor):
    try:
        cursor.execute("""
        SELECT port FROM services WHERE mid = '%s'""" % mid)
        return cursor.fetchall()
    except mysql.connector.Error, e:
        print colored('Error SELECT ALL SID %s:' % e.args[0], 'red')
        writelog("[!] Erreur select all sid")
        sys.exit(8)

## Permet de convertir un objet date en String au format HH:MM:SS
# @param tmp_time Date a convertir
# @return date Date converti

def datestr(tmp_time):
    tmp_time = str(tmp_time.day)+'/'+str(tmp_time.month)+'/'+str(tmp_time.year)+' '+str(tmp_time.hour)+':'+str(tmp_time.minute)+':'+str(tmp_time.second)
    return tmp_time

## Permet de remplir les structure Host et Service en fonction de l'analyse NMAP
# @param nm Objet de l'analyse NMAP

def analyze(nm):
    proto_yes=['tcp', 'udp']
    print colored('Analyse des machines...(%s)' % datestr(datetime.now()), 'yellow')
    writelog("[-] Analyse des machines")
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

## Permet de lancer le scan NMAP en prenant en compte les IPs et les ports voulus.
## La fonction prend en compte la vitesse voulu. En mode Slow NMAP sera execute normalement pour un scan complet.
## En mode Fast NMAP utilisera des threads. Le scan sera rapide mais peut-etre incomplet.
# @param ip Plage IP ou IP a scanner
# @param port Plage de port ou port a scanner
# @param mode Fast ou Slow pour un scan threade ou non
# @return nm Retourne le resultat du scan

def start_scan(ip, port, mode):
    print colored('Scan en cours... (%s)' % datestr(datetime.now()), 'yellow')
    nm = nmap.PortScanner()

    try:
        if port == 'all':
            if mode == 'fast':
                nm.scan(ip, arguments='-p- --max-parallelism=100 -T5 --max-hostgroup=256 --script banner -sV -f')
            else:
                nm.scan(ip, arguments='-sV --script banner -p- -f')

        else:
            if mode == 'fast':
                nm.scan(ip, port, arguments='--max-parallelism=100 -T5 --max-hostgroup=256 --script banner -sV -f')
            else:
                nm.scan(ip, port, arguments='-sV --script banner')
    except KeyboardInterrupt:
            interruptprogram()   

    print colored('Scan termine!(%s)\n' % datestr(datetime.now()), 'green')
    return nm

## Permet de lancer l'insertion des informations scannees en BDD
# @param listhost Liste des machines scannees sur le reseau

def start_insert(listhost):
    print colored('Insertion dans la BDD...(%s)\n' % datestr(datetime.now()), 'yellow')
    writelog("[-] Insertion en base de donnees")

    for currenthost in listhost:
        insertmachine(currenthost, cursor)
        insertport(returnmid(currenthost.ip, cursor), currenthost.serv, currenthost.date, cursor)
    print colored('\nInsertion terminee!(%s)' % datestr(datetime.now()), 'green')

## Permet d'enregistrer les informations de la BDD dans un fichier txt
# @param temptotal Temps total de l'analyse
# @param cursor Variable lie a l'ouverture de la bdd

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

## Permet d'enregistrer les informations de la BDD dans un fichier csv
# @param temptotal Temps total de l'analyse
# @param cursor Variable lie a l'ouverture de la bdd

def result_to_csv_file(temptotal, cursor):
    c = csv.writer(open("/tmp/result.csv", "wb"))
    c.writerow(["IP","FQDN","proto","port","nom service","Etat","banner","version"])
    sqlmachine = """SELECT DISTINCT ip, fqdn FROM machines"""
    cursor.execute(sqlmachine)
    machine = cursor.fetchall()

    for rowmac in machine:
        c.writerow([rowmac[0],rowmac[1],"","","","","",""])
        mid = returnmid(rowmac[0], cursor)
        sqlservice = 'SELECT DISTINCT proto, port, nom_service, state, banner, version FROM services WHERE mid = '+str(mid)
        cursor.execute(sqlservice)
        service = cursor.fetchall()
        for rowserv in service:
            c.writerow(["","",rowserv[0],str(rowserv[1]),rowserv[2],rowserv[3],rowserv[4],str(rowserv[5])])
    c.writerow([""])
    c.writerow(["Temp total du scan", temptotal])


## Permet d'envoyer les resultats du scan par mail
# @param reseau Reseau que le scan a analyse

def send_result_mail(reseau):

    writelog("[--] Envoi des resultats par mail")

    fromaddr = readconf("AddrSend")
    toaddrtmp = readconf("AddrDest")
    toaddrsplit = toaddrtmp.split(", ")
    toaddr = []
    for tmp in toaddrsplit:
        toaddr.append(tmp)

    result_to_csv_file(temp_exec, cursor)
 
    msg = MIMEMultipart()
 
    msg['From'] = fromaddr
    msg['To'] = ", ".join(toaddr)
    msg['Subject'] = "Resultat script"
 
    body = "Je suis le script python et voici les resultats pour le reseau "+reseau
 
    msg.attach(MIMEText(body, 'plain'))
 
    filename = "result.csv"

    try:
        attachment = open("/tmp/result.csv", "rb")
    except IOError:
        writelog("[!] Erreur lecture fichier result.csv. Envoi mail annule")
        return
 
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 
    msg.attach(part)

    server = smtplib.SMTP(readconf("AddrSMTP"), int(readconf("PortSMTP")))
    server.starttls()
    try:
        server.login(fromaddr, readconf("Passmail"))
    except SMTPAuthentificationError:
        writelog("[!] Erreur identifiant mail")
        return
    text = msg.as_string()
    try:
        server.sendmail(fromaddr, toaddr, text)
    except Exception:
        writelog("[!] Erreur envoi mail")
        return
    finally:
        server.quit()
    os.remove("/tmp/result.csv")
    writelog("[--] Mail envoye")
## Permet l'ecriture d'un log dans le fichier de log /var/log/pythonnmap/pythonnmap.log
# @param chaine Chaine de caractere a ecrire dans le fichier de log

def writelog(chaine):
    fic = open("/var/log/pythonnmap/pythonnmap.log", "a")
    fic.write(datestr(datetime.now())+" : "+chaine+"\n")
    fic.close()

## Permet la lecture du fichier de configuration
# @param param Nom du parametre que l'on recherche dans le fichier de configuration

def readconf(param):
    try:
        with open(path_conf) as fp:
            for line in fp:
                if line.split(" = ", 1)[0] == param:
                    return line.split(" = ", 1)[1].rstrip('\n')
        writelog("[!] Parametre "+param+" non specifie dans le fichier pythonnmap.conf")
        sys.exit(0)
    except IOError:
        writelog("[!] Erreur lecture fichier de configuration")
        sys.exit(0)

## Permet de gerer l'interruption du programme par interruption clavier.
## Ce signal est aussi utilise par le daemon.
# @param *args Arguments de l'interruption

def interruptprogram(*args):
    writelog("[!] Interruption")
    try:
        bdd.close()
    except NameError:
        print "BDD non connectee"
    exit(0)

## Permet de generer une liste d IP en fonction d une la plage IP
# @param rangeip Plage IP

def define_ip_addr(rangeip):
    ip_list = []
    if "/" in rangeip:
        ip_list = list(IPNetwork(rangeip))
        ip_list.pop(0)#on retire l'addresse de reseau
        return ip_list
    elif "-" in rangeip:
        numberip = rangeip.split('.')
        debip = [map(int, numberip.split('-')) for numberip in numberip]
        ranges = [range(c[0], c[1] + 1) if len(c) == 2 else c for c in debip]

        for address in itertools.product(*ranges):
            ip_list.append('.'.join(map(str, address)))
        return ip_list
    else:
        ip_list.append(rangeip)
        return ip_list

if len(sys.argv) == 2:
    path_conf=sys.argv[1]
else:
    path_conf="pythonnmap.conf"

while True:

    startTime = datetime.now()

    try:
        writelog("[*] Scan en cours pour le reseau "+readconf("Reseau")+" pour les port "+readconf("Port")+" en mode "+readconf("Speed"))

        for ipactu in define_ip_addr(readconf("Reseau")):

            writelog("[**] Scan machine "+str(ipactu)+" en cours")

            startTimeMachine = datetime.now()

            resultscan = start_scan(str(ipactu), readconf("Port"), readconf("Speed"))

            print colored('Connexion a la BDD... (%s)' % datestr(datetime.now()), 'yellow')

            try:
                ## @var bdd
                # Variable de connexion a la BDD
                bdd = mysql.connector.connect(host=readconf("BDDAddr"),user=readconf("BDDUser"),password=readconf("BDDPass"), database=readconf("BDDName"))
                cursor = bdd.cursor()
            except mysql.connector.Error, e:
                print colored('Error %s:' % e.args[0], 'red')
                writelog("[!] Erreur connexion BDD")
                sys.exit(1)

            print colored('Connexion reussi! (%s)\n' % datestr(datetime.now()), 'green')

            analyze(resultscan)

            temp_exec_machine = datetime.now() - startTimeMachine

            print colored('Temps d execution machine : %s' % temp_exec_machine, 'green')

            if readconf("Envoimail") == "y":
                send_result_mail(readconf("Reseau"))

            bdd.close()

            writelog("[**] Scan termine pour la machine "+str(ipactu)+" Temps total : "+str(temp_exec_machine))

        temp_exec = datetime.now() - startTime
        writelog("[*]Scan total termine. Temps total : "+str(temp_exec))
        print colored('Temps d execution total : %s' % temp_exec, 'green')

    except KeyboardInterrupt:
        interruptprogram()
