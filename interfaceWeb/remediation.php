<?php

  $rulesFile = fopen("rules_anchor.txt", "a");

  $bdd = new PDO('mysql:host=127.0.0.1;dbname=Scanner', 'root', 'azerty');
  if (!$bdd) {
      die('Connexion impossible : ' . mysql_error());
  }
  echo "Connecte correctement <br>";

  $result = $bdd->query ("SELECT machines.mid, services.mid, services.proto, services.port, services.manage, machines.ip FROM services, machines WHERE (machines.mid = services.mid) AND manage=2");
  $result->setFetchMode(PDO::FETCH_ASSOC);

  while ($row = $result->fetch()) {
      $ip = $row["ip"];
      $port = $row["port"];
      $proto = $row["proto"];

      fputs($rulesFile, "block quick proto " . $proto . " from any to " . $ip . " port " . $port . "\n");

  }

  fclose($rulesFile);

  mysql_close($bdd);

  header('Location: service_managed.php');
 ?>
