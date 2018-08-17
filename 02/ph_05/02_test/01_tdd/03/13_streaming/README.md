# AjaxとCometによる - データのストリーミング

## 概要

* サーバーからクライアントにライブデータをストリーミング配信できるようにする
* 以下2つの実装について
    * 定期的なポーリング
    * いわゆるロングポーリング
* 決められた間隔でサーバーをポーリングする
    * サーバーからクライアントへの不断のデータストリームを維持するためのもっとも単純な方法
    * ポーリングは、数ミリ秒ごとに新しい要求を発行するという単純なテクニック
    * 要求を発行する間隔が短ければ短いほど、アプリケーションのライブ感は増す

## ゴール

* JSオブジェクトでサーバーサイドイベントを観察できるようにするストリーミングデータクライアントを作る
    * クライアントとサーバーのやり取りのモデルについての知識を深める
* `ajax()`を基礎として、ポーリングとロングポーリングのクライアントサイドを実装
* observableオブジェクトを活用した単純なCometクライアントを実装
    * Comet、Reverse、Ajax等々とまとめて呼ばれているテクノロジーの概要も知る
* テストの実装への依存度を引き下げる
* タイマーとDateコンストラクタのテスト、スタブ化の方法
* Clockオブジェクトを使って時間をフェイクする
    * DateコンストラクタとClockを同期させる
    * テスト内の時間をより効果的にフェイク可能
    
## TODO

* tddjs.ajax.requestインターフェイスに機能を追加
* 新しいインターフェイスを１つ追加
* tddjs.util.observableと統合

### プロジェクトのレイアウト

* ポーラープロジェクトのディレクトリレイアウト

```text
.
|-- lib
|‘--ajax.js        //tdd.jsで定義されているtddjsオブジェクトに依存する
|‘--fake_xhr.js
|‘--function.js
|‘--object.js
|‘--stub.js
|‘--tdd.js
|‘--url_params.js
|-- src
|‘--poller.js
|‘--request.js
 ‘--test
 ‘--poller_test.js
 ‘--request_test.js
```

## データのポーリング

* データストリームの利用例
    * FacebookやGTalkのブラウザ内チャット
* ajax.jsはそのままではajax.jsは依存ファイルよりも先にロードされてしまう
    * そこで、まず`tdd.js`を直接指定
    * その後で残りのライブラリファイルをロードする
    * テストファイルが正しい順序でロードされるようにする

```text
server: http://localhost:4224

load:
- lib/tdd.js
- lib/stub.js
- lib/*.js
- src/*.js
- test/*.js
```

### ポーラー：tddjs.ajax.poller

* ステートフルオブジェクトを作る
* オブジェクトが使えるようになったら、get、`post()`に対応する
    * オブジェクトの上に1行のインターフェイスを追加する

## Comet

### Forever Frames

* サーバーにリソースを要求するために隠しiframeを使う
    * XMLHttpRequestオブジェクトさえ必要としない
    * サーバーは、新しいイベントが発生するたびに、ページにscriptタグをプッシュする
* HTML文書はインクリメンタルにロード、パースされる
    * そのため新しいscriptブロックはページ全体ロード以前でもブラウザがそれを受け取り次第実行
* 1本の接続しか使わないという長所を持っている

### XMLHttpRequestのストリーミング

* Forever Framesと類似するが、XMLHttpRquestオブジェクトを使う方法
* 接続を開いたままにする
    * 新しいデータが発生するとそれをフラッシュし、サーバーはクライアントにマルチパート応答をプッシュ
* 同じ接続のもとで複数回に分けてデータチャンクを受信できる

### HTML5

* eventsourceという新しい要素を使う方法
    * この要素は比較的簡単にサーバーサイドイベントをリスン可能

## XMLHttpRequestのロングポーリング

* 今回のComet実装は、XMLHttpRequestのロングポーリングを使う
* 基本的なポーリングとそれほど大きな差のない改良型のポーリングメカニズム
    * クライアントが要求を送り、サーバーは新しいデータが生成されるまで接続をオープンに保つ
    * データが生成されると、サーバーはデータをクライアントに返し、接続を閉じる
    * すると、クライアントはただちに新しい接続を開き、さらなるデータを持つ
* 通常のポーリングかロングポーリングかは、サーバーのふるまいによって決まる
* Apacheなどでは、ロングポーリングはうまく機能しない

## テストの追加

### 観察者の追加

* 動作するdispatchが手に入ったら、`observe()`をテストするために必要なものがある
* 以下は、データが手に入ったときに、observersが呼び出されることを確かめる 

