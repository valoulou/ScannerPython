<?php

  $rulesFile = fopen('rules_anchor.txt', 'a+');

  $bdd = new PDO('mysql:host=192.168.10.33;dbname=Scanner', 'scanner_web', 'web@pass');
  if (!$bdd) {
      die('Connexion impossible : ' . mysql_error());
  }
  echo "Connecte correctement <br>";

  $result = $bdd->query ("SELECT machines.mid, services.mid, services.proto, services.manage, machines.ip, services.port FROM services, machines WHERE (machines.mid = services.mid) AND manage=2");
  $result->setFetchMode(PDO::FETCH_ASSOC);

  while ($row = $result->fetch()) {
      $ip = $row["ip"];
      $port = $row["port"];
      $proto = $row["proto"];

      fputs($rulesFile, 'block quick proto ' . $proto . ' from any to ' . $ip . ' port ' . $port . "\n");

  }

  fclose($rulesFile);

  $conn->close();

 ?>
