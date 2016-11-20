<?php
if(isset($_POST['mid']) && !empty($_POST['mid'])) {
    $action = $_POST['mid'];

    $servername = "127.0.0.1";
    $username = "scanner_web";
    $password = "web@pass";
    $dbname = "Scanner";

    $conn = new mysqli($servername, $username, $password, $dbname);
    if ($conn->connect_error) {
      die("Connection failed: " . $conn->connect_error);
    }

    $sql = "SELECT ip FROM machines WHERE mid = '$action'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {

    while($row = $result->fetch_assoc()) {
        echo "ip: " . $row["ip"];
    }
    } else {
      echo "0 results";
    }
    $conn->close();
}
?>