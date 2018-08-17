# その他の検索条件の設定

## データの並び順の指定　order
    
* findで検索するとき、何も指定していないとレコードを登録した順番に取り出され
* 特定の順番で並べ替えたい場合は、この`order`を利用する
    * `検索条件`に`order`というキー名の連想配列を設定する
    * `order()`を利用する
* 例: `第１次ソートキー`は`名前の降順`、`２次キー`は`IDの昇順`と指定している

```php
//orderをキーにして並び順を指定
find('all' array(
    'order' => array(
        'name' => 'DESC', 'id' => 'ASC'
    )
));
```

```php
//order()で並び順を指定
find()
    ->order(['name' => 'DESC', 'id' => 'ASC']);
```

引数には、並べ替えの基準となるフィールド名に`ASC`または`DESC`のいずれかの値を設定した連想配列を用意する

* `Asc`: 昇順(小さいものから順に並べる)
* `Desc`: 降順

## メソッドチェーン

* 下記は`find()`にselectとorderを追加したもの
    * 検索テキストを入力して送信すると、そのテキストをnameに含むレコードをname順に並べる
    * また表示されるのはIDとnameのみで、そのほかの項目は値が表示されない

```php
//メソッドチェーン
public function find() {
    $this->set('msg', null);
    if ($this->request->is('post')) {
        $find = $this->request->data['find'];
        $persons = $this->Persons->find()
            ->select(['id', 'name'])
            ->order(['name' =>'Asc'])
            ->where(["name like "=> '%' . $find . '%']);
    } else {
        $persons = [];
    }
    $this->set('persons', $person);
}
```

ここで検索処理を行っている文を見ると、このように書かれていることがわかる

* `$this->Person->find()->select(○○)->order(○○)->where(○○);`
* メソッドが全て繋がっている
* これらのメソッドは全てQueryクラスに用意されており、しかも全て`Queryインスタンスを返す`ようになっている
* つまり、メソッドを呼び出すと、その処理を設定した自分自身が返される
* このため、こうやって次々とメソッドを連続して呼び出すような書き方が可能になっている
* こうした書き方をメソッドチェーンと呼ぶ
    * メソッドの返値をいちいち変数に代入したりする必要がなく、非常に簡単に複雑な処理を記述可能
