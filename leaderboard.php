<?php
include 'db_connect.php';

function get_leaderboard($link) {
    $sql = "SELECT * FROM leader ORDER BY place";
    $result = mysqli_query($link, $sql);

    if (!$result) {
        die("Query failed: " . mysqli_error($link));
    }

    $leaderboard = [];
    while ($row = mysqli_fetch_assoc($result)) {
        $leaderboard[] = $row;
    }

    return $leaderboard;
}

header('Content-Type: application/json');
echo json_encode(get_leaderboard($link));
?>
