# ログ管理

* `rsyslog`
    * CentOSで使用されるシスログプログラム
    * `シスログ`: システムのログを処理するプログラム
    * `/etc/rsyslog.conf`
        * シスログの設定ファイル
        * どんなログメッセージをどのログファイルに記録するか設定変更可能
* ログローテーション
    * 古いログの削除
    * デフォルトでは４週間分しか保存されない
    * `/etc/logrotate.conf`
        * ログローテーション期間の設定ファイル
        * `rotate 4`とある箇所の数字を変更
            * 例: `rotate 52`とすれば１年分(52週間)のログが保存される
* `logwatch`
    * ログ監視ツール
    * ログファイルの中から重要な項目だけをメールにまとめてレポートを送信する
        * 1日に一度のペース

## ログファイルとは

* ログが記録されたファイル
    * ログ: システムやサービスプログラムの挙動、ユーザーのログイン状況の履歴
* ログファイルの多くはテキストファイル
    * lessコマンドなどを使って閲覧可能
* 新しいログはログファイルの末尾に追加される
    
## 保存先

* `/var/log` ディレクトリ
    * ログファイルが保存される

```bash
#ログファイルとサブディレクトリを表示する
ls /var/log
```

![log](./image/log_01.png)

* /var/log/
    * messages
        * システム一般の記録
    * secure
        * 認証関連の記録
    * maillog
        * メール関連の記録
    * cron
        * cronによる自動処理の記録

## 日付で絞り込む

ログテーションされたファイルを確認する

```bash
ls /var/log/*2016*
```

## 末尾を表示

```bash
#CentOSでは、/var/log/messageファイルの閲覧にroot権限が必要
su - 
tail /var/log/messages
```

## ログファイルの見方

```text
日時 ホスト名 出力元:メッセージ
```

* Dec 16 23:21:19」が日時
* centos7がホスト名
* su が出力元
* それ以降がメッセージ

![log2](./image/log_02.png)

### Webサーバーへのアクセスを確認

* WebブラウザーからWebサーバーにアクセスすると、Webサーバーはその記録をログファイルに残す。
* アクセスログ
    * アクセスログには情報が記録される
    * １アクセスが１行で記録される
        * アクセス元のIPアドレス
        * 日時
        * アクセスページ
        * Webブラウザーの種類やバージョン
    * `/var/log/httpd/access_log`
        * Apacheのアクセスログ
        * 閲覧するにはrootユーザーの権限が必要

```bash
su -
less /var/log/httpd/access_log
```

アクセスログの例

* IPが192.168.11.8のコンピューターから
* /test.htmlファイルが
* 16/Nov2015:0:13:00にアクセスされ
* その際のWebブラウザーはMoxilla/5.0(Firefox/31.0)
* OSはLinux x86_64
* アクセスは200で正常に動作した

```text
192.168.11.8 - - [16/Nov/2015:05:13:00 +0900] "GET /test.
html HTTP/1.1" 304 - "-" "Mozilla/5.0 (X11; Linux x86_64;
rv:31.0) Gecko/20100101 Firefox/31.0"
```

主なステータスコードは以下

| ステータースコード | 説明 |
|:----|:----|
| 200(OK) | Webブラウザーからのリクエストは成功 |
| 401(Unauthorized) | ユーザー認証が必要だが失敗した |
| 403(Forbidden) | アクセス権限がない |
| 404(Not Found) | 指定されたファイルが存在しない |
| 500(Internal Server Error) | サーバー内部でエラーが発生した |

* index.htmlにアクセスしようとしたけど
* ファイルが見つからなかった(「404」)
* アドレスの入力間違いの他、何らかの攻撃を試されている可能性あり

```text
192.168.11.8 - - [16/Nov/2015:04:24:19 +0900] "GET /index.
html HTTP/1.1" 404 207 "-" "Mozilla/5.0 (Windows NT 6.3;
WOW64; rv:33.0) Gecko/20100101 Firefox/33.0"
```

* 基本認証に失敗
* ユーザー名「baduser」で
* 「/secret/secret.html」ファイルにアクセスしようとしたけど
* ユーザー名とパスワードの組み合わせが正しくなかったため、
* アクセスする権限が得られなかった

```text
192.168.11.8 - baduser [16/Nov/2014:04:27:55 +0900] "GET /
secret/secret.html HTTP/1.1" 401 381 "-" "Mozilla/5.0
(Windows NT 6.3; WOW64; rv:33.0) Gecko/30100101
Firefox/33.0"
```

## エラーログを確認

* Apacheにはエラーログというログファイルもある
    * エラーの発生したアクセス
    * Apacheの起動や終了の記録
* `/var/log/httpd/error_log`

### Apacheを起動した時のログ

```text
Sun Nov 16 04:37:47.364366 2014] [suexec:notice] [pid
13058] AH01232: suEXEC　mechanism enabled (wrapper: /usr/
sbin/suexec)
[Sun Nov 16 04:37:47.599905 2014] [auth_digest:notice]
[pid 13058] AH01757: generating secret for digest
authendicaition ...
[Sun Nov 16 04:37:47.601489 2014] [Ibmethod_heartbeat:notice] [pid 13058] AH02282: No slotmem from mod_heartmonitor
[Sun Nov 16 04:37:47.605893 2014] [mpm_prefork:notice]
[pid 13058] AH00163: Apache/2.4.6 (CentOS) configured
-- resuming normal operations
[Sun Nov 16 04:37:47.605976 2014] [core:notice] [pid
13058] AH00094: Command line: '/usr/sbin/httpd -D
FOREGROUND'
```

### Apacheを終了した時のログ

```text
[Sun Nov 16 04:37:45.715566 2014] [mpm_prefork:notice]
[pid 12404] AH00170: caught SIGWINCH, shutting down
gracefully
```

### 基本認証に失敗した際のログ

* ユーザー名「baduser」で
* 「/secret/secret.html」ファイルにアクセスしようとしたけど
* baduserというユーザーが見つからなかった

```text
[Sun nov 16 04:24:55.4991933 2014] [auth_basic:error] [pid
12407] [client 192.168.11.8:63038] AH01618: user baduser
not found: /secret/secret.html
```



