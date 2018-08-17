# 削除(delete)

* 削除で行うことは更新処理とほとんど同じ
    * アクセス時に渡されたID番号をもとにエンティティを検索
    * それを使ってフォームを作成
    * 送信されたら、そのエンティティを削除
* 最後に実行するのが`更新する`と`削除する`と違うだけで、それ以外は更新と同じ

## まずはテンプレートの作成

```bash
touch Template/Persons/delete.ctp
```

```php
<div>
    <h3>Delete Person</h3>
    <?= $this->Form->create($person) ?>
    <fieldset>
        <?php
            <p>ID: <?= h($person->id); ?></p>
            <p>NAME: <?= h($person->name); ?></p>
            <p>AGE: <?= h($person->age); ?></p>
            <p>MAIL: <?= h($person->mail); ?></p>
        ?>
    </fieldset>
    <?= $this->Form->button('Submit') ?>
    <?= $this->Form->end() ?>
</div>
```

* ここでは、フォームを一つ用意
* `$person`を引数に指定して、フォームを生成している点も更新のフォームと同じ
    * `<?= $this->Form->create($person) ?>`
* フォーム内にあるのは、エンティティの値を出力するためのタグのみ
    * `<?= h($person->id); ?>`
* 入力フィールドなどは一切ない
    * ただ、Submitボタンが表示されるだけ
    * つまり、何も値を`送信しないフォーム`
    * このフォームは、何かの値を送るためのものではない
    * 単に、deleteアクションに`POST送信する`というためのもの
* つまり、ただ送信するだけのフォームを用意しておいたということ
    * コントローラー側のアクションメソッドで、処理をさせるため
        * 処理: `GETならエンティティを表示し、POSTなら削除する`
* コントローラー側にエンティティ削除の`delete()`を用意

```bash
vim PersonsController.php
```

```php
public functoin delete($id = null)
{
    // ID番号をパラメータに指定してアクセスし、getで指定のIDのエンティティを取得
    $person = $this->Persons->get($id);
    
    // POSTをチェック
    if ($this->request->is(['post', 'put'])) {
    
        // モデルのdelete()で削除( 引数にはエンティティを渡す )
        if ($this->Persons->delete($person)) {
            return $this->redirect(['action' => 'index']);
        }
    } else {
        $this->set('person', $person);
    }
}
```

```bash
vim MembersController.php
```

```php
public function delete($id = null)
{
    // POSTをチェック
    $this->request->allowMethod(['post', 'delete']);
    
    // ID番号をパラメータに指定してアクセスし、getで指定のIDのエンティティを取得
    $member = $this->Members->get($id);
    
    // モデルのdelete()で削除( 引数にはエンティティを渡す )
    if ($this->Members->delete($member)) {
        $this->Flash->success(__('The member has been deleted.'));
    } else {
        $this->Flash->error(__('The member could not be deleted. Please, try again.'));
    }

    return $this->redirect(['action' => 'index']);
}
```

* ID番号をパラメータに指定してアクセス
* 例えば、ID = 1のエンティティを削除したければ、以下のようにアクセス
    * http://localhost:8765/persons/delete/1
* 削除するデータの内容が表示される
* 内容を確認し、削除したければ送信ボタンをクリックする
* deleteには、引数にエンティティを渡す
* これにより、そのエンティティのレコードをデータベースから削除
* 正常に削除がされれば、deleteはtrueを返す
* 削除に失敗するとfalseを返す
    * この返値をチェックすることで削除できたかどうかを確認可能

## 削除処理

* まずは単純に、指定された`IDのレコード`を削除する方法

```php
boolean delete (【id:数値】,【従属データも削除するか:bool】)
```

* `第一引数`の`id`は、`削除したいレコードのID`
* `第二引数`の`従属データも削除するか`は、注意が必要
* CakePHP基本思想
    * `データを削除したらそのデータに従属しているデータ(削除データがhasOne,hasManyで所有しているデータ)も削除する`
* 例
    * `会議室レコード`を削除したら、その`会議室`を使っている`会議情報`もざっくり消すことによって`データの不整合`を無くそうというもの
    * もちろん、削除されるのは従属しているデータだけなので、`会議情報`を削除したからといって、`会議室情報`まで消えることはない
    * この引数の初期値は、true(削除する)なので、必要に応じて変更する
* このメソッドの戻り値は`boolean`
* 削除成功なら`true`を、削除失敗なら`false`を返す

