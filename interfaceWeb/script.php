<?php
if(isset($_POST['manageValue']) && !empty($_POST['manageValue'])) {
    $ValForm = $_POST['manageValue'];

    $arguments = explode(";", $ValForm);

    $servername = "127.0.0.1";
    $username = "scanner_web";
    $password = "web@pass";
    $dbname = "Scanner";

    $conn = new mysqli($servername, $username, $password, $dbname);
    if ($conn->connect_error) {
      die("Connection failed: " . $conn->connect_error);
    }

    echo $ValForm . "\n";

    echo "Manage= " . $arguments[0];
    echo "MID= " . $arguments[1];
    echo "SID= " . $arguments[2];


    $sql = "UPDATE services SET manage= $arguments[0] WHERE (mid = $arguments[1]) AND (sid = $arguments[2]) ";
    $result = $conn->query($sql);

    /*if ($result->num_rows > 0) {

    while($row = $result->fetch_assoc()) {
        echo "ip: " . $row["ip"];
    }
    } else {
      echo "0 results";
    }*/
    $conn->close();
}
?>
