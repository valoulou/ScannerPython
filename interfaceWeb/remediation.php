<?php

include_once 'includes/credentials.php';

  $rulesFile = fopen("rules_anchor.txt", "w+");

  $bdd = new PDO('mysql:host='.HOST.';dbname='.DBNAME, USER, PWD);
  if (!$bdd) {
      die('Connexion impossible : ' . mysql_error());
  }

  $result = $bdd->query ("SELECT machines.mid, services.mid, services.proto, services.port, services.manage, machines.ip FROM services, machines WHERE (machines.mid = services.mid) AND manage=2");
  $result->setFetchMode(PDO::FETCH_ASSOC);

  while ($row = $result->fetch()) {
      $ip = $row["ip"];
      $port = $row["port"];
      $proto = $row["proto"];

      fputs($rulesFile, "block quick proto " . $proto . " from any to " . $ip . " port " . $port . "\n");

  }

  fclose($rulesFile);

 header('Location: service_managed.php');

  mysql_close($bdd);


 ?>
