# Authクラスの作成

## Authクラス

* クラスの名前と主なメソッド
    * [AuthController.php](AuthController.php)    
* 実装
    * [AuthController.php](https://github.com/aki-creatist/smarty/blob/master/project/php_libs/controller/AuthController.php)

## 認証情報の格納先

* SESSIONはあらかじめ認証情報を格納する配列名を決めておく
    * 会員の認証情報は`$_SESSION['userinfo']`格納する
    * 管理者の認証情報は`$_SESSION['systeminfo']`に格納する

## 概要

* セッション名の指定
    * セッション名は初期値として`PHPSESSID`と決められている
    * 会員側と管理側でセッション名を変えておくと安全性が高められる
* セッションの開始
* 認証情報の確認
* 認証情報の破棄

# Sessionクラスの作成

## Sessionクラス

* クラスの名前と主なメソッド
    * [SessionController.php](SessionController.php)
* 実装
    * [SessionController.php](https://github.com/aki-creatist/smarty/blob/master/project/php_libs/controller/base/SessionController.php)

# Authクラスの組み込み

## Authクラスでセッション開始

* testauth1.phpにAuthクラスを組み込んで、testauth2.phpを作成する
    * `$auth = new Auth;`として、Authクラスのメソッドを`$auth->メソッド()`と指定して実行可能
    * はじめに`set_authname()`で定数`_MEMBER_AUTHINFO`を設定する
    * 設定ファイル`init.php`で`_MEMBER_AUTHINFO`を`userinfo`として定義している
    * init.phpで`_MEMBER_SESSNAME`を`PHPSESSION_MEMBER`と定義している
    * これは新しいセッション名となる
    * `$auth->start();`でセッションが開始される

## Authクラスで認証

* ユーザーネームとパスワードが一致したら、`$_SESSION[$auth->get_authname()]['id']`に1を追加する
* 先ほどの`set_authname`により`$_SESSION['userinfo']['id']`に`1`が格納される
* ログアウトする場合は、`$auth->logout();`を実行するだけ
* `$auth->check()`で、`$_SESSION['userinf']['id']`に`1`以上が格納されていたら認証済みとなり、会員画面が表示される

```php
if (!empty($_POST['type']) &&  $_POST['type'] == 'authenticate' ) {
    // 認証機能
    if( $_POST['username']== 'user' && $_POST['password'] == 'pass' ){
        $_SESSION[$auth->get_authname()]['id'] = 1;// 数値ならなんでもOK
    }
}else if( !empty($_GET['type']) && $_GET['type'] == 'logout'){
   $auth->logout();
}


if($auth->check()){
    // 認証済み
    $smarty->assign("title", "会員ページ");
    $file = 'testauth.tpl';

}else{
    // 未認証
```

# パスワードの保存

* パスワードは暗号化して保存する
    * 安全性を高めるため
    * ハッシュ値をパスワードからハッシュ関数で計算して保存
        * 元のデータの長さに関わらず一定の長さの文字列にする
    * `ソルト`をあらかじめ付加してパスワード解析しにくくする
        * `ソルト`: ランダムな文字列

# DB接続クラス

* DBに接続するクラス
    * MVCの`M(モデル)`にあたる
    * すべてのモデルで共通する処理を担当させる
    * BaseModelにはコンストラクタにDBへの接続処理が書かれている
* [BaseModel.php](https://github.com/aki-creatist/smarty/blob/master/project/php_libs/model/base/BaseModel.php)

### catch

* `catch()`には捕捉するPDOExceptionとオブジェクトを格納する変数$Exceptionを指定
    * dieはexitと同じでプログラムを停止して引数のメッセージを表示する
* PDOExceptionクラスの`getMassage()`によりエラーメッセージを取得して表示する
* 発生したエラーに関する情報は、PDOクラスの`errorInfo()`あるいはPDOStatementクラスの`errorInfo()`で取得する
* エラー処理の確認で文字コードを'utf9'にしてみるなど、接続エラーを表示するなどテストすると動作がわかりやすい

## BaseController

* ビュークラス(Smarty) の準備
* ページ分割処理
* デバッグ用表示処理