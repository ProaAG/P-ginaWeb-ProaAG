<?php
$servername = "localhost";
$username = "username"; //cambiar por usuario de la base de datos
$password = "password"; //cambiar por contraseña de la base de datos
$dbname = "mydb"; //cambiar por nombre de la base de datos

$conexion = new mysqli($servername, $username, $password, $dbname);

if ($conexion->connect_error) {
  die("Conexion fallida: " . $conexion->connect_error);
}