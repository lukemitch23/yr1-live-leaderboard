<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Airport Departures Board</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Pixeltype&display=swap" rel="stylesheet">
</head>
<body>
    <header class="departures-banner">
        <div class="header-content">
            <img src="side_plane.png" alt="Header Image" class="header-image">
            <h1 class="header-title">LEADERBOARD</h1>
            <div id="clock" class="header-clock">
                <span id="hour1" class="clock-box"></span>
                <span id="hour2" class="clock-box"></span>
                <span class="clock-separator">:</span>
                <span id="minute1" class="clock-box"></span>
                <span id="minute2" class="clock-box"></span>
            </div>
        </div>
    </header>
    <div class="departures-board">
        <table>
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Username</th>
                    <th>Code</th>
                    <th>Score</th>
                </tr>
            </thead>
            <tbody>
                <tr id="row1"><td>1</td><td>Energetic Eagle27</td><td>ee27</td><td>123</td></tr>
                <tr id="row2"><td>2</td><td>Bored Fly53</td><td>bf53</td><td>234</td></tr>
                <tr id="row3"><td>3</td><td>Noisy Cheetah26</td><td>nc26</td><td>145</td></tr>
                <tr id="row4"><td>4</td><td>Purple Alligator62</td><td>pa62</td><td>198</td></tr>
                <tr id="row5"><td>5</td><td>Cool Finch60</td><td>cf60</td><td>276</td></tr>
                <tr id="row6"><td>6</td><td>Disloyal Goat15</td><td>dg15</td><td>87</td></tr>
                <tr id="row7"><td>7</td><td>Vibrant Aardvark46</td><td>va46</td><td>210</td></tr>
                <tr id="row8"><td>8</td><td>Grey Cormorant35</td><td>gc35</td><td>156</td></tr>
                <tr id="row9"><td>9</td><td>Dry Goldfinch54</td><td>dg54</td><td>189</td></tr>
                <tr id="row10"><td>10</td><td>Quiet Antelope6</td><td>qa6</td><td>78</td></tr>

            </tbody>
        </table>
    </div>
    <script>
        function updateClock() {
            const now = new Date();
            const hours = now.getHours().toString().padStart(2, '0');
            const minutes = now.getMinutes().toString().padStart(2, '0');
            document.getElementById('hour1').textContent = hours[0];
            document.getElementById('hour2').textContent = hours[1];
            document.getElementById('minute1').textContent = minutes[0];
            document.getElementById('minute2').textContent = minutes[1];
        }

        setInterval(updateClock, 1000);
        updateClock(); // Initial call to display the clock immediately
    </script>
</body>
</html>

<?php
include 'db_connect.php';

// Get the total count of rows in the 'leader' table
$sql = "SELECT COUNT(id) AS total_count FROM leader";
$result = mysqli_query($link, $sql);

if (!$result) {
    die("Query failed: " . mysqli_error($link));
}

$row = mysqli_fetch_assoc($result);
$data_amount = (int)$row['total_count'];
$whole_iterations = floor($data_amount / 10);
$partial_iterations = $data_amount % 10;

$ten_block = 0;

function get_update($ten_block, $link) {
    $row_id = 1;
    $start_id = ($ten_block * 10) + 1;
    $end_id = ($ten_block * 10) + 10;
    $sql = "SELECT * FROM leader WHERE id BETWEEN $start_id AND $end_id ORDER BY place";
    $ranks = mysqli_query($link, $sql);

    if (!$ranks) {
        die("Query failed: " . mysqli_error($link));
    }

    while ($row = mysqli_fetch_assoc($ranks)) {
        echo '<script type="text/javascript">
        updateRow(' . $row_id . ', "' . $row['place'] . '", "' . $row['name'] . '", "' . $row['code'] . '", "' . $row['score'] . '");
        </script>';
        $row_id++;
    }
}

while (true) {
    get_update($ten_block, $link);
    sleep(45);
    $ten_block++;
    if ($ten_block > $whole_iterations) {
        $ten_block = 0;
    }
}
?>


