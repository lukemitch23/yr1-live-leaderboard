<?php
define('DB_SERVER', 'localhost');
define('DB_USERNAME', 'pi_agent');
define('DB_PASSWORD', 'PowerUp');
define('DB_NAME', 'leaderboard');

$link = mysqli_connect(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME);
 
if($link === false){
    die("ERROR: Could not connect. " . mysqli_connect_error());
}
?>