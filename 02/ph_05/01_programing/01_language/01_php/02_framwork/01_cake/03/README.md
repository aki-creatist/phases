# テストの作成と実行

これを機にtestを体験する。

## テスト用DBの作成

次に、テスト用のDBを作成する

```sql
mysql -u root -p

CREATE DATABASE test_project CHARACTER SET utf8;
CREATE USER 'user'@'localhost' IDENTIFIED BY 'pass';
GRANT ALL PRIVILEGES ON test_project.* TO 'user'@'localhost';
FLUSH PRIVILEGES;
```

## テストの実行

Git Bashで以下の入力を行う

```bash
# テストの実行
vendor/bin/phpunit tests/TestCase/Model/PersonsTableTest.php
#Tests: 2, Assertions: 0, Incomplete: 2.
```

## テストコードの編集

* 自動生成されたソースコードを少し編集する

```php
//TestCase/Model/Table/PersonsTableTest.php

public function testInitialize()
{
    //$this->markTestIncomplete('Not implemented yet.');
    $this->assertEquals('persons', $this->Persons->getTable());
    $this->assertEquals('id', $this->Persons->getPrimaryKey());    
}
```

```php
//TestCase/Model/Table/PersonsTableTest.php

public function testValidationDefault()
{
    //$this->markTestIncomplete('Not implemented yet.');
    $this->assertEquals('persons', $this->Persons->getTable());
    $this->assertEquals('id', $this->Persons->getPrimaryKey());    
}
```

## テストの実行

```bash
# テストを再度実行する
vendor/bin/phpunit tests/TestCase/Model/PersonsTableTest.php
```

以下のような実行結果になる。

```text
OK, (2 tests, 4 assertions
```

## Controllerのテストも実行してみる

```text
PHPUnit 6.1.3 by Sebastian Bergmann and contributors.
Tests: 5, Assertions: 0, Incomplete: 5.
OK, but incomplete, skipped, or risky tests!
```

## コントローラーテストを修正する

[テストソース](PersonsController.php)

```text
OK, (2 tests, 9 assertions
```

以上が単体テストの簡単な概要