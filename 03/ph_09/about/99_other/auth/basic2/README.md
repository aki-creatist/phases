# Basic認証

# プログラム内のIDとPWで認証

## 確認画面を表示する

* IDとパスワードをプログラム内部に設定してアクセスを制限する
* Basic認証の仕組みを利用して動作を確認可能
* PHPのheader関数を活用するとBasic認証のログイン画面を表示可能
* この機能を利用して簡単な認証システムをPHPで作成する
* 下記のコードは認証画面を表示するだけの機能しかない
    * [auth_test1.php](https://github.com/aki-creatist/exam1/blob/master/var/www/html/basic2/auth_test1.php)
* header関数に`WWW-Authenticate`と`HTTP/1.0 401 Unauthorized`というメッセージを設定
    * 送信すると認証画面が表示される
    * realm属性の`Member Only`が画面に表示される

### ユーザー名とパスワードを受け取る

* 設定画面に入力されたユーザーIDとパスワードは以下に格納される
    * `$_SERVER['PHP_AUTH_USER']`
    * `$_SERVER['PHP_AUTH_PW']`
* if文の中でempty関数を使って以下が空かどうかでチェックする
    * `$_SERVER['PHP_AUTH_USER']`または`$_SERVER['PHP_AUTH_PW']`
* どちらか一方でも値がない場合
    * `header`関数によって認証画面が表示される
    * 認証画面から、任意の文字列をユーザーIDとパスワードとして送信すると、elseブロックが実行され、画面に入力した文字列が表示される

#### realm属性の`"`

* realm属性は`"`(ダブルクォーテーション)で囲む必要がある
* Webサーバーとブラウザ間のやりとり上の決まり
* header関数の引数も同じ`"`で囲んでいるため、realm属性の`"`は、このまま実行するとPHPの動作条件によりエラーになる
* これはrealm属性の`"`が`header`関数の引数の終わりだとPHPに誤認識されるため
* ここでは`¥`または`\`でエスケープ(機能を無効に)して、`"`が文字列として使用できるようにする

### 認証する

* 認証画面の`キャンセル`がクリックされる
    * `キャンセルされました`と表示される
* `$_SERVER['PHP_AUTH_USER']`に値がある場合
    * 以下の条件式でユーザーIDがsample、パスワードがpasswordと入力された場合だけその後に続く認証済み画面が表示される

```php
if ($_SERVER['PHP_AUTH_USER'] == "sample" && $_SERVER['PHP_AUTH_PW'] == "password") {
```

### 実行する

#### 認証画面を表示する

* `basic_auth.php`をApacheのDocumentRootに設置
* Webブラウザからbasic_auth.phpにアクセスする
* 認証画面が表示される

#### 画面を表示する

* ユーザー名に`sample`、パスワードに`password`と入力してOKをクリック
* `こんにちは、sampleさん。`とユーザー名に入力した文字列が表示される
