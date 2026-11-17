<?php
session_start();
include 'conexion.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $correo = $_POST['usuario'];
    $password = $_POST['contraseña'];

    $sql = "SELECT id, correo, password FROM usuarios WHERE correo = ?";
    $stmt = $conexion->prepare($sql);
    $stmt->bind_param("s", $correo);
    $stmt->execute();
    $resultado = $stmt->get_result();

    if ($row = $resultado->fetch_assoc()) {
        if (password_verify($password, $row['password'])) {
            $_SESSION['usuario'] = $row['correo'];
            header("Location: ../Index.html");
            exit();
        } else {
            echo "Contraseña incorrecta.";
        }
    } else {
        echo "El usuario no existe.";
    }
}