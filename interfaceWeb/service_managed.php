<html>

  <head>
      <meta charset="utf-8" />
      <link rel="stylesheet" href="style.css" />
      <title>La belle page d'accueil</title>
  </head>

  <body>
    <h1>Service managed</h1>

    <p>1: Port laissé ouvert</p>
    <p>2: Port à fermer</p>

    <?php

    $bdd = new PDO('mysql:host=192.168.10.33;dbname=Scanner', 'scanner_web', 'web@pass');
    if (!$bdd) {
        die('Connexion impossible : ' . mysql_error());
    }
    echo "Connecte correctement <br>";

    $result = $bdd->query ("SELECT machines.ip, services.mid, services.sid, services.port, services.nom_service, services.state, services.version, servives.banner, services.last_view, services.manage  FROM services, machines WHERE (machines.mid = services.mid) AND state = 'open' AND (manage=1 OR manage=2)");
    $result->setFetchMode(PDO::FETCH_ASSOC);

    if (!$result) {
        $message  = 'Requête invalide : ' . mysql_error() . "\n";
        die($message);
    }
    ?>

    <table>
        <thead>
          <tr>
            <th>mid</th>
            <th>ip</th>
            <th>sid</th>
            <th>port</th>
            <th>nom_service</th>
            <th>state</th>
            <th>version</th>
            <th>banner</th>
            <th>last_view</th>
            <th>manage</th>
          </tr>
        </thead>

      <?php while ($row = $result->fetch()) { ?>
        <tr>
          <td><?php echo htmlentities($row["mid"], ENT_QUOTES, "utf-8");?></td>
          <td><?php echo htmlentities($row["ip"], ENT_QUOTES, "utf-8");?></td>
          <td><?php echo htmlentities($row["sid"], ENT_QUOTES, "utf-8");?></td>
          <td><?php echo htmlentities($row["port"], ENT_QUOTES, "utf-8");?></td>
          <td><?php echo htmlentities($row["nom_service"], ENT_QUOTES, "utf-8");?></td>
          <td><?php echo htmlentities($row["state"], ENT_QUOTES, "utf-8");?></td>
          <td><?php echo htmlentities($row["version"], ENT_QUOTES, "utf-8");?></td>
          <td><?php echo htmlentities($row["banner"], ENT_QUOTES, "utf-8");?></td>
          <td><?php echo htmlentities($row["last_view"], ENT_QUOTES, "utf-8");?></td>
          <td><?php echo htmlentities($row["manage"], ENT_QUOTES, "utf-8");?></td>
        </tr>
      <?php } ?>

    </table>

    <?php
      mysql_close($bdd);
    ?>

    <form action="remediation.php" method="post">
    <input type="submit" value="Generer les règles" />
    </form>
  </body>

</html>
