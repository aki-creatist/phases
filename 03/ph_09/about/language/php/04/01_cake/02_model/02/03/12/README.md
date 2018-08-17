# クエリーを直接実行するには？

* フレームワークのDB利用は、基本的に`いかにSQLのクエリーを排除するか`を考えて設計されている
* DB固有の部分を排除することがフレームワークの命題
* しかし、`SQLクエリーを直接実行できた方が便利`というシーンもある
    * `Connection`というクラスを利用する

## 利用の流れ

* Connectionを用意する
* StatementInterfaceを得る
* フェッチする
* クエリーを直接実行してみる

### Connectionを用意する

* `Connection`インスタンスを用意するにはいくつかの方法がある
* 基本は、`ConnectionManager`というクラスの`get()`を使う方法
* 引数には、取り出すDB設定名を指定する
    * DBの設定は、app.php内に、'Datasources'という値として用意されている
        * 通常はここにある'default'の設定が使われる
        * `get('default')`としておく
    * app.phpにいくつかの設定を用意しておけば、getで取り出す設定名を変えることで複数のDBにアクセス可能

```php
$変数 = ConnectinManager::get('default');
```

### StatementInterfaceを得る

* `query()`
    * 引数にクエリーのテキストを指定し、`statementInterface`のインスタンスを返す
* これにより、クエリーを実行するステートメントのオブジェクトが用意される

```php
$変数 = 《Connection》->query( クエリー文 );
```

### フェッチする

* ステートメントから、実際にデータを取り出するfetch`は呼び出すたびに一つずつエンティティを取り出していく
* `fetchAll`
    * 全てのエンティティをまとめて取り出す

```php
$変数 = 《StatementInterface》->fetch();
$変数 = 《StatementInterface》->fetchAll();
```

### テンプレートの修正

```bash
vim find.ctp
```

* クエリーを直接実行する場合、モデルを解さない
    * 得られるレコードは連想配列の形になって渡される
    * 連想配列の中からフィールドの値を取り出すような形に書き換えておく必要がある

```html
<!--モデル利用の場合-->
<td><?= h($person->id) ?></td>
<td><?= h($person->name) ?></td>
<td><?= h($person->age) ?></td>
<td><?= h($person->mail ?></td>
<!--連想配列の場合-->
<td><?= h($person['id']) ?></td>
<td><?= h($person['name']) ?></td>
<td><?= h($person['age']) ?></td>
<td><?= h($person['mail']) ?></td>
```

```html
<!--修正したfind.ctp-->
<div>
    <h3>Find Person</h3>
    <?= $msg ?>
    <?= $this->Form->create() ?>
    <fieldset>
        <?= $this->Form->input('find'); ?>
    <?= $this->Form->button('Submit') ?>
    <?= $this->Form->end() ?>
    </fieldset>
    <table>
    <thead>
        <tr>
            <th>ID</th>
            <th>NAME</th>
            <th>AGE</th>
            <th>MAIL</th>
        </tr>
    </thead>
    <tbody>
    <?php foreach ($persons as $person): ?>
        <tr>
            <td><?= h($person['id']) ?></td>
            <td><?= h($person['name']) ?></td>
            <td><?= h($person['age']) ?></td>
            <td><?= h($person['mail'] ?></td>
        </tr>
    <?php endforeach; ?>
    </tbody>
    </table>
</div>
```

### クエリーを直接実行してみる

* `find()`を修正
* 入力フィールドにクエリーの条件となる部分(where以降の部分)を書いて送信する
    * それを直接実行して結果を表示する
* 例: `age > 20 and age < 40`
    * こんな具合に書いて送信すると、ageの値が`20以上40未満`のものだけを検索する
* これを実行すると、DBに以下のクエリが投げられる
    * `select * from persons where age > 20 and age < 40`

```diff
+ use Cake/Datasource/ConnectionManager; // このuseを追加

  public function find() {
      $this->set('msg', null);
      $persons = [];
      if ($this->request->is('post')) {
          $find = $this->request->data['find'];
          $connection = ConnectionManager::get('default');
          $query = 'select *  from persons where ' . $find;
          $persons = $connection->query($query)->fetchAll();
      }
  }
```

