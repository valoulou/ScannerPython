#!/bin/bash

unistall() {
    rm pythonnmap.conf
    rm -r gestion_bdd
    rm -r /var/log/pythonnmap/
    rm /etc/init.d/pythonnmap
}

clear_bdd() {
    read -p "Nom BDD : " nom_bdd
    read -p "IP BDD : " ip_bdd
    echo "Renseignez un utilisateur disposant des droits TRUNCATE/DELETE/ALTER sur la table "$nom_bdd
    read -p "Nom utilisateur : " bdd_user
    read -p "Mot de passe : " -s bdd_pass
    mysql -h $ip_bdd -u $bdd_user "-p"$bdd_pass $nom_bdd < "./gestion_bdd/clear_bdd.sql"
}

drop_bdd() {
    read -p "Nom BDD : " nom_bdd
    read -p "IP BDD : " ip_bdd
    echo "Renseignez un utilisateur disposant des droits DROP sur la table "$nom_bdd
    read -p "Nom utilisateur : " bdd_user
    read -p "Mot de passe : " -s bdd_pass
    mysql -h $ip_bdd -u $bdd_user "-p"$bdd_pass $nom_bdd < "./gestion_bdd/drop_bdd.sql"
}

create_bdd() {
    echo "Renseignez un utilisateur disposant des droits CREATE/ALTER sur la table " $1
    read -p "Nom utilisateur : " bdd_user
    read -p "Mot de passe : " -s bdd_pass   
    mysql -h $2 -u $bdd_user "-p"$bdd_pass $1 < "./gestion_bdd/create_bdd.sql" 
}

create_script_bdd() {
    mkdir "gestion_bdd"

    cat <<'WRITE_SCRIPT' > ./gestion_bdd/create_bdd.sql
CREATE TABLE `machines` (
  `mid` int(11) NOT NULL,
  `fqdn` text CHARACTER SET utf8 NOT NULL,
  `ip` text CHARACTER SET utf8 NOT NULL,
  `last_view` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `services` (
  `sid` int(11) NOT NULL,
  `mid` int(11) NOT NULL,
  `proto` text NOT NULL,
  `port` int(11) NOT NULL,
  `nom_service` text NOT NULL,
  `state` text NOT NULL,
  `banner` text NOT NULL,
  `version` text NOT NULL,
  `last_view` datetime NOT NULL,
  `manage` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

ALTER TABLE `machines`
  ADD PRIMARY KEY (`mid`),
  ADD KEY `mid` (`mid`) USING BTREE,
  ADD KEY `last_view` (`last_view`) USING BTREE;
ALTER TABLE `services`
  ADD PRIMARY KEY (`sid`),
  ADD KEY `mid` (`mid`) USING BTREE,
  ADD KEY `sid` (`sid`) USING BTREE,
  ADD KEY `last_view` (`last_view`) USING BTREE,
  ADD KEY `port` (`port`) USING BTREE;

ALTER TABLE `machines`
  MODIFY `mid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

ALTER TABLE `services`
  MODIFY `sid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

ALTER TABLE `services`
  ADD CONSTRAINT `fk_mid` FOREIGN KEY (`mid`) REFERENCES `machines` (`mid`);
WRITE_SCRIPT

    create_bdd $1 $2

    cat <<'WRITE_SCRIPT' > ./gestion_bdd/clear_bdd.sql
TRUNCATE TABLE services;
DELETE FROM `machines`;
ALTER TABLE `machines` AUTO_INCREMENT = 1;
WRITE_SCRIPT

    cat <<'WRITE_SCRIPT' > ./gestion_bdd/drop_bdd.sql
DROP TABLE `services`;
DROP TABLE `machines`;
WRITE_SCRIPT
}

currentfolder=$(pwd)

if [ "$(id -u)" != "0" ]; then
   echo "Ce script doit etre execute en root" 1>&2
   exit 1
fi

if [ "$1" != "install" ] && [ "$1" != "unistall" ] && [ "$1" != "reinstall" ] && [ "$1" != "clearbdd" ]; then
    echo "Usage : sh install_scanner.sh [install/unistall/reinstall/clearbdd]"
    exit 1
fi

if [ "$1" = "clearbdd" ];then
    clear_bdd
    exit 1
fi

if [ "$1" = "unistall" ];then
    echo "Desinstallation..."
    drop_bdd
    unistall
    echo "Daemon supprime..."
    echo "BDD videe..."
    echo "Supprimez la DataBase pour completer la desinstallation..."
    exit 1
fi

if [ "$1" = "reinstall" ];then
    echo "Reinstallation"
    unistall
fi

echo "Creation du dossier de log : /var/log/pythonnmap/"

mkdir /var/log/pythonnmap/

echo "Creation du service..."

cat <<'WRITE_SCRIPT' >> /etc/init.d/pythonnmap
#!/bin/sh
# kFreeBSD do not accept scripts as interpreters, using #!/bin/sh and sourcing.
if [ true != "$INIT_D_SCRIPT_SOURCED" ] ; then
    set "$0" "$@"; INIT_D_SCRIPT_SOURCED=true . /lib/init/init-d-script
fi
### BEGIN INIT INFO
# Provides:          skeleton
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Example initscript
# Description:       This file should be used to construct scripts to be
#                    placed in /etc/init.d.  This example start a
#                    single forking daemon capable of writing a pid
#                    file.  To get other behavoirs, implemend
#                    do_start(), do_stop() or other functions to
#                    override the defaults in /lib/init/init-d-script.
### END INIT INFO
# Author: Valentin Chaigneau <valentin.chaigneau@insa-cvl.fr>

DESC="Analyse reseau en python avec nmap"
DAEMON=/usr/sbin/pythonnmap
DAEMON_NAME=pythonnmap
WRITE_SCRIPT

read -p "Adresse de la BDD : " addr_bdd

read -p "Nom de la base : " bdd_name

read -p "Nom utilisateur BDD : " bdd_user

read -p "Mot de passe BDD : " -s password

echo ""

read -p "Reseau a analyser [0.0.0.0/24] : " addr_reseau

read -p "Port a analyser [Port_debut-Port_fin / all] : " port_analyze

echo "NOTE : En vitesse fast l analyse est moins precise !"

read -p "Vitesse d analyse [fast/slow] : " speed

cat <<'WRITE_SCRIPT' >> /etc/init.d/pythonnmap

DAEMON_USER=root

PIDFILE=/var/run/$DAEMON_NAME.pid

do_start () {
    log_daemon_msg "Starting service scanner $DAEMON_NAME"

WRITE_SCRIPT

echo '    start-stop-daemon --start --background --pidfile $PIDFILE --make-pidfile --user $DAEMON_USER --chuid $DAEMON_USER --exec /usr/bin/python '$currentfolder'/jajscan.py '$currentfolder/pythonnmap.conf >> /etc/init.d/pythonnmap

cat <<'WRITE_SCRIPT' >> /etc/init.d/pythonnmap
    log_end_msg $?
}
do_stop () {
    log_daemon_msg "Stopping service scanner $DAEMON_NAME"
    #start-stop-daemon --stop --signal INT --pidfile $PIDFILE --retry 10
    kill -2 `cat $PIDFILE`
    killall -9 nmap
    log_end_msg $?
}

case "$1" in

    start|stop)
        do_${1}
        ;;

    restart|reload|force-reload)
        do_stop
        do_start
        ;;

    status)
        status_of_proc "$DAEMON_NAME" "$DAEMON" && exit 0 || exit $?
        ;;

    *)
        echo "Usage: /etc/init.d/$DAEMON_NAME {start|stop|restart|status}"
        exit 1
        ;;

