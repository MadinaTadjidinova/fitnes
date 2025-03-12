<?php
// Database connection
$conn = new mysqli('localhost', 'root', '', 'fitnesspal');

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = $_POST['signup-name'];
    $email = $_POST['signup-email'];
    $password = password_hash($_POST['signup-password'], PASSWORD_BCRYPT);  // Hashing the password

    // SQL query to insert data into the users table
    $sql = "INSERT INTO users (name, email, password) VALUES (?, ?, ?)";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param('sss', $name, $email, $password);

    if ($stmt->execute()) {
        echo "Sign up successful!";
    } else {
        echo "Error: " . $conn->error;
    }

    $stmt->close();
    $conn->close();
}
?>
