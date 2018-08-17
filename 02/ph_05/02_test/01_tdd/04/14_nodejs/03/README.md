# POST要求のメッセージの処理

* postアクションは、cometClientが送ってくる形式のJSONを受け付け、メッセージを作る
    * メッセージを作成するためのJSON要求

```json
{
  "topic": "message",
    "data": {
        "user": "cjno",
        "message": "Listening to the new 1349 album"
    }
}
```

* 外側の`topic`プロパティは、どのようなタイプのイベントを作るかを説明する
    * この場合は、新しいメッセージ
* 外側の`data`プロパティは、実際のデータを保持している
* クライアントは、同じサーバーリソースに異なるタイプのクライアントサイドイベントをポスト可能
    * 例: 誰かがチャットに参加してきたとき、クライアントはJSONを送ってくる

## チャットルームに参加するためのJSON要求

* 複数のチャットルームをサポートするようにバックエンドを拡張する
* その場合、メッセージにはユーザーがどの部屋に入ったかについての情報も含まれるようになる

```json
{ 
  "topic": "userEnter",
  "data": {
    "user": "cjno"
  }
}
```

## 要求本体の読み出し

* post処理でまず要求本体を取り出さなければならない
    * ここにはURLエンコードのJSON文字列が含まれている
    
### 処理

* 要求が届く
* `request`オブジェクトは要求本体のチャンクを引数として`data`イベントを生成する
* すべてのチャンクが届く
* `request`オブジェクトは`end`イベントを生成する

### 備考

* `events.EventEmitterインターフェイス`
    * Observerパターンのobservableに当たるNodeイベントの駆動力
* テストでは、requestオブジェクトとしてスタブを使う
    * `request`のスタブは`EventEmitter`でなければならない
        * テストしたい`data`、`end`イベントを生成するため
    * そうすれば、テストからチャンクをいくつか生成可能になる
    * その結果、`JSON.parse`に結合された文字列が渡されていることをアサート可能になる
* 要求本体全体がJSON.parseに渡されていることを確かめる
    * スタブ関数を使ってJSON.parseをスタブ化する

```bash
touch deps/stub.js
```

```javascript
//NodeとstubFnを併用する
module.exports = function (returnValue) {
    function stub() {
        stub.called = true;
        stub.args = arguments;
        stub.thisArg = this;
        return returnValue;
    }

    stub.called = false;

    return stub;
};
```

## テストの作成

* セットアップコードはすぐ後で移動する 
* `setUp`と`tearDown`
    * テストがスタブ化した`JSON.parse`の`復元`のための処理を行っている
* 次に、フェイクの`request`、`response`オブジェクトを引数としてcontrollerオブジェクトを作る
* POSTのテストデータを作る
* テストデータをそれに合わせてエンコードしなければならない
    * tddjs.ajaxツールは、現在`URLエンコードされたデータ`しかサポートしていないため
* 次にURLエンコードされたJSON文字列を2つのチャンクに分けて生成する
    * `end`イベントを生成
    * 最後に`JSON.parse()`が呼び出されたことを確かめる

```javascript
//要求本体がJSONとしてパースされることを確かめる
module.exports = chatRoom;

var EventEmitter = require("events").EventEmitter;
var stub = require("stub");

/* ... */

testCase(exports, "chatRoomController.post", {
    setUp: function () {
        this.jsonParse = JSON.parse;
    }

    tearDown: function () {
        JSON.parse = this.jsonParse;
    },

    "should parse request body as JSON": function (test) {
        var req = new EventEmitter();
        var controller = chatRoomController.create(req, {});
        var data = { data: { user: "cjno", message: "hi" } };
        var stringData = JSON.stringify(data);
        var str = encodeURI(stringData);

        JSON.parse = stub(data);
        controller.post();
        req.emit("data", str.substring(0, str.length / 2));
        req.emit("data", str.substring(str.length / 2));
        req.emit("end");

        test.equals(JSON.parse.args[0], stringData);
        test.done();
    }
});
```

### ソース修正

* テストに合格するコード

```javascript
//要求本体を読み、JSONとしてパースする
var chatRoomController = {
    /* ... */

    post: function () {
        var body = "";

        this.request.addListener("data", function (chunk) {
            body += chunk;
        });

        this.request.addListner("end", function () {
            JSON.parse(decodeURI(body));
        });
    }
};
```

### リファクタリング

* テストに合格したら、重複を取り除く
* 重複を積極的に取り除くことがきわめて重要
    * 書き換えやすく、適していると思う形に変形しやすい柔軟なコードベースを作るため
* テストはコードベースの一部
    * テスト自体もコンスタントにリファクタリングと改良を必要とする
* `create`と`post`
    * 両方ともスタブの要求、応答オブジェクトを使ってコントローラインスタンスを作っている
    * getのテストケースも同じことをする
