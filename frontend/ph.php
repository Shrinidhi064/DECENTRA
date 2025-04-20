<?php
// Database connection
$servername = "localhost";
$db_username = "root";
$db_password = ""; // Default password for XAMPP
$dbname = "login_system";

$conn = new mysqli($servername, $db_username, $db_password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Handle POST request
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['username'];
    $password = $_POST['password'];

    // Check if username exists
    $stmt = $conn->prepare("SELECT password FROM users WHERE username = ?");
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $stmt->store_result();

    if ($stmt->num_rows > 0) {
        $stmt->bind_result($stored_password);
        $stmt->fetch();

        // Validate password
        if ($password === $stored_password) {
            echo "success";
        } else {
            echo "Invalid Password.";
        }
    } else {
        echo "Invalid Username.";
    }

    $stmt->close();
} else {
    echo "Invalid Request.";
}

$conn->close();
?>
