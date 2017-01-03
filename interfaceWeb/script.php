<?php
if(isset($_POST['manageValue']) && !empty($_POST['manageValue'])) {
    $ValForm = $_POST['manageValue'];

    $arguments = explode(";", $ValForm);

    $servername = "127.0.0.1";
    $username = "root";
    $password = "azerty";
    $dbname = "Scanner";

    $conn = new mysqli($servername, $username, $password, $dbname);
    if ($conn->connect_error) {
      die("Connection failed: " . $conn->connect_error);
    }

    echo $ValForm . "\n";

    echo "Manage= " . $arguments[0];
    echo "SID= " . $arguments[1];



    $sql = "UPDATE services SET manage= $arguments[0] WHERE sid = $arguments[1]";
    $result = $conn->query($sql);

    $conn->close();

    header('Location: toute_la_bdd.php');
}
?>