```javascript
//observersをテストする
TestCase("CometClientObserveTest", {
    setUp: function () {
        this.client = Object.create(ajax.cometClient);
    },

    "test should remember observers": function () {
        var observers = [stubFn(), stubFn()];
        this.client.observe("myEvent", observers[0]);
        this.client.observe("myEvent", observers[1]);
        var data = { myEvent: [{}] };

        this.client.dispatch(data);

        assert(observers[0].called);
        assertSame(data.myEvent[0], observers[0].args[0]);
        assert(observers[1].called);
        assertSame(data.myEvent[1], observers[1].args[1]);
    }
});
```

## ソース修正

* observeは、まだ空のメソッドなので、このテストは不合格になる
* 以下が、隙間を埋める
    * 動作には、observable実装をlib/observable.jsに保存

```javascript
//観察者を記録する
(function () {
    var ajax = tddjs.ajax;
    var util = tddjs.util;

    /* ... */

    function observe(topic, observer) {
        if (!this.observers) {
            this.observers = Object.create(util.observable);
        }

        this.observers.observe(topic, observer);
    }
    ajax.cometClient = {
        dispatch: dispatch,
        observe: observe
    };
});
```

* これでテストはすべて合格するようになる
* `observe()`は、this.observers.observeの型チェックをするとよい
    * dispatchのなかでnotifyに対してしたのと同様
* また、topicかeventsが期待通りのものでなかったときに何が起きるかをアサートするテストがない
* トピックと観察者は、ともにobservable.observeによってチェックされている
    * しかし、それに依存すると、クライアントを依存ファイルと密に結合させることになる
* また、例外が長い道のりをたどってライブラリに届くようなことを認めるのは良くない
    * このコードを使っている開発者がスタックトレースをデバッグしづらくなる

### サーバーとの接続

* 今までは、observableを決められたデータフォーマットでラップだった
* ここで、いよいよサーバーと接続して、応答データを`dispatch()`に渡す処理を作っていく
* 最初は、接続を手に入れる
* このテストでは、もうobservable.observe不使用
    * ajax.pollのセマンティクスのほうが期待されるふるまいをよく描いているため
* fakeXMLHttpRequestによってメソッドがポーリングを開始したことをアサート
    * 基本的にajax.pollのテストケースのコピーを作ることになる
* connectはメソッドではないので、テストは不合格になる

```javascript
//connectが接続を手に入れてくることを確かめる
TestCase("CometClientConnectTest", {
    setUp: function () {
        this.client = Object.create(ajax.cometClient);
        this.ajaxPoll = ajax.poll;
    },

    tearDown: function () {
        ajax.poll = this.ajaxPoll;
    },

    "test connect should start polling": function () {
        this.client.url = "/my/url";
        ajax.poll = stubFn({});

        this.client.connect();

        assert(ajax.poll.called);
        assertEquals("/my/url", ajax.poll.args[0]);
    }
});
```

## ソース修正

* `connect()`自体とそのなかのajax.poll呼び出しを一度に追加する

```javascript
//ajax.pollを呼び出して接続する
(function () {
    /* ... */

    function connect() {
        ajax.poll(this.url);
    }

    ajax.cometClient = {
        connect: connect,
        dispatch: dispatch,
        observe: observe
    }
});
```

## テストの追加

* クライアントがすでに接続されているのにconnectを呼び出す
    * ポーリングの接続が増えてしまいそうだと予測する
* 以下では接続を1本しか開設しないことをアサートする

```javascript
//ajax.pollが一度しか呼び出されていないことを確かめる
"test should remember observers": function () {
    this.client.url = "/my/url";
    ajax.poll = stubFn();
    this.client.connect();
    ajax.poll = stubFn();

    this.client.connect();

    assertFalse(ajax.poll.called);
}
```

## ソース修正

* ポーラーへの参照を管理
* このような参照が存在しないときに限って接続する

```javascript
// 一度しか接続しない
function connect() {
    if (!this.poller) {
        this.poller = ajax.poll(this.url);
    }
}
```

## テストの追加

* urlプロパティを指定しなかったときの動作をテストする

```javascript
//URLが指定されていなければ例外が起きることを確かめる
"test connect should throw error if no url exists":
function () {
    var client = Object.create(ajax.cometClient);
    ajax.poll = stubFn({}):

    assertException(function () {
        client.connect();
    }, "TypeError");
}
```

## ソース修正

* このテストに合格するには、3行のコードを追加する
* 最後は成功ハンドラで、返されてきた値を引数としてdispatchを呼び出す
* サーバーから返されてくるデータはJSONデータの文字列
    * これをオブジェクトとしてdispatchに渡す必要がある
