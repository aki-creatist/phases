# バリデーション

### サンプル

ルールを追加して実行する`add()`のサンプル

```php
public function add()
{
    $person = $this->Persons->newEntity();
    $this->set('person',$person);
    if ($this->request->is('post')) {
        $validator = new Validator();
        $validator = add(
            'age','comparison',['rule' =>['comparison','>',20]] //ageに20より大きい値のみ受け付け
        );
        $errors = $validator->errors($this->request->data);
        if (!empty($errors)){
            $this->Flash->error('comparison error');
        } else {
            $person = $this->Persons->patchEntity($person,
                $this->request->data);
            if ($this->Persons->save($person)) {
                return $this->redirect(['action' => 'index']);
            }
        }
    }
}
```

* `$errors = $validator->errors($this->request->data);`
    * 注意: チェックする対象は、送信されたフォームの情報であり、エンティティ(`$person`)ではない
    * また、これとは別に、`$person`ではテーブルクラスの`validationDefault`に用意されたバリデーションもチェックされる
    * `validationDefault`の代わりになるわけではないので注意

エラーメッセージを個別に指定したい場合、以下のようにvalidation定義時に引数に指定することで可能になる

```php
//Validationの例
/**
 * 編集用バリデーション
 * @param \Cake\Validation\Validator $validator
 * @return \Cake\Validation\Validator
 */
public function validationEdit(Validator $validator) {
    $validator
        ->notEmpty('day','日付は必須です。')
        ->lengthBetween('day', [10, 10], '日付は10桁で入力してください。')
        ->date('day', ['ymd'], '日付は年月日の形式で入力して下さい。')
        ->notEmpty('title','タイトルは必須です。')
        ->maxLength('title', 120, 'タイトルは120文字以内で入力してください。')
        ->allowEmpty('text')
        ->maxLength('text', 1024, 'コメントは1024文字以内で入力してください。')
        ->allowEmpty('url')
        ->maxLength('url', 120, 'URLは120文字以内で入力してください。')
        ->allowEmpty('area')
        ->integer('area', 'エリアは正しい形式で選択してください。')
        ->allowEmpty('open_flag')
        ->integer('open_flag', '表示状態は正しい形式で選択してください。')
        ->allowEmpty('time_flag')
        ->integer('time_flag', '最終更新時間は正しい形式で選択してください。');
    return $validator;
}
```

コントローラ側は以下のようになる

```php
$validate = $model->newEntity($this->request->data(), ['validate' => 'edit']);
```

* 値にeditと指定するだけでTableクラスの`ValidationEdit()`を呼び出し可能
    * キーにvalidationを指定する

実際には以下のように処理を進めていくことがほとんど

```php
///編集処理の例
public function edit($id, $type)
{
    if (!$model) {
        $this->Flash->error('不正なパラメータが設定されました');
        return $this->_redirectIndex();
    }
    $validate = $model->newEntity($this->request->data(), ['validate' => 'edit']);
    if (empty($validate->errors())) {
        // データの存在のみチェック
        $fields     = $this->_setEditParams($type);
        $result     = $model->updateAll($fields, $conditions);
```


* また、これらはメソッドは`Modelクラス`のメソッドだけあって、DBアクセスも容易
* 入力チェックを`Modelクラス`内で行うメリット
* CakePHPでは、入力チェックの処理順として、`単一項目のチェック`と`相関チェック`を分けない
    * 相関チェック: さらにその後のDBを使用するチェック
    * CakePHPの入力チェックの基本思想が「項目単位」だから
