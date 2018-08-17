<?php
require_once '../config.php';

// データソースネーム
$dsn = 'mysql:host='. HOST .';dbname='.NAME;
// データベースハンドラ
$dbh = new PDO($dsn, USER, PASS);

$sql  = "SELECT "
        . "id, "
        . "name, "
        . "contents, "
        . "created_at, "
        . "updated_at "
        . "FROM board"
        ;

$stmt = $dbh->prepare($sql);
$stmt->execute();

$data = [];
while ($result = $stmt->fetch(PDO::FETCH_ASSOC)) {
    array_push($data, $result);
}

arsort($data);
?>
<!doctype html>
<html>
<head>
<meta charset="UTF-8">
<title>掲示板</title>
</head>
<body>
<!-- ここに、書き込まれたデータを表示する -->
<table border="1px">
    <tr>
        <th>id</th>
        <th>name</th>
        <th>contents</th>
        <th>created_at</th>
        <th>updated_at</th>
    </tr>
<?php
    foreach($data as $val)
    {
        echo "<tr>";
        echo "<td>" . $val['id'] . "</td>";
        echo "<td>" . $val['name'] . "</td>";
        echo "<td>" . $val['contents'] . "</td>";
        echo "<td>" . $val['created_at'] . "</td>";
        echo "<td>" . $val['updated_at'] . "</td>";
        echo "</tr>";
    }
?>
</table>
</body>
</html>
