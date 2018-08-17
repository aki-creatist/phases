# 集計単位を指定　group

SQLにおける`GROUP BY`のように、`検索結果を集計`したい場合には、`group`で集計単位を指定する

また、`集計`と一緒に使われる`集約関数`も使用可能

```php
//集計単位を指定
find ('all', array(
    'fields' => array(
        'MAX (point) as top',             // 各クラスの最高点
        'MIN (point) as worst',         // 各クラスの最低点
        'COUNT (point) as class_cnt'    // 各クラスの人数
    ),
    'group' => array('class_id')        // 集計単位
))
```