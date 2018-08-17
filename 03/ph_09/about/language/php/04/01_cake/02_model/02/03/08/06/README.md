# 重複行を削除する

`重複行`を削除する`DISTINCT`も使用可能

```php
//重複行の削除
find ('all', array(
    'fields' => array(
        'DISTINCT (name) as name',
    ),
))
```
