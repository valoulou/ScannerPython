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

      $bdd = new PDO('mysql:host=127.0.0.1;dbname=Scanner', 'scanner_web', 'web@pass');
      if (!$bdd) {
          die('Connexion impossible : ' . mysql_error());
      }
      echo "Connecte correctement <br>";

      $result = $bdd->query ("SELECT mid, sid, port, state, version, last_view  FROM services WHERE state = 'open'");
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
              <th>sid</th>
              <th>port</th>
              <th>state</th>
              <th>version</th>
              <th>last_view</th>
            </tr>
          </thead>

        <?php while ($row = $result->fetch()) { ?>
          <tr>
            <td id="mid" onclick="addRowHandlers(this)";><?php echo htmlentities($row["mid"], ENT_QUOTES, "utf-8");?></td>
            <td><?php echo htmlentities($row["sid"], ENT_QUOTES, "utf-8");?></td>
            <td><?php echo htmlentities($row["port"], ENT_QUOTES, "utf-8");?></td>
            <td><?php echo htmlentities($row["state"], ENT_QUOTES, "utf-8");?></td>
            <td><?php echo htmlentities($row["version"], ENT_QUOTES, "utf-8");?></td>
            <td><?php echo htmlentities($row["last_view"], ENT_QUOTES, "utf-8");?></td>
          </tr>
        <?php } ?>

      </table>

      <?php
        mysql_close($bdd);
      ?>
  </body>
</html>
