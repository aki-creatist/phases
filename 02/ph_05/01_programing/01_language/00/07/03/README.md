# foreach文

* foreach文は**配列や連想配列を一度に処理する**ことができる
* さらに、foreach文を入れ子にすると多次元配列を操作可能

## 構文1 - 配列の操作

### 構文

```php
foreach ($配列 as $変数) {
    処理;
}
```

```javascript
配列.forEach (コールバック関数)
```

### 実践

```php
weeks = ["月", "火", "水", "木", "金", "土", "日"];
```

```php
foreach ($weeks as $week) {
    echo $week; // 月火水木金土日
}
```

```javascript
weeks.forEach (function(week) {
    console.log(week)
})
```

## 構文2 - 連想配列の操作

### 構文

```php
foreach ($配列 as $キー => $変数) {
    処理;
}
```

```javascript
配列.forEach (コールバック関数)
```

* forEachは配列に対するメソッドなので、連想配列のキー名称を配列化したのちにforEachを行う

```javascript
var 連想配列 = { ... }

Object.keys( 連想配列 ).forEach(コールバック関数)
```

* 第二引数に連想配列を指定することで、ループ処理内の「this」が連想配列を指す

```javascript
var 連想配列 = { ... }

Object.keys( 連想配列 ).forEach(コールバック関数, オブジェクト)
```

### 実践

```php
$members = ["name" => "AKI", "age"  => 29];

foreach ($members as $key => $value ) {
    echo "$key : $value";
}
```

```javascript
var members = {"name": "AKI", "age": 29};

Object.keys(members).forEach(function(key) {
    console.log(key + ':' + members[key]);
})

// this でオブジェクトを指定する
Object.keys(members).forEach( function(key) {
    console.log( key + ':' + this[key] );
}, members)
```

## 多次元配列の展開

* https://github.com/aki-creatist/php_beginner/blob/master/var/www/html/loop/forEach.js

### if文でキーを判定する

```php
foreach ($member as $key => $value) {
    if ($key == "name") {   // 取り出した$keyを == を使って name と等しいかどうか確認
        $title = "名前";
    } elseif ($key == "age") {
        $title == "年齢";
    } elseif ($key == "tall") {
        $title = "身長";
    }
    echo "$key:$value";
    echo '<br>';
}
```

## スクリプトブロックと固定テンプレート

* スクリプティングデリミタ（<?php...?>）で囲まれたスクリプトブロックに対して、それ以外の箇所、固定的なHTMLソースのことを「固定テンプレート」、または、「HTMLテンプレート」と呼ぶ
* 制御構文のブロックの一部として繰り返し使用される
* PHPページにおける固定テンプレートは、扱いとしてはprint命令と等価であると考えてもよい
* forループ（やその他の制御命令）の途中でスクリプトブロックを区切ることができ、その中に固定テンプレートがふくまれていても正しく実行される
* ある程度まとまった文字列の出力がスクリプトブロックに含まれている場合には、積極的に固定テンプレートに切り出すことで、コードをよりシンプルに記述可能