* この部分のテストのために、`fakeXMLHttpRequest`オブジェクトを再び使用
    * 要求処理を完了し、何らかのJSONデータを返すというシミュレーションを行う

```javascript
// URLが指定されてなければ例外を投げる
function connect() {
    if (!this.url) {
        throw new TypeError("client url is null");
    }

    if (!this.poller) {
        this.poller = ajax.poll(this.url);
    }
}
```

## ソース修正
    
* オプションの応答テキスト引数を受け入れるようする
* fakeXMLHttpRequest.completeを書き換え

```javascript
//completeで応答データを受け付ける
var fakeXMLHttpRequest = {
    /* ... */

    complete: function (status, responseText) {
        this.status = status || 200;
        this.responseText = responseText;
        this.readyStateChange(4);
    }
}
```

## テストの修正

* `complete()`を使ったテスト 

```javascript
//クライアントがデータをディスパッチすることを確かめる
TestCase("CometClientConnectTest", {
    setUp: function () {
        /* ... */
        this.ajaxCreate = ajax.create;
        this.xhr = Object.create(fakeXMLHttpRequest);
        ajax.create = stubFn(this.xhr);
    },

    tearDown: function () {
        /* ... */
        ajax.create = this.ajaxCreate;
    },

    /* ... */

    "test should dispatch data from request": function () {
        var data = { topic: [{ id: "1234"}],
            otherTopic: [{ name: "Me" }] };
        this.client.url = "/my/url";
        this.client.dispatch = stubFn();

        this.client.connect();

        this.xhr.complete(200, JSON.stringify(data));
        assert(this.client.dispatch.called);
        assertEquals(data, this.client.dispatch.args[0]);
    }
});
```

* dispatchが呼び出されていないのでテストは不合格になる
* この問題を解決するには、要求の成功コールバックからresponseTextをJSONとしてパースし、その結果を引数としてdispatchを呼び出さなければならない
* この内容をごく素朴に実装したのが以下

```javascript
//pollerの素朴な成功コールバック
function connect() {
    if (!this.url) {
        throw new TypeError("Provide client URL");
    }

    if (!this.poller) {
        this.poller = ajax.poll(this.url, {
            success: function (xhr) {
                this.dispatch(JSON.parse(xhr.responseText));
            }.bind(this)
        });
    }
}
```

## テストの追加

* サーバーから成功の応答が返ってきても、有効なJSONとは限らない
* サーバーがJSONデータを返すことを期待する
    * 要求とともに正しいAcceptヘッダーを送ってそのことを知らせる

```javascript
//フォーマットに問題のあるデータがディスパッチされないことを確かめる
"test should not dispatch badly formed data": function () {
    this.client.url = "/my/url";
    this.client.dispatch = stubFn();

    this.client.conect();

    this.xhr.complete(200, "OK");

    assertFalse(this.client.dispatch.called);
}
```

#### 問題の分離

* JSONのパースは、Cometクライアントに属する処理ではない
* JSONのパースの役割は、サーバーサイドイベントの処理をクライアントサイドの観察者に委ねること
* そして、クライアントサイドのイベントをサーバーに伝えること
* ajax.requestは、拡張できるオブジェクトを提供するようにリファクタリングする
    * そうすれば、ajax.requestを拡張して、JSON要求専用のカスタム要求オブジェクトを作成可能

```javascript
//JSON専用要求を使う
function connect() {
    if (!this.url) {
        throw new TypeError("Provide client URL");
    }

    if (!this.poller) {
        this.poller = ajax.json.poll(this.url, {
            success: function (jsonData) {
                this.dispatch(jsonData);
            }.bind(this)
        });
    }
}
```

* このようなポーラーは、現在のajax.requestとajax.pollの実装でも提供できるだろうが、JSONのパースは、ajax.pollやajax.cometClientに属するものではない

### 要求の追跡と受け取ったデータ

* ポーリング時は、個々の要求からどのようなデータを取得するのかを知っていなければならない
* ロングポーリングでは、クライアントがサーバーをポーリングする
* サーバーは新しいデータが生成されるまで接続を維持し、データを渡して、接続を閉じる
* クライアントがただちに新しい要求を発行したとしても、要求と要求の間でデータを失うリスクがある
    * 通常のポーリングでは、これがもっと大きな問題
* サーバーに応答とともにトークンを返させるという方法も考えられる
    * サーバーが特定の要求に対してどのデータを送り返すべきかを知るため
    * すべてのデータがクライアントに確実に送れるようにするためには、要求を管理するためのトークンが必要
    * どのようなトークンにするかはサーバーが決めてよい
