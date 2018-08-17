# ダイナミックファインダー

* 複雑な条件の検索だけでなく、アプリケーションでは`シンプルな検索`も多用される
    * 特定のフィールドから指定した値のものを探す、というような検索
* では、それ以外のフィールドから検索するためのものはないか？
* それは`ダイナミックファインダー(Dynamic finder)`と呼ばれるもの

## findBy○○

* このような名前のメソッドがモデルに自動生成される(○○の部分にはテーブルのフィールド名が入る)
* 例えば、personsテーブルでは、id,name,age,mailといったフィールドが用意されているため
* 以下のようなメソッドが自動的に作成されている
    * findById
    * findByName
    * findByAge
    * findByMail
* 引数に検索する値を渡して呼び出せば、その値のエンティティが全て取り出せてしまう
* `find()`を以下のように書き換える

```php
public function find() {
    $this->set('msg', null);
    $persons = [];
    if ($this->request->is('post')) {
        $find = $this->request->data['find'];
        $persons = $this->Persons->findByName($find);
    }
    $this->set('persons, $persons);
}
```

* 入力フィールドにテキストを書いて送信する
    * nameからテキストを検索してエンティティを表示する

## １件表示(view)

* 特定のデータの表示処理
    * `URI`で指定された`ID値`は、`メソッド`の引数として引き継がれる
    * その値でDBを検索し、その結果を画面に引き継いでいる

```php
 /**
  * view method
  *
  * @throws NotFoundException 指定IDのデータが存在しない。
  * @param string $is データのID値
  * @return void
  */
public function view ($id = null) {
    // IDの存在チェック
    if (!this->Meeting->exists ($id) {
        throw new Not FoundException(__('Invalid meeting'));
    }
    // 抽出条件の組み立て(Meeting.idが$idであるデータ)
    $options = array('conditions' => array(
        'Meeting.' . $this->Meeting->primaryKey => $id
    });
    // 検索して結果をViewに引き渡す
    $this->set('meeting',
        $this->Meeting->find('first', $options)
    );
}
```



