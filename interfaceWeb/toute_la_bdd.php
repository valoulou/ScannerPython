<html>

    <head>
        <meta charset="utf-8" />
        <link rel="stylesheet" href="style.css" />
        <script src="event.js" type="text/javascript"></script>
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
        <title>Projet Scanner</title>
    </head>

    <body>

      <h1> Projet Scanner </h1>

      <?php

      $bdd = new PDO('mysql:host=192.168.10.33;dbname=Scanner', 'scanner_web', 'web@pass');
      if (!$bdd) {
          die('Connexion impossible : ' . mysql_error());
      }
      echo "Connecte correctement <br>";

      $result = $bdd->query ("SELECT machines.ip, services.mid, services.sid, services.port, services.proto, services.nom_service, services.state, services.version, servives.banner, services.last_view, services.manage  FROM services, machines WHERE (machines.mid = services.mid) AND state = 'open'");
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
              <th>proto</th>
              <th>nom_service</th>
              <th>state</th>
              <th>version</th>
              <th>banner</th>
              <th>last_view</th>
              <th>manage</th>
              <th>Change manage</th>
            </tr>
          </thead>

        <?php while ($row = $result->fetch()) { ?>
          <tr>
            <td><?php echo htmlentities($row["mid"], ENT_QUOTES, "utf-8");?></td>
            <td><?php echo htmlentities($row["ip"], ENT_QUOTES, "utf-8");?></td>
            <td><?php echo htmlentities($row["sid"], ENT_QUOTES, "utf-8");?></td>
            <td><?php echo htmlentities($row["port"], ENT_QUOTES, "utf-8");?></td>
            <td><?php echo htmlentities($row["proto"], ENT_QUOTES, "utf-8");?></td>
            <td><?php echo htmlentities($row["nom_service"], ENT_QUOTES, "utf-8");?></td>
            <td><?php echo htmlentities($row["state"], ENT_QUOTES, "utf-8");?></td>
            <td><?php echo htmlentities($row["version"], ENT_QUOTES, "utf-8");?></td>
            <td><?php echo htmlentities($row["banner"], ENT_QUOTES, "utf-8");?></td>
            <td><?php echo htmlentities($row["last_view"], ENT_QUOTES, "utf-8");?></td>
            <td><?php echo htmlentities($row["manage"], ENT_QUOTES, "utf-8");?></td>
            <td>
              <form action="script.php" method="post">
                <select type="text" name="manageValue" size="1" />
                  <option></option>
                  <option value=<?php echo htmlentities("1;" . $row["sid"] , ENT_QUOTES, "utf-8");?>>Laisser Ouvert</option>
                  <option value=<?php echo htmlentities("2;" . $row["sid"] , ENT_QUOTES, "utf-8");?>>Le Fermer</option>
                </select>
                <input type="submit" value="Valider">
              </form>
            </td>
          </tr>
        <?php } ?>

      </table>

      <?php
        mysql_close($bdd);
      ?>
  </body>
</html>
