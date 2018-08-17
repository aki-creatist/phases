<?php
require_once '../config.php';

$dsn = 'mysql:host=' . HOST . ';dbname=' . NAME;
    try{
        $pdo = new PDO( $dsn, USER, PASS );
        $pdo -> setAttribute( PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION );
        $pdo -> setAttribute( PDO::ATTR_EMULATE_PREPARES, false );
        echo "接続しました<br>";
    }catch (PDOException $Exception){
        die( 'エラー:' .$Exception->getMessage());
    }

$search_key = '';

if (isset($_POST['search_key']) && $_POST['search_key'] !== '') {
    $search_key = '%' . $_POST['search_key'] . '%';

    try {
        $sql = "SELECT * FROM board WHERE name like :name OR contents like :contents";
        $stmh = $pdo->prepare($sql);
        $stmh->bindValue(':name', $search_key, PDO::PARAM_STR);
        $stmh->bindValue(':contents', $search_key, PDO::PARAM_STR);

    } catch (PDOException $Exception){
            echo "エラー:" . $Exception->getMessage();
    }
} else {
    $sql = "SELECT * FROM board ";
    $stmh = $pdo->prepare($sql);
}
$stmh->execute();
$count = $stmh->rowCount();

echo "検索結果は" . $count . "件です。<br>";
?>

<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<title>掲示板</title>
</head>
<body>
<form method="post" action="">
    検索
    <input type="text" name="search_key" value="">
    <input type="submit" value="検索">
</form>
<?php
if ($count < 1) {
    echo "検索結果がありません<br>";
} else {
?>

<table width ="450" border="1" cellpacing = "0" cellpadding = "8">
<tbody>
    <tr>
        <th>id</th>
        <th>名前</th>
        <th>内容</th>
    </tr>
<?php
$data = [];
while ($row = $stmh->fetch(PDO::FETCH_ASSOC)) {
    $data = $row;
?>
    <tr>
        <td><?php echo htmlspecialchars($data['id']) ?></td>
        <td><?php echo htmlspecialchars($data['name']) ?></td>
        <td><?php echo htmlspecialchars($data['contents']) ?></td>
    </tr>
<?php
}
?>
</tbody>
</table>
<?php
}
?>
</body>
</html>