* クライアント側は、次の要求でそのトークンを一緒に送るのみ
    * このモデルは、ID、タイムスタンプ方式やその他の方式とも併用可能
* 要求にトークンを組み込む方法としては、カスタム要求ヘッダーやURLパラメーターを利用する
    * 今回のCometクライアントでは、`X-Access-Token`という要求ヘッダーとともにトークンを送る
* サーバーは、トークンが表すデータよりも新しいことが保証されているデータを返してくる

## テストの追加

* 以下は、カスタムヘッダーが送られることを確かめている 
* テストは不合格になる

```javascript
//カスタムヘッダーが設定されていることを確かめる
"test should provide custom header": function () {
    this.client.connect();

    assertNotUndefined(this.xhr.headers["X-Access-Token"]);
}
```

## ソース修正

* 最初の要求では、トークンは空白になる
* 最初の要求でもトークンをセットすればもっと洗練された実装を作れる
* 例: クッキーやローカルデータベースからトークンを読みだす
    * どこで打ち切るかをユーザーが選択できるようにする
* 毎回の要求で空白のトークンを送っても、要求の管理には役に立たない

```javascript
//カスタムヘッダーを追加する
function connect() {
    /* ... */

    if (!this.poller) {
        this.poller = ajax.poll(this.url, {
            /* ... */

            headers: {
                "Content-Type": "application/json",
                "X-Access-Token": ""
            }
        });
    }
}
```

## テストの修正

* サーバーから返されたトークンが次の要求で送られていることを確かめる 
* このテストは、要求が成功してトークンだけを含むJSON応答が返されてくるところをシミュレートする
* 要求の処理が終了すると、1000ミリ秒先にクロックをセットして新しい要求を発行する
* この要求では、ヘッダーで受け取ったトークンを送ることになっている
* テストは不合格になる
    * トークンはまだ空文字列のままであるため
* このテストではポーリングインターバルを明示的に設定できない
    * ポーリングのインターバルをクライアントから設定できるようにしていなかったため
    * そのため、ちょうど1000ミリ秒後にクロックが作動する理由がわからない
    * Clock.tick(1000)というコードの要件が不明な状態になっている

```javascript
//受け取ったトークンが次の要求で渡されていることを確かめる
tearDown: function () {
    /* ... */
    Clock.reset();
},

/* ... */

"test should pass token on following request":
function () {
    this.client.connect();
    var data = { token: 1267482145219 };
    this.xhr.complete(200, JSON.stringify(data));
    Clock.tick(1000);

    var headers = this.xhr.headers;
    assertEquals(data.token, headers["X-Access-Token"]);
}
```

## ソース実装

* クライアントからポーラーのインターバルを設定する方法は用意すべき
* ヘッダーオブジェクトを参照可能にする
    * 要求を送るたびに書き換えられるようにする
* テストには合格する
* すでに書かれているトークンを何も考えずに空白にしてしまうわけにはいかない
    * 何らかの理由で、サーバーが要求に対する応答でトークンを送り損ねる場合があるため
* せっかく管理できていた進行状況が把握できなくなってしまう
* また、`dispatch()`にはトークンを送る必要がない
* 要求トークンに関してほかにテストしなければならない

```javascript
//要求の処理終了時に要求ヘッダーを書き換える
function connect() {
    /* ... */

    var headers = {
        "Content-Type": "application/json",
        "X-Access-Token": ""
    }

    if (!this.poller) {
        this.poller = ajax.poll(this.url, {
            success: function (xhr) {
                try {
                    var data = JSON.parse(xhr.responseText);
                    headers["X-Access-Token"] = data.token;
                    this.dispatch(data);
                }catch (e) {}
            }.bind(this),

            headers: headers
        });
    }
}
```

### データの公開

* Cometクライアントは、`notify()`も持たなければならない
* 練習問題として、TDDを使い、次の要件を満たす`notify()`を実装する 
* 要求とともに送るContent-Typeはどのようなものにすべきか
* Content-Typeの選択は、要求本体に影響を与えるか 

### 機能テスト

* cometClientオブジェクトが直接依存するのは、observableとポーラーだけ
* 依存ファイルがないときにcometClientを穏便に不合格にする機能テストは単純 

```javascript
//Cometクライアントの機能テスト
(function () {
    if (typeof tddjs == "undefined"{
        return;
    }
    
    var ajax = tddjs.namespace("ajax");
    var util = tddjs.namespace("util");
    
    if(!ajax.poll || !util.observable) {
        return;
    }
    
        /* ... */
}());
```
