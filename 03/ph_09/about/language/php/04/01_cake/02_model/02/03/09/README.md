# 検索処理のコールバックメソッド

さて、しばらくSQL寄りの話が続いたので、Modelに戻る

* 前述の通りCakePHPはかなり柔軟な検索を実現可能
* 条件を毎回描くのは面倒で、バグも出やすくなる
* こういう時の解決策の一つが、`Modelクラス内に独自のメソッドを作って、そこで検索処理を代理呼び出しする`という方法

```php
class Aaa extends AppModel {
    // 論理削除状態じゃないレコードだけを検索
    function findNotLogicalDelete() {
        return $this->find ('all', array(
            'conditions' => array('delete_flg'=>)
        ));
    }
}
```

* 既存のコードの`find()`を、全部`独自メソッド`に書き換える手間が発生し、`修正漏れ`のリスクも生じる
* こんなときに便利なのが、`コールバックメソッド`

コールバックメソッドは、下記のように使用する。

```php
class Ass extends AppModel {

/**
 * 検索処理の直前に呼び出される処理
 *
 * @param array $queryData 検索条件の配列
 * ただし検索の直前に呼び出されるので、検索型に応じてCakePHPが
 * 検索条件を書き換えた後の状態
 * @return mixed
 *         ・true:                以降の検索処理を継続する
 *        ・false:            検索処理を取りやめる
 *        ・$queryData:        返された検索条件で検索を行う
 */
     public function beforeFind ($queryData) {
        // ここで検索条件を追加したり可能
        return $queryData;
    }

/**
 * 検索処理の直後に呼び出される処理
 * ただし検索直後のため検索型に応じた配列形式の変換は行っておらず
 * 検索型 "all" の時の形式
 * @param boolean $primary このモデルが主モデルかどうか
 *         true:主モデル,    false:関連モデルとして呼ばれたモデル
 * @return mixed 良いように書き換えた後の検索結果
 */
     public function afterFind ($results, $primary = false) {
        // ここで検索結果を書き換える
        return $results;
    }
}
```

このような関数を`Modelクラス`の中で実装するだけで、自動的に`検索`前後にCakePHPが呼び出してくれるというのは便利

* ただし、これだけだとコントローラ側の都合で、`今回だけはbeforeFind()で条件を変えて欲しくない！`といったケースに対応不可
* CakePHPが問答無用で呼び出してしまうため
* そんなときには、`find()`の`検索条件`として、下記のように指定

```php
find ('all', array(
    'callbacks' => 'after'    // beforeFind()は呼び出さない
))
```

このように、検索条件の`callbacks`に`'after'`をセットすると、`afterFind()`だけ呼ばれて、`beforeFind()`がスキップされる

`callbacks`にセットできる値は、以下のようになる

| | beforeFind() | afterFind()</th>
|:----|:----|:----|
| true | ○(呼ぶ) | ○(呼ぶ) |
| 'before' | ○(呼ぶ) | ×(呼ばない) |
| 'after' | ×(呼ばない) | ○(呼ぶ) |
| false | ×(呼ばない) | ×(呼ばない) |

これで、コールバックメソッドの利便性がますます上がる
