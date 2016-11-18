<html>

    <head>
        <meta charset="utf-8" />
        <link rel="stylesheet" href="style.css" />
        <script src="event.js" type="text/javascript"></script>
        <title>Projet Scanner</title>
    </head>

    <body>

      <h1> Projet Scanner </h1>

      <?php

      $bdd = mysql_connect('192.168.10.33:3306', 'scanner_web', 'web@pass');
      if (!$bdd) {
          die('Connexion impossible : ' . mysql_error());
      }
      echo "Connecte correctement <br>";

      $db_selected = mysql_select_db('Scanner', $bdd);

      $result = mysql_query("SELECT mid, sid, port, state, version, last_view  FROM services WHERE state = 'open'");

      if (!$result) {
          $message  = 'Requête invalide : ' . mysql_error() . "\n";
          die($message);
      }
      ?>
      <div>
      <table id= "result" >
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

        <?php while ($row = mysql_fetch_assoc($result)) { ?>
          <tr>
            <td onclick="addRowHandlers(this)";><?php echo htmlentities($row["mid"], ENT_QUOTES, "utf-8");?></td>
            <td><?php echo htmlentities($row["sid"], ENT_QUOTES, "utf-8");?></td>
            <td><?php echo htmlentities($row["port"], ENT_QUOTES, "utf-8");?></td>
            <td><?php echo htmlentities($row["state"], ENT_QUOTES, "utf-8");?></td>
            <td><?php echo htmlentities($row["version"], ENT_QUOTES, "utf-8");?></td>
            <td><?php echo htmlentities($row["last_view"], ENT_QUOTES, "utf-8");?></td>
          </tr>
        <?php } ?>

      </table>
    </div>

      <?php
        mysql_close($bdd);
      ?>
  </body>
</html>
