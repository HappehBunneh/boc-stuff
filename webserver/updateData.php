<?php
// This is the server-side script.

// Set the content type.
header('Content-Type: text/plain');

// Send the data back.
$servername = 'localhost';
$username = 'root';
$password = 'raspberry';
$dbname = 'data';
$array = array();
$sql = "SELECT * FROM data";
$conn = new mysqli($servername, $username, $password, $dbname);
$result = $conn->query($sql);
if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        array_push($array, [$row['current'], $row['voltage'], $row['temperature'], $row['power']]);
    }
}
mysqli_close($conn);
echo json_encode($array);
?>