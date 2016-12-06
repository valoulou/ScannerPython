<?php
if(isset($_POST['manageValue']) && !empty($_POST['manageValue'])) {
    $ValForm = $_POST['manageValue'];

    $arguments = explode(";", $ValForm);

    $servername = "192.168.10.33";
    $username = "scanner_web";
    $password = "web@pass";
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
