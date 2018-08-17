# Node.jsとともにクライアントを使う

* 3つのクライアントコンポーネントのなかの1つが完成した
* Nodeアプリケーションのchappに配管的なコードを追加
* クライアントにサービスを提供させてみる
* HTTPサーバーモジュールを通じて静的ファイルを提供する概念を持っていない
    * Nodeは低水準のランタイムであるため
* 静的ファイルを提供するには、ファイルをクライアントにストリーミングしなければならない
    * 要求のURLとディスク上のファイルを突き合わせる

## ソース実装

* Felix Geisendörferのnode-paperboyというモジュールを使う
* このモジュールをchappのdepsディレクトリに追加する
* `chappのlib/server.js`に格納されたモジュールをロードする
    * サーバーは、publicディレクトリのファイルを提供するようにセットアップされている
    * 例: http://localhost:8000/index.htmlは、public/index.htmlを返そうとする 

```javascript
//chappのサーバーに静的ファイルサービス機能を追加する
/* ... */
var paperboy = require("node-paperboy");

module.exports = http.createServer(function (req,res) {
    if (url.parse(req.url).pathname == "/comet") {
        /* ... */
    } else {
        var delivery = paperbos.deliver("public", req, res);

        delivery.otherwise(function () {
            res.writeHead(404, { "Content-Type": "text/html" });
            res.write("<h1>Nothing to see here, move along</h1>");
            res.close();
        });
    }
});
```

* publicディレクトリに要求されたURLに対応するファイルが見つからない場合
    * otherwiseコールバックが呼び出される
* その場合は、簡単な404ページを返す
* チャットクライアントにサービスを提供する

```bash
mkdir public/js
cp tdd.js public/js/
cp observable.js public/js/
cp function.js public/js/
cp object.js public/js/
cp user_form_controller.js public/js/
```

* HTMLを作成
    * [public/index.html](public/index.html)
* 単純なスタイルシート作成
    * [public/css/chapp.css](public/css/chapp.css)
* 以下のブートストラップスクリプト作成
    * [public/js/chat_client.js](public/js/chat_client.js)
* ここでサーバーを起動して、ブラウザでhttp://localhost:8000/にアクセス
* 素っ気ないフォームが表示される
* サブミットすると、ブラウザはあいさつを表示して、フォームを隠してしまう

