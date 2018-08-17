# While文

* while文は、**ある条件のときだけ繰り返す**というときに使用する
* はじめに条件を判断し、ある条件が成立する間、処理を繰り返す
* while文は、データの数がわからない時の繰り返し処理に便利

```text
// 処理が一つの場合
while (条件式) 処理;

// 処理が複数ある場合は、「{ }」で処理を囲みます。
while ( 条件式 ) {
    処理1;
    処理2;
}
```

## wnile文の動作を確認する

* 代入
    * 変数$iに`0`
* 判定
    * while文に指定された条件式`$i <= 10`
* 増幅式
    * `++`

処理が実行は、$iは`0`なので、`10`よりも小さく、条件式の結果はTRUEとなり、実行される

```text
$i = 1 ;
while ($i <= 5) echo $i++; // 12345
```

## 条件の工夫

* 条件部分は以下のような書き方もできます。

```text
// $処理結果がfalse以外
while (false !== ($処理結果 = 処理(引数)))
```

* https://github.com/aki-creatist/php_beginner/blob/master/var/www/html/loop/read_files_in_dir.php

## endwhile

```text
while (条件式):
    処理1;
    処理2;
endwhile;
```

* https://github.com/aki-creatist/php_beginner/blob/master/var/www/html/loop/endwhile.php

## do…while文

* while文とdo…while文の違いは、条件式の判定箇所

```text
do {
    処理;
} while (条件式);
```

* https://github.com/aki-creatist/php_beginner/blob/master/var/www/html/loop/do_while.php
