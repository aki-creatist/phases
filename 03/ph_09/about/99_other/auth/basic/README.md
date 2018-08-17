# Basic認証

* http://localhost:8093/Basic/test.php

## パスワードファイルの作成

* パスワードファイル名
    * `.htpasswd`
* ユーザーID
    * `sample`
* パスワード
    * `password`

```bash
USER_ID='sample'
PW_FILE_NAME='.htpasswd'
PASSWD='password'

#新規作成
##対話式
htpasswd -c ${PW_FILE_NAME} ${USER_ID}
##非対話式
htpasswd -c -b ${PW_FILE_NAME} ${USER_ID} ${PASSWD}

#ユーザー追加
htpasswd ${PW_FILE_NAME} ${USER_ID}
#ユーザー削除
htpasswd -D ${PW_FILE_NAME} ${USER_ID}
```

# Basic認証

## Basic認証とは

* HTTPプロトコルで定義された認証プロトコルを使用するもの
    * 処理の流れ
        * 認証を必要とするURLにアクセスされる
        * `WWW-Authenticate: Basic realm="任意の文字列"`というレスポンスヘッダがWebサーバかrWebブラウザへ送られる
        * Webブラウザは認証ダイアログを表示
        * ユーザーがユーザーIDとパスワードを入力するまで待機状態になる
        * ユーザーIDとパスワードが入力されて送信される
            * Webサーバーでは、正しいユーザーIDとパスワードかをチェック
                * 正しい場合は、そのページを表示する
                * 認証されなかった場合は、`HTTP/1.0 401 Unauthorized`というレスポンスヘッダがWebブラウザに送信される
* 制限されたエリア(ディレクトリ)にあるファイルにアクセスすると認証画面が表示される
* 認証するには予め設定しておいたユーザー名とパスワードを入力して`OK`をクリックする

## Basic認証の手順

### `.htaccess`の設定

* `.htaccess`をドキュメントルートに準備する
    * `AuthType Basic`で、ユーザ認証の種類をBasic認証に設定している
* 引数に半角スペースが入る場合は上記のように`"`で囲う
* `AuthUserFile`、`.htpasswd`ではユーザーIDとパスワードの一覧が記録されたファイルのパスを設定する
* 絶対パス、またはServerRootからの相対パスのいずれも可
    * `Require valie-user`
        * `認証されたユーザー全てにディレクトリへのアクセスを許可する`という意味

### パスワードファイルの生成

* パスワードファイルは`htpasswd`コマンドを利用して作成する
* htpass -cとすると新規にファイルが作成され、ユーザーIDとパスワードが追加される
* コマンドを実行するとパスワード入力のためのプロンプト`New Password:`が表示される
    * パスワードを入力する
* 半角英数字で入力し、Re-Typeと再入力による確認を求められるので同じものを入力する

```text
#パスワードファイル新規作成
$ htpasswd -c パスワードファイル ユーザーID
New Password: ←パスワードを求められる
Re-Type New Password: ←同じものを入力
Adding password for user ユーザーID ←成功すると成功メッセージが表示される
```

* ファイル名は.htpasswdとして`.htaccess`のあるドキュメントルートに作成
* 名称が`.ht`で始まるファイルにアクセスしたときの動作
    * httpd.comf内の設定`Require all denied`により、エラーメッセージが表示されアクセスできない
* さらに安全にするには、.htpasswdをドキュメントルートの外に保管する

### その他のコマンド例

* オプションを付けずに実行すると、指定したファイルにユーザーIDとパスワードを追加する

```bash
#パスワードファイル追加
htpasswd パスワードファイル ユーザーID
```

* オプションに`D`を指定するとファイル内のユーザーを削除する

```bash
#パスワードファイル削除
htpasswd -D パスワードファイル ユーザーID
```

### 認証の確認

* ドキュメントルートにtest.phpを配置
* ブラウザからhttp://localhost/test.phpを閲覧する
* ログイン画面が表示されるので、ユーザIDとパスワードを入力して送信する
* Webサーバは、正しいユーザIDとパスワードかをチェックする
    * 正しい場合は、そのページを表示する
    * 認証されなかった場合は、`HTTP/1.0 401 Unauthorized`というレスポンスヘッダがWebブラウザに送信される
        * もし、何度正しくパスワードを設定しても認証されない場合はhtpasswdコマンドのバグの可能性がある
* `htpasswd`のバグを回避するには、下記を試す

```bash
htpasswd -b パスワードファイル名 ユーザーID パスワード
```
