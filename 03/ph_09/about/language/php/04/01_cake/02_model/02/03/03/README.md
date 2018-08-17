# find()とwhere()

* この検索条件の設定で、SQLなら最も基本となるのは`where`
* CakePHPにはfindを軸に２通りの書き方がある
    * `検索条件`に`conditions`というキー名の`連想配列`をセットする
    * クエリビルダで`where()`を使用した検索条件の設定を行う

## IDが2のレコードだけを抽出したい場合

```php
//conditionsを使用した表記
$this->モデル名->find('all', array(
    'conditions' => array(
        'モデル名.カラム名' => 値
    )
));
```

```php
$this->モデル名->find()
    ->where(["条件文" => 値 ]);
```

## 別の書き方
  
* `-> where(条件文, 値)`
* 第一引数には、条件となる文を記述するこれは、条件式の`値以外の部分
* 値: 値となるものが第二引数に指定される

## 例

* `idが1のもの`なら、`id = 1`というように条件を設定
* この`１`より前の部分が第一引数、`１`が第二引数になる
    * `１`という数技の代わりに、変数$id`を使って値を指定するなら、下記のようになる
        * 引数に式と値を指定する例
        * `find()->where('id = ', $id);`
* 実際に、Personsテーブルのidが`1`のデータを検索してみる

### conditions

```php
//conditionsでid=1を検索する例
Persons->find('all', array(
    'conditions' => array(
        'Persons.id' => 1
    )
));
```

### where

```php
//クエリビルダでid=1を検索する例
Persons->find()
    ->where(["id=" => 1]);
```

* 項目名の前の`Persons`は、モデル名
* `複数テーブル`が乱れ飛ぶような実際の開発では必須これを機会に`モデル名`をつける癖をつける

## 例

* これは入力フィールドに書いたテキストに該当するidのレコードを検索するサンプル
* 例えば、`1`と書いて送信すると、idが`1`のレコードが検索される

### conditions

```php
//conditionsを使用してidで検索をする例
public function find() {
    $persons = [];
    if($this->request->is('post')) {
        $find = $this->request->data['find'];
            $persons = $this->Persons->find('all',array(
                'conditions' => array(
                    "id" => $find
                )
            ));
            debug($persons);
    } $this->set('msg',null);
}
```

### where

```php
//クエリビルダを使用してidで検索をする例
- $persons = $this->Persons->find('all',array(
-     'conditions' => array(
-         "id" => $find
-     )
- ));
+ $persons = $this->Persons->find()
+    ->where(['id =' => $find]);
```

## 例

* 入力フィールドに書いたテキストをnameに含むレコードを全て検索する
    * 例えば、`aki`と書いて送信すると、名前に`aki`を含むものが全て検索される
* この条件文を整理すると、ここで指定されている式はこうなる
    * `name like '%○○%'`
* この○○の部分は、findの値がはめ込まれるこれは`LIKE検索(あいまい検索)`と呼ばれるもの
* テキストを含むものもを検索するのに用いられる
* `%記号`はワイルドカード(どんな文字でも当てはまる)として働く
    * `○○で始まるもの`を取り出す→'○○%'
    * `○○で終わるもの`を取り出す→'%○○'

### conditions

```php
//conditionsでnameを部分一致検索をする例
public function find() {
    $persons = [];
    if ($this->request->is('post')) {
        $find = $this->request->data['find'];
            $persons = $this->Persons->find('all',array(
                'conditions' => array(
                    "name LIKE " => '%' . $find . '%'
                )
            ));
            debug($persons);
    } $this->set('msg',null);
}
```

### where

```php
  //クエリビルダでnameを部分一致検索をする例
- $persons = $this->Persons->find('all',array(
-     'conditions' => array(
-         "name LIKE " => '%' . $find . '%'
-     )
+ $persons = $this->Persons->find()
+     ->where(["name LIKE " => '%' . $find . '%']);
```
        