### 一括削除処理

* 複数レコードの削除考え方としては更新のときの`updateAll()`と類似
* `第一引数`の`削除条件`
    * `find()`の`検索条件`(conditions)の中に書く内容と同じ
* `第二引数`の`従属データも削除するか`
    * `delete()`と同じ(指定しない場合の初期値は`true`(削除する))
* `第三引数`の`コールバックメソッドを呼び出すか`
    * 削除の前後に`コールバックメソッド`を呼び出すかを指定する
    
```php
boolean deleteAll (
    【削除条件:配列】,
    【従属データも削除するか:bool】
    【コールバックメソッドを呼び出すか:bool】
)
```

* コールバックメソッドの初期値がfalse(呼び出さない)になっていることに留意が必要
* このメソッドの戻り値も`boolean`(`true`(削除成功)、`false`(削除失敗))

### $this->request->is(['post', 'put'])の秘密

* `is()`の引数について補足
* コントローラーでは、POST送信されたことをチェックするのに、`is()`を使用した
* 例: `add()`
    * `if ($this->request->is('post')) {.....`
* ところが、editやdeleteでは以下の形で使われていた
    * `if ($this->request->is(['post', 'put')) {.....`
* この違いは
* 引数の`['post', 'put']`というのは、
* editやdeleteでアクセスした際に生成されるフォーム内に以下のタグが書かれている
    * `<input type="hidden" name="_method" value="PUT">`
        * フォームヘルパーを使い、`create`の引数にエンティティを設定時に自動追加されるもの
        * これにより、フォーム送信すると、自動的に`_method`という項目が送信されることになる
* requestの`is()`は、単純に`アクセス方式がGETかPOSTか`をチェックしているわけではない
* アクセス方式の情報(`<form>`のmethod属性の値)は、`_method`という変数に保管されている
    * `is`は、この`_method`の値をチェックしているもの
    * 普通にフォームを送信すると、この`_method`の値は'post'になる
* しかしフォームにエンティティを設定した場合、`_method`という項目が合わせて送信される
    * `_method`の値は、`['post', 'put']`になる
* このため、エンティティを設定したフォームを送信した場合は、`is('post')`では、POST送信したと判断されなくなる
* 続く`削除`系の`コールバックメソッド`については、下記の通り

```php
//削除処理のコールバックメソッド
class Aaa extends AppModel {
/**
 * 削除処理実行前に呼び出される処理
 *
 * @param boolean $cascade 従属レコードも削除するか
 *    
 * @return boolean
 *        ・true :     以降の削除処理を継続する
 *        ・false :     削除処理を取りやめる
 */
    public function beforeDelete ($cascade = true) {
        return true;
    }
    
/**
 * 削除処理実行後に呼び出される処理
 *
 * @return void 戻り値不要
 */
    public function afterDelete () {
    }
}
```

* 削除の場合は、少し特別
    * `検索`/`更新`では`コールバックメソッド`を呼び出しを制御できた
* まず`delete()`は`コールバックメソッド`の`呼び出し要否`を制御不可
* 必ず呼ばれる
* 次に`deleteAll()`はメソッドの`第三引数`として、`コールバックメソッド呼び出しの要否`を指定可能
    * セットできる値は`true`(呼び出す)、`false`(呼び出さない)の２種類だけ
    * 初期値は`false`(呼び出さない)

#### Behaviorの実装　論理削除

* `論理削除`を、`Behavior`で実装する

```php
//論理削除Behavior
<php

/* app/Model/Behavior/MyDeleterBehavior.php */

class MyDeleterBehavior extends ModelBehavior {

/**
 * Behavior読み込み時に呼ばれるメソッド。
 * コンストラクタ的な位置付けと思えば近いかも。
 * 特に初期処理が必要ないなら省略可。
 *
 * @param Model $Model モデルのインスタンス
 * @param array $config Behavior の設定情報
 * @return void 戻り値不要
 */
public function setup (Model $Model, array $settings = array()) {
}

/**
 * 指定されたレコードの論理削除を行う
 * @param Model $Model 削除を行うModelのインスタンス
 * @param type $id 削除レコードのID
 * @return boolean 論理削除の結果(true:成功、false:失敗)
 * @throws NotFoundException 指定されたデータが存在しない
 * @throws FatalErrorException テーブルに削除フラグが無い
 */
    public function logicalDelete (Model $Model, $id = null) {
        if (empty ($id) {
            $id = $Model->id;
        }
        // 対象データが存在するか
        if (!$Model->exists($id)) {
            throw new NotFoundException('そんなIDのデータはないよ');
        }
        // このテーブルに項目`削除フラグ`があるか
        $tableConst = $Model->getDataSource()->describe($Model);
    debug($tableConst);
        if (!isset($tableConst['delete_flg'])) {
            throw new FatalErrorException('削除フラグがないよ');
        }
        // 更新データ組立
        $data = array(
            $Model->alias => array(
                'id' => $id,
                'delete_flg' => true,
            )
        );
    debug($data);
        // 更新
        $sts = $Model->save($data, array('validate' => false));
        if ($sts === false) {
            return false;
        } else {
            return true;
        }
    }
}
?>
```

