# Node.js

* Nodeはイベントループを使用している
* ApacheHTTPなどのWebサーバーは、並行実行に難があり
    * そのためスケーラビリティに支障が出る
    * 1本の接続に1つのスレッドを割り当てるため
* Nodeは、要求を受け付けると、データの取得などのイベントのリスンを開始
    * スリープに入る
* データの準備ができると、イベントがNodeに通知を送り、接続を終了する
* 以上がNodeのイベントループによってシームレスに処理される

### 環境のセットアップ

* 別ページ参照

#### ディレクトリ構造

```text
.
|--deps     // サードパーティの依存ファイルのためのディレクトリ
|--lib
|  '--chapp //今回のプロジェクト名
'--test
   '--chapp
```


#### サーバー

* NodeでHTTPサーバーを作る
    * `httpモジュール`とその`createServer()`が必要
    * 要求`リスナー`としてアタッチされる関数を受け付ける
    * lib/chapp/server.js

```javascript
//Node.jsによるHTTPサーバー
var http = require("http");
var url = require("url");
var crController = require("chapp/chat_room_controller");

module.exports = http.createServer(function (reg, res) {
    if(url.parse(req.url).patjname == "/comet") {
        var controller = crController.create(req, res);
        controller[req.method.toLowerCase()]();
    }
});
```

* サーバーは、モジュールとしてchatRoomControllerを必要とする
    * このモジュールは要求/応答ロジックを処理する
    * 現在のところ、サーバーは/cometというURLへの要求だけに応答する 

#### 起動スクリプト

* サーバーを起動するには、サーバーを起動するスクリプトが必要
    * ロードパスをセットアップし、サーバーファイルをrequireするため
* 以下は起動スクリプトで、`./run_server`に格納する
    * chmod +x run_serverで実行可能にしておく 

```bash
#!/usr/local/bin/node

require.paths.push(__dirname);
require.paths.push(__dirname + "/deps");
require.paths.push(__dirname + "/lib");

require("chapp/server").listen(procss.argv[2] || 8000);
```

* listen呼び出しがサーバーを起動する
* `process.argv`には以下が含まれている
    * 全てのCLI引数
    * インタープリタ
    * 実行されるファイル
    * スクリプト実行時に与えられるその他の引数
* スクリプトは、./run_server 8080で実行される
* ポート番号を省略してサーバーを起動すると、デフォルトで8000番ポートを使う 

## コントローラ

* /cometというURLへの要求に対して、コントローラの`create()`を呼び出す
* 使ったHTTPメソッドに対応するコントローラメソッドを呼び出す
    * ここでは、`get()`、`post()`しか実装しない

### CommonJSモジュール

* Nodeは`CommonJS`モジュールを実装している
    * CommonJSモジュール: 再利用可能なJSコンポーネントの構造化された管理方法
    * CommonJSモジュール内の暗黙のスコープはグローバルスコープではない
    * ブラウザにロードされるスクリプトファイルとは異なる
    * そのため、識別子のリークを防ぐための無名クロージャでラップす不要
    
### モジュールに関数やオブジェクトを追加する

* 特別なexportsオブジェクトにプロパティを追加する
* あるいは、モジュール全体を1個のオブジェクトとして指定
* `module.exports = myModule`のように代入する

### モジュールのロード

* モジュールはrequire("my_module")でロードする
    * この関数は、require.paths配列で指定されたパスを使う
* 配列の内容は、必要に応じて変更可能
* ロードパスにないモジュールもロード可能
    * その他場合はモジュール名の先頭に"./"というプレフィックスをつける
    * プレフィックスをつけると、Nodeはカレントモジュールファイルの相対パスからモジュールを探す 

## プロミス

### 非同期インターフェイスの操作

* プロミスを使う非同期メソッドは、コールバックを受け付けない
    * プロミス、すなわち`呼び出しの最終的な結果`を表現するオブジェクトを返す
    * 返されるオブジェクトは観察対象オブジェクト
        * 呼び出し元は成功、失敗のイベントを登録可能
* プロミスを作った最初の呼び出しは、処理を終了時にプロミスの`resolve()`を呼び出す
    * すると、成功コールバックが実行される
    * 同様に、呼び出しが失敗時、プロミスの`reject()`が呼び出される
        * このメソッドには例外を渡せる
* プロミスを使えば、コールバックをネストさせる必要がなくなる
