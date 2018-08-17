# Node.jsによる - サーバーサイドJavaScript

## 概要

* テスト駆動開発により、Nodeを使った小さなサーバーサイドアプリケーションを開発する
    * Nodeとそのルールを学ぶ
    * ブラウザよりも予測可能性の高い環境でJavaScript開発を実践
    * ブラウザ内で動作するチャットアプリケーションのバックエンドを作る
* [準備](00)
* [モジュールを定義する](01)
* [コントローラを作る](02)
* [POST要求のメッセージの処理](03)
* [要求に応答する](04)
* [動作確認](05)

## ドメインモデルとストレージ

* チャットアプリケーションのドメインモデル
    * 1個のchatRoomオブジェクトから構成する
* chatRoomは、単純にメモリ内にメッセージを格納

### チャットルームを作る

* chatRoomを継承する新しいオブジェクトは、Object.createで作る
    * コントローラのときと同様
* しかし、オブジェクトは`Object.create`で直接作る
    * さしあたりchatRoomは初期化ルーチンを必要としないため
* 後で初期化ルーチンを追加する際、テスト内のチャットルームオブジェクト作成部分の更新が必要
* これは、呼び出しの重複を避けようと思うよいきっかけになる
* [メッセージを追加する](06)
* [メッセージをフェッチする](07)
* [プロミスを使用する](08)
* [イベントエミッタ](09)

## 再びコントローラの開発へ

* 動作するデータレイヤーが準備できたので、コントローラの仕上げに戻る
* postの仕上げに取りかかるとともに、getの実装もする 

### post()を仕上げる

* 現在の`post()`
    * メッセージが追加されたかに関わらず、ステータスコード201に応答する
    * しかし、これは201への応答のセマンティクスに違反している
* HTTP仕様の規定は以下
    * オリジナルサーバーは、ステータスコード201を返す前にリソースを作らなければならない

## テストの修正

* postがwriteHeadを呼び出すことを確かめているテストは更新が必要
* 今度は、`addMessage()`が解決したらヘッダーが書き込まれることを確かめる

```javascript
//addMessageが解決した直後にpostが応答することを確かめる
/* ... */
var Promise = require("node-promise/promise").Promise;
/* ... */

function controllerSetUp() {
    /* ... */
    var promise = this.addMessagePromise = new Promise();
    this.controller.chatRoom = { addMessage: stub(promise) };
    /* ... */
}

/* ... */

testCase(exports, "chatRoomController.post", {
    /* ... */

    "should write status header when addMessage resolves":
        function (test) {
            var data = { data: { user: "cjno", message: "hi" } };

            this.controller.post();
            this.sendRequest(data);
            this.addMessagePromise.resolve({});

            process.nextTick(function () {
                test.ok(this.res.writeHead.called);
                test.equals(this.res.writeHead.args[0], 201);
                test.done();
            }.bind(this));
        },

    /* ... */
});
```

* テストにまだ合格するなら、新しいセットアップコードは一切壊れていない
    * チェックを遅らせてもテストにあまり影響を及ぼさないため
* 接続がクローズされることを確かめる次のテストも同様に更新可能
* 以下は、更新後のテスト

```javascript
//addMessageが解決した直後に接続がクローズされることを確かめる
"should close connection when addMessage resolves":
function (test) {
    var data = { data: { user: "cjno", message: "hi" } };
    this.controller.post();
    this.sendRequest(data);
    this.addMessagePromise.resolve({});

    process.nextTick(function () {
        test.ok(this.res.end.called);
        test.done();
    }.bind(this));
}
```

## テストの追加

* 今までの2つのテストと書き方が異なる新しいテスト
* addMessageが解決されるまでpostが応答しないことを確かめている
* このテストは、今までの2つほどスムースには動作しない

```javascript
//postがただちには応答しないことを確かめる
"should not respond immediately": function (test) {
    this.controller.post();
    this.sendRequest({ data: {} });

    test.ok(this.res.end.called);
    test.done();
}
```

## ソース修正

* addMessageが返したプロミスが解決されるまで、クローズ呼び出しを遅らせる
    * `post()`がどのような形でもエラーを処理していないことに注意

```javascript
//postはaddMessageが解決したときに応答する
post: function () {
    /* ... */

    this.request.addListener("end", function () {
        var data = JSON.parse(decodeURI(body)).data;

        this.chatRoom.addMessage(
            data.user, data.message
        ).then(function () {
            this.response.writeHead(201);
            this.response.end();
        }.bind(this));
    }.bind(this));
}
``` 