* `メソッド`が呼ばれたら、`物理削除`はしないで`削除フラグ`を立てているだけ

## Behaviorの約束事

* `Behaviorの名前`は`キャメルケース`とする
* クラス名は`(Behaviorの名前)+("Behavior")`とする
* ファイル名は`(クラス名)+(".php")`とする
* Behaviorクラスは`ModelBehaviorクラス`を継承する
    * `自動的に`というのがポイント
    * あなたのプログラムがこのメソッドを呼び出す場合には引数が１つ少なくなる

#### Behaviorの組み込み

* まずは、`Modelクラス`に読み込み定義する
* これは`Modelクラス`の`$actsAs`に、下記のように記述する

```php
//Behaviorの読み込み宣言
/* app/Model/Member.php */

class Member extends AppModel {

    // 設定情報を引き継がない場合
    // public $actsAs = array('MyDeleter');
    
    // 設定情報を引き継ぐ場合
        public $actsAs = array(
            'MyDeleter' => array(
                'opt1' => 'opt1value'
            )
        );
    );
〜以下略〜
```

* `設定情報`を引き継ぐ場合と、引き継がない場合を列挙している
* `設定情報`を引き継ぐ場合、その情報は`setup()`の引数`$setting`に引き継がれる
* `メソッド`の呼び出し側
* `論理削除メソッド`の呼び出しに書き換える
    * `メンバー・コントローラ`の`delete()`内で、`削除メソッド`を呼び出している箇所

```bash
vim app/Controller/MemberController.php
```

```diff
  //Behavior()の呼び出し
- if ($this->Member->delete()) {
+ if ($this->Member->logicalDelete($id)) {
```

* これで、`メンバー削除処理`は実際の削除は行わず、`削除フラグ`を立てるだけになった
* Behaviorのメソッドのはずなのに、まるで`モデル`の`メソッド`のように呼び出している
* `Behaviorはまるでモデルの一部のように振る舞う`というのは、こういうこと
* `修正範囲`の狭い方法を採用
    * ここでは、`logicalDelete()`が`モデル`の一部のように見えることを理解するため
* しかし、こうやって拡張を続けると、メソッドの数が増える
* CakePHPの基本思想は`同じような処理はあまり別メソッドにせずにオプションでバリエーションを持たせよう`
* そのため、例えば、基底クラスである`AppModel.php`の中で、

```php
//app/Model/AppModel.php
class AppModel extends Model {

    public function delete ($id = null, $option = array()) {
        // デフォルトオプションに指定オプションを上書き
        $defaultOpt = array(
            'cascade' => true, 'logicalDelete' => false
        );
        if (is_bool ($option)) {    // 既存の呼び出し方式場合
            $defaultOpt('cascade') = $option;
            $option = array();
        }
        $option = array_merge ($defaultOpt, $option);
        // DBアクセス処理呼び出し
        if ($option['logicalDelete']) {
            if (function_exists ($this, 'logicalDelete')) {
                // 論理削除
                $sts = $this->logicalDelete ($id);
            } else {
                throw new FatalErrorException (
                    'MyDeleterBehaverが導入されていないのでは？');
            }
        } else {
            // 物理削除
            $sts = parent::delete($id, $option['cascade']);
        }
        return $sts;
    }
}
```

と、`delete()`をオーバーライドしてオプションを追加すると、

```php
app/Controller/MembersController.php
    if ($this->Member->delete($id,
        array ('logicalDelete' => true)) {
```

のようにオプションを指定だけで論理削除が実現可能
