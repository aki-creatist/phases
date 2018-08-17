# ○○番目からデータを取り出す offset

* データの取得開始位置の指定をし、対象データの先頭から何件ずらして取得するかは、`offset`で指定する
* 検索したデータの最初からではなく、指定した位置からデータを取り出すためのもの
* この場所を示す値は、一番最初が`ゼロ`、２番目が１、３番目が２となる
* `10番目のものから取り出した`というなら、引数は`９`になる
* 以下の２通りの書き方がある
    * `検索条件`に`offset`をキー名にして数値を指定する
    * `offset()`を利用する
* `offset`を指定する場合は、`limit`の併用が必要`

```php
//offsetをキーにして取得開始位置指定
find ('all', array(
    'offset' => 3,    // 3+1で４件目から
    'limit' => 2,    // ２件取得
))
```

```php
//offset()で取得開始位置指定
find()
    ->offset(3)
    ->limit(2);
```

先ほどのサンプルを書き換えて、修正する

```php
//メソッドチェーンで繋げる
public function find() {
    $this->set('msg', null);
    if ($this->request->is('post')) {
        $find = $this->request->data['find'];
        $first = $this->Persons->find()
            ->limit(1)
            ->where(["name LIKE " => '%' . $find . '%']);
        $persons = $this->Persons->find()
            ->offset(1)
            ->limit(3)
            ->where(["name LIKE " => '%' . $find . '%']);
        $this->set('msg', $first->first()->name .
            ' is first data.');
    } elset {
        $persons = [];
    }
}
```

* `Find Persons`のタイトルの下に`○○is first data.`というように最初のデータのnameを表示する
* そして下のテーブルには、２番目以降のデータを最大３つまで表示する

