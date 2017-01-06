#!/bin/bash

unistall() {
    rm pythonnmap.conf
    rm -r /var/log/pythonnmap/
    rm /etc/init.d/pythonnmap
}

currentfolder=$(pwd)

if [ "$(id -u)" != "0" ]; then
   echo "Ce script doit etre execute en root" 1>&2
   exit 1
fi

if [ "$1" != "install" ] && [ "$1" != "unistall" ] && [ "$1" != "reinstall" ]; then
    echo "Usage : sh install_scanner.sh [install/unistall/reinstall]"
    exit 1
fi

if [ "$1" = "unistall" ];then
    echo "Desinstallation..."
    unistall
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

echo '    start-stop-daemon --start --background --pidfile $PIDFILE --make-pidfile --user $DAEMON_USER --chuid $DAEMON_USER --exec /usr/bin/python '$currentfolder'/jajscan.py' >> /etc/init.d/pythonnmap

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