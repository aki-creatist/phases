# 比較演算子,特殊演算子

* `条件式`は必ずしも、`等号`(＝)とは限らない
* そんなときには`比較演算子`を使用する

使い方の例は下記の通り

```text
//比較演算子
'id >'    => 2,    // IDの値が２よりも大きい

'id >='    => 2,    // IDの値が２以上

'id <'    => 2,    // IDの値が２よりも小さい

'id <='    => 2,    // IDの値が２以下

'id <>'    =>2,    // IDの値が２以外
'id !='        => 2,     // IDの値が２以外

'id' => array(2,3,4),     // IDの値が２か３か４

'id BETWEEN ? AND ?' => array(2,3),     // IDの値が２から３の間

'name' => null,    // 名前がnull (IS NULLと同じ)
```