esac
exit 0

WRITE_SCRIPT

chmod +x /etc/init.d/pythonnmap

read -p "Voulez-vous recevoir les resultats du scan par mail (SMTP uniquement)? [y/n]" reponse

if [ $reponse == "y" ];then
    read -p "Adresse d envoie : " addr_send
    read -p "Mot de passe adresse d envoie : " passmail
    read -p "Adresse destination (mail1, mail2, mail3...) : " addr_dest
    read -p "Adresse SMTP (gmail:smtp.gmail.com) : " addr_smtp
    read -p "Port SMTP (gmail:587) : " port_smtp
fi

echo "Creation du fichier de configuration..."

echo "################ CONFIGURATION SCANNER PYTHON NMAP ################" >> pythonnmap.conf
echo 'BDDAddr = '$addr_bdd >> pythonnmap.conf
echo 'BDDName = '$bdd_name >> pythonnmap.conf
echo 'BDDUser = '$bdd_user >> pythonnmap.conf
echo 'BDDPass = '$password >> pythonnmap.conf
echo 'Reseau = '$addr_reseau >> pythonnmap.conf
echo "## Format : PortDebut-PortFin ou mettre all pour scanner tout les ports" >> pythonnmap.conf
echo 'Port = '$port_analyze >> pythonnmap.conf
echo "## Format : slow ou fast (le mode fast est moins precis)" >> pythonnmap.conf
echo 'Speed = '$speed >> pythonnmap.conf
echo "################ CONFIGURATION MAIL SCANNER PYTHON NMAP ################" >> pythonnmap.conf
echo "## Mettre y pour activer l envoie de mail" >> pythonnmap.conf
echo 'Envoimail = '$reponse >> pythonnmap.conf
echo 'AddrSend = '$addr_send >> pythonnmap.conf
echo 'Passmail = '$passmail >> pythonnmap.conf
echo "##Adresse destination format : mail1, mail2, mail3..." >> pythonnmap.conf
echo 'AddrDest = '$addr_dest >> pythonnmap.conf
echo 'AddrSMTP = '$addr_smtp >> pythonnmap.conf
echo 'PortSMTP = '$port_smtp >> pythonnmap.conf

if [ "$1" = "install" ];then
    echo "Creation des script SQL..."
    create_script_bdd $bdd_name $addr_bdd
fi