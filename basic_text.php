<?php
include 'db_connect.php';

// Define the table name
$table_name = 'leader'; // Change this to your table name

// Query to select all rows from the table
$sql = "SELECT * FROM $table_name";
$result = mysqli_query($link, $sql);

if (!$result) {
    die("Query failed: " . mysqli_error($link));
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Database Table Output</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>Database Table Output</h1>
    <table>
        <thead>
            <tr>
                <?php
                // Fetch the field names and display them as table headers
                $fields = mysqli_fetch_fields($result);
                foreach ($fields as $field) {
                    echo "<th>{$field->name}</th>";
                }
                ?>
            </tr>
        </thead>
        <tbody>
            <?php
            // Fetch and display the rows from the table
            while ($row = mysqli_fetch_assoc($result)) {
                echo "<tr>";
                foreach ($row as $cell) {
                    echo "<td>{$cell}</td>";
                }
                echo "</tr>";
            }
            ?>
        </tbody>
    </table>
</body>
</html>

<?php
// Close the database connection
mysqli_close($link);
?>
