# DB接続

```php
<?php
$dsn = 'mysql:host=' . 'dbserver' . ';dbname=' . 'project' . ';charset=utf8';
$user = 'user';
$password = 'pass';
$dbh = new PDO($dsn, $user, $password);
$sql = "SELECT version();";
foreach ($dbh->query($sql, PDO::FETCH_ASSOC) as $row) {
    print_r($row);
}
```