* この部分を抽出し、共有セットアップメソッドとして使える関数を作る
* この変更を加えた後
    * テストは`controller`、`req`、`res`をthisのプロパティとして参照しなければならない

```javascript
//セットアップを共有する
function controllerSetUp() {
    var req = this.req = new EventEmitter();
    var res = this.res ={};
    this.controller = chatRoomController.create(req, res);
    this.jsonParse = JSON.parse;
}

function controllerTearDown() {
    JSON.parse = this.jsonParse;
}

/* ... */
testCase(exports, "chatRoomController.create", {
    setUp: controllerSetUp,
    /* ... */
});

testCase(exports, "chatRoomController.post", {
    setUp: controllerSetUp,
    tearDown: controllerTearDown,
    /* ... */
});
```

## メッセージを抜き出す

* 要求本体はJSONとしてパース可能になったら、得られたオブジェクトからメッセージを抽出する
    * 安全に管理可能な場所に渡すため
* ここまでトップダウンで作っているため、まだデータモデルを考えていない
* そこで、どのような感じになるのかを大ざっぱに決める
* `post()`処理を完成させるまでスタブを使う
* メッセージはチャットルームに属する
* コントローラは、サーバーにchatRoomオブジェクトを割り当ててもらわなければならない
    * チャットルームは要求をまたがって残っていなければならないため
* `chatRoom`オブジェクトからは、`addMessage(user, message)`を呼び出せる

## テストの追加

* `post`がこのインターフェイスによって`addMessage`にデータを渡していることを確かめる

```javascript
//postがメッセージを追加していることを確かめる
"should add message from request body": function (test) {
    var data = { data: { user: "cjno", message: "hi" } };

    this.controller.chatRoom = { addMessage: stub() };
    this.controller.post();
    this.req.emit("data", encodeURI(JSON.stringify(data)));
    this.req.emit("end");

    test.ok(this.controller.chatRoom.addMessage.called);
    var args = this.controller.chatRoom.addMessage.args;
    test.equals(args[0], data.data.user);
    test.equals(args[1], data.data.message);
    test.done();
}
```

* 要求本体リスナーを追加させるために`post()`を呼び出す
* 次にニセの要求データを生成する
* 最後に、コントローラが正しい引数を指定する
    * chatRoom.addMessageを呼び出していることを確かめる

## 合格するよう修正する

* 無名の`end`イベントハンドラの中で`chatRoom.addMessage`にアクセスする
    * バインドを使えば、thisへのローカル参照を手作業で管理せずにこれを実現可能
* しかし、これではまだ完全に動作するとは言えない
* 同じくpostを呼び出す前のテストが、chatRoomのaddMessageを呼び出そうとする
    * しかし、`chatRoom`はそのテストでは`undefined`

```bash
touch deps/function-bind.js
```

```javascript
//POST要求時にメッセージを追加する
require("function-bind");

var chatRoomController = {
    /* ... */

    post: function () {
        /* ... */

        this.request.addListener("end", function () {
            var data = JSON.parse(decodeURI(body)).data;
            this.chatRoom.addMessage(data.user, data.message);
        },bind(this));
    }
};
```

### Undefinedの解決

* `chatRoom`スタブを`setUp`に移動すれば解決しテストが緑になる

```javascript
//chatRoomスタブを共有する
function controllerSetup() {
    /* ...*/

    this.controller.chatRoom = { addMessage: stub() };
}
```

## リファクタリング

* 第2のテストで導入してしまったロジックの重複に注意を向ける
* 特に、両方のテストが本体つきの要求を送るところをシミュレートしている
* このロジックをセットアップに抽出すれば、テストを大幅に簡略化可能
* `sendRequest()`により、要求を発行する新しいテストも簡単に書けるようになった

```javascript
//postテストをクリーンにする
function controllerSetUp() {
    /* ... */

    this.sendRequest = function (data) {
        var str = encodeURI(JSON.stringify(data));
        this.req.emit("data", str.substring(0, str.length /2));
        this.req.emit("data", str.substring(str.length /2));
        this.req.emit("end");
    };
}

testCase(exports, "chatRoomController.post",{
    /* ... */

    "should parse request body as JSON": function (test) {
        var data = { data: {user: "cjno", message: "hi"}
    };
    JSON.parse = stub(data);

    this.controller.post();
    this.sendRequest(data);
    
    test.equals(JSON.parse.args[0], JSON.stringify(data));
    test.done();
},

/* ... */
});
```

## 悪意のあるデータ

* 今のコードは、まったくフィルタリングされていないメッセージを受け付けていることに注意
* 例: 以下は悪意のある要求

```json
{ 
  "topic": "message",
  "data" : {
    "user": "cjno",
    "message":
    "<script>window.location = 'http://hacked';</script>"
  }
}
```
