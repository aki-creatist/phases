# 基本

データの検索は、メソッドを呼び出すだけで複雑な検索を行う`Query Builder`という仕組みが用意されている

* ブラウザから指示を受け取ったら、今度はそれに該当する`データ`を`検索`
* `検索`には、`モデルクラス`を使用

```php
<?php
App::uses ('AppController', 'Controller');

class MeetingRoomsController extends AppController {
    
    public function view ($id = null) {
        $data = $this->MeetingRoom->read($id);
    }
}
```

* 上記のソースコード中の、`MeetingRoom`というのが、モデルクラス
* `$this`がコントローラ・クラス
    * モデル・クラスのインスタンスが、コントローラのメンバーのようになっている
    * CakePHPのコントローラでは、まるでメンバー変数のようにデフォルトモデルにアクセス可能
        * `デフォルトモデル`: コントローラに対応したモデルクラス
* `コントローラの名前`と`モデルの名前`が一致しない場合もある
    * コントローラのメンバー変数`$uses`に`モデル名`をセットする
    * `デフォルトモデル`と同様の操作が可能になる
* `デフォルト・モデル`に他のモデルとの関連付けを定義してある場合
    * 関連先の`会議テーブル`の検索も可能
    * `$this->MeetingRoom->Meeting->read($id)`という形
