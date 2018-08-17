# エンティティの一覧表示とindex()

* エンティティの一覧を表示する`R`ead(取得)
* これは、`index`アクションとして用意する

## find()

* 開発では、`IDからの検索`のためにはIDを取得するための検索が必要
* そのためのメソッドが、`find()`
* findを利用して得られるのは`Query`というオブジェクト
* これを利用して検索を行うのがCakePHP3の基本
* このQueryを使った検索の仕組みは、`Query Builder`と呼ばれる
* `検索型名`とは、`何を検索するかを指定`すること

```php
find (【検索型名：文字列】,【検索条件：配列】)
```

## コントローラー側のメソッドの追加

```php
<?php
//src/Controller/PersonsController.php
namespace App\Controller;

use App\Controller\AppController;

class PersonsController extends AppController
{

    public function index()
    {
        $this->set('persons', $this->Persons->find('all'));
    }
}
```

* `set()`を使い、`'persons'`という名前で値を保管しているだけ
* 問題は保管している値
* ここでは、以下のような文が指定されている
    * `$this->Persons->find('all');`
        * これは、Personsの`全エンティティを取り出す`ための処理
        * `find()`: `エンティティを検索し取得する`
* 引数に`all`という検索型名を指定すると、全エンティティを検索する
* この`find('all')`で得られる値は、エンティティの配列
    * これをそのまま`set()`で`'persons'`という変数に設定
    * あとは、テンプレート側で、受け取った配列から値を取り出し表示する


## 検索型名として使えるのは、以下

| 検索型名 | 取得できるもの |
|:----|:----|
| all | 対象レコード`全件`を取得普通の検索 |
| first | 対象レコードのうち`１件目`を取得 |
| count | 対象レコードの`件数`を取得 |
| neighbors | 対象レコードのうち、`Model->id`に指定されたIDの`前後のレコード`を取得 |
| list | 対象レコードを`ID=>displayField`の書式で取得 |
| threaded | `parent_id`項目を使ってレコード間に親子関係が成立している時、`parent_id`で検索すると`親子レコード`をセット検索できる |

先ほどの`MeetingroomsController.php`の`index()`の末尾に、下記の1行を追加

```php
//findの検索結果の取得
debug($this->Persons->find('all', array()));
```

## エンティティ一覧のテンプレート

* エンティティ一覧表示のテンプレートを用意
* `src/Template/Persons/index.ctp`を作成
* コントローラー側では、personsという名前で`find('all')`した結果を保管していた
* テンプレートでは、このpersons`から順に値を取り出しては変数$person`に納めていく
* 繰り返しの中では、`<?= $person->id ?>`と、エンティティのプロパティを取り出して出力

```html
<!--src/Template/Persons/index.ctp-->
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
<?php foreach ($persons as $person); ?>
    <tr>
        <td><?= $person->id ?></td>
        <td><?= h($person->name) ?></td>
        <td><?= h($person->age) ?></td>
        <td><?= h($person->mail) ?></td>
    </tr>
<?php endforeach; ?>
</tbody>
</table>
```

## h(○○)ってなに？

* `h`という関数のようなものの引数としてエンティティのプロパティを記述
    * `h`: PHPの`htmlspecialchars`関数の短縮系
    * `h(○○)`と書けば、○○をエスケープ処理して出力する

## 自在な検索

* 取得したデータの形式は`read()`のときと似たところがある
    * しかし、`find()`の場合は、対象が複数件になる可能性がある
        * `read()`の結果に`0,1,2,...`と添え字をつけて、さらに`配列`に格納する
* `関連テーブル`の`読み込み範囲`を制限
    * `$this->MeetingRoom->recursive = 0;`
        * `read()`のときには一緒に検索できていた`関連テーブル`のデータが読み込まれなくなる
        * `一覧表示`で`関連テーブル`まで読み込むと、パフォーマンスが悪化しかねないため

もう一つ、もっと自由度の高い検索を実現する方法がある

* `SQLをダイレクトに実行する方法`

```php
array query (【SQL文：文字列】)
```

CakePHPを使っていてダイレクトに`SQL`を発行する機会はそれほど多くない
