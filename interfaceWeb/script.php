<?php

include_once 'includes/credentials.php';

if(isset($_POST['manageValue']) && !empty($_POST['manageValue'])) {
    $ValForm = $_POST['manageValue'];

    $arguments = explode(";", $ValForm);

    $conn = new mysqli(HOST, USER, PWD, DBNAME);
    if ($conn->connect_error) {
      die("Connection failed: " . $conn->connect_error);
    }

    $sql = "UPDATE services SET manage= $arguments[0] WHERE sid = $arguments[1]";
    $result = $conn->query($sql);

    if ($arguments[0] == 2){

    $rulesFile = fopen("rules_anchor.txt", "a+");

    fputs($rulesFile, "block quick proto " . $arguments[2] . " from any to " . $arguments[3] . " port " . $arguments[4] . "\n");

    fclose($rulesFile);

  }

    $conn->close();

    header('Location: toute_la_bdd.php');
}
?>