### GETによるメッセージのストリーミング

* GET要求の処理
    * すぐにメッセージを返してくるか
    * メッセージが返せる状態になるまで接続をオープンにしておくか
* コントローラの`get()`は、単純に要求とデータを結び付けるだけ
* chatRoom.waitForMessagesSinceを実践する過程で大半は処理済み

#### アクセストークンによるメッセージのフィルタリング

* `cometClient`が取得したいデータは何かをどのようにしてサーバーに知らせていたかを思い出す
* 任意の値を格納でき、サーバーがコントロールできる`X-Access-Token`ヘッダーを使用していた
* 進行状況の監視にも当然IDを使用する
    * waitForMessagesSinceはIDを使うように作ったため
* クライアントは、初めて接続したときに空のX-Access-Tokenを送ることになる
* その条件を処理するところから始める
* 以下は、最初のGET要求をテストする
* 空のアクセストークンを送ったときには0以降のすべてのメッセージを持つ
    * 最初のGET要求には返せるすべてのメッセージが返されることを確かめる

```javascript
//クライアントがすべてのメッセージを取りだしてくることを確かめる
testCase(exports, "chatRoomController.get",{
    setUp: controllerSetUp,
    tearDown: controllerTearDown,

    "should wait for any message":function (test) {
        this.req.headers = { "x-access-token": "" };
        var chatRoom = this.controller.chatRoom;
        chatRoom.waitForMessagesSince = stub();

        this.controller.get();

        test.ok(chatRoom.waitForMessagesSince.called);
        test.equals(chatRoom.waitForMessagesSince.args[0], 0);
        test.done();
    }
});
```

* Nodeが**ヘッダーを小文字**にして使っていることに注意
* これに気付かないと、貴重な時間がムダになる

## ソース修正

* メソッドに直接期待されるIDを渡してずるをする
* これでテストには合格する

```javascript
//ずるをしてテストに合格する
var chatRoomController = {
    /* ... */

    get: function () {
        this.chatRoom.waitForMessagesSince(0);
    }
};
```

## テストの追加

* アクセストークンが設定されているはずの二度目以降の要求に進む
* 実際の値でアクセストークンをスタブ化
* それがwaitForMessagesSinceに渡されることを確かめる
* 渡されたIDが`X-Access-Token`ヘッダーで与えられたものと同じだということを確かめている

```javascript
//getがアクセストークンを渡すことを確かめる
"should wait for messages since X-Access-Token":
function (test) {
    this.req.headers = { "x-access-token": "2" };
    var chatRoom = this.controller.chatRoom;
    chatRoom.waitForMessagesSince = stub();

    this.controller.get();

    test.ok(chatRoom.waitForMessagesSince.called);
    test.equals(chatRoom.waitForMessagesSince.args[0], 2);
    test.done();
}
```

## ソース修正

```javascript
//アクセストークンヘッダーを渡す
get: function () {
    var id = this.request.headers["x-access-token"] || 0;
    this.chatRoom.waitForMessagesSince(id);
}
```
#### respond()

* `get()`
    * 応答本体とともに、ステータスコード、おそらくは何らかの応答ヘッダーを送る
        * 応答本体は何らかの形のJSON応答でなければならない
    * 最後に接続をクローズする
* これは、`post()`が現在行っていることと類似
* そこで、応答部分を新しいメソッドに分割して、getとpostで共有可能にする
* 以下は、postのテストケースからコピーした2つのテストケースを示している

```javascript
//respondのための最初のテスト
testCase(exports, "chatRoomController.respond", {
    setUp: controllerSetUp,
    "should write status code": function (test) {
        this.controller.respond(201);
        test.ok(this.res.writeHead.called);
        test.equals(this.res.writeHead.args[0],201);
        test.done();
    }

    "should close connection": function (test) {
        this.sontroller.respond(201);

        test.ok(this.res.end.called);
        test.done();
    }
});
```

## ソース修正

* `post()`に追加した2行を新しい`respond()`にコピーすれば合格する
* `post()`は、このメソッドを呼び出すことで単純化できる
* また、これにより、ステータスコードと接続クローズの2つのテストを1つに共通化可能
* respondをスタブ化して、respondが呼び出されたことを確かめればよい

```javascript
//専用respond()
var chatRoomController = {
    /* ... */
    respond: function (status) {
        this.response.writeHead(status);
        this.response.end();
    }
};
```

## テストの追加

#### メッセージを整形する

* `get()`の次の仕事は、メッセージの整形
* ここでも、データフォーマットを定義している`cometClient`に頼る必要がある
    * このメソッドは、JSONオブジェクトを応答してくる
        * このJSONオブジェクトは名前がトピック、値がオブジェクト配列というプロパティを表す
    * また、このJSONオブジェクトには、tokenプロパティが含まれている
* 応答本体にはJSON文字列を書き込まなければならない
* respondをスタブ化すれば、これをテストにすることができる
* 今度は、オブジェクトが第2引数として渡されていることを確かめる
    * そのため、あとでrespondに手を入れる
    * そして、第2引数にJSON文字列の応答本体を書き込ませなければならない
* 少し消化しやすくするために、`seyUp()`を補った
* 今までのテストはすべて`waitForMessagesSince`をスタブ化し、ヘッダーを設定しておく必要があった
* これらを抽出すれば、問題のテストが何を実現しようしているのかがわかりやすくなる
* このテストの要件
    * waitForMessagesSinceが返してきたプロミスを解決
    * そのデータがcometClientフレンドリなオブジェクトにラップされる
    * ステータスコード200とともに`resolve()`に渡されていることを確かめる

```javascript
//respondにオブジェクトが渡されることを確かめる
function controllerSetUp() {
    var req = this.req = new EventEmitter();
    req.headers = { "x-access-token": "" };

    /* ... */

    var add = this.addMessagePromise = new Promise();
    var wait = this.waitForMessagesPromise = new Promise();

    this.controller.chatRoom = {
        addMessage: stub(add),
        waitFofMessagesSince: stub(wait)
    };

    /* ... */
}

/* ... */

testCase(exports, "chatRoomController.respond", {
    /* ... */

    "should respond with formatted data": function (test) {
        this.controller.respond = stub();
        varmessages = [{ user: "cjno", message: "hi" }];
        this.waitForMessagesPromise.resolve(message);

        this.controller.get();

        process.nextTick(function () {
            test.ok(this.controller.respond.called);
            var args = this.controller.respond.args;
            test.same(args[0], 201);
            test.same(args[1].message, messages);
            test.done();
        }.bind(this));
    }
});
```

## ソース修正

```javascript
//getから応答する
get: function () {
    var id = this.request.headers["x-access-token"] || 0;
    var wait = this.chatRoom.waitForMessagesSince(id);

    wait.then(function (msgs) {
        this.respond(200, { message: msgs });
    }.bind(this));
}
```

## テストのつか

#### トークンを更新する

* `get()`は、応答のなかにメッセージとともにトークンを埋め込まなければならない
* トークンはcometClientによって自動的に選ばれる
* その後の要求の`X-Access-Token`ヘッダーで送られる
* 以下は、メッセージとともにトークンが渡されていることを確かめる

```javascript
//応答にトークンが埋め込まれていることを確かめる
"should include token in response": function (test) {
    this.controller.respond = stub();
    this.waitForMessagesPromise.resolve([{id:24}, {id:25}]);

    this.controller.get();

    process.nextTick(function () {
        test.same(this.controller.respond.args[1].oken, 25);
        test.done();
    }.bind(this));
}
```

## ソース修正

* 最後のメッセージIDをトークンとして渡す

```javascript
//トークンを読み込む
get: function () {
    /* ... */

    wait.then(function (messages) {
        this.respond(200, {
            message: messages,
            token: messages[messages.length -1].id
        });
    }.bind(this));
}
```

### 応答ヘッダーと本体

* 最後まで残ったのは、応答データをJSONにエンコードし、応答本体を書くこと
* 以下は、`respond()`のコード例 
* これで完成

```javascript
//respond()
respond: function (status, data) {
    var strData = JSON.stringify(data) || "{}";

    this.response.writeHead(status, {
        "Content-Type": "application/json",
        "Content-Length": strData.length
    });

    this.response.write(strData);
    this.response.end();
}
```

## 動作確認

* 動作確認には新しいCLIセッションを開始する

```bash
#完成したアプリケーションをCLIから手作業でテストする
node-repl
```

```text
node> var msg = { user:"cjno", message:"Enjoying Node.js" };
node> var data = { topic:"message", data: msg };
node> var encoded = encodeURI(JSON.stringify(data));
node> var require("fs").writeFileSync("chapp.txt",encoded);
node> Ctrl-d
```

```bash
curl -d 'cat chapp.txt' http://localhost:8000/comet
curl http://localhost:8000/comet
```

```text
{"message":[{"id":1,"user":"cjno",\
"message":"Enjoying Node.js"}],"token":1}
```
