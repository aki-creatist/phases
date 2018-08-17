# Cometクライアント

* サーバーに対するプロキシとして機能するクライアントを作る
* サーバーからデータが届くたびに、クライアントはメッセージをトピックごとに分類
* 関連する観察者に通知を送る
    * こうすれば、接続を1本に制限しつつ、様々なトピックのメッセージを受信可能
* このクライアントは、observable（観察対象）オブジェクトを使って観察者を処理する

### メッセージ形式

* クライアントサイドオブジェクトは単一のトピックを観察
    * observableオブジェクトと同様
* 新しいデータが届くたびに引数として1個のオブジェクトを指定した形で呼び出す
    * サーバーからJSONデータを送る手法をとる
* 個々の応答は、プロパティ名がトピック、値がトピックに関連したデータの配列になっているオブジェクトを送り返す

## JSON形式の応答

* 以下はサーバーから送られてくる典型的なJSON形式の応答のサンプル
* 以下の`chatMessage`トピックの観察者は合計2回呼び出される
    * 1つのチャットメッセージにつき1回ずつ

```json
{
    "chatMessage": [{
    "id": "38912",
    "from": "chris",
    "to": "",
    "body": "Some text ...",
    "sent_at": "2010-02-21T21:23:43.687Z"
}, {
    "id": "38913",
    "from": "lebowski",
    "to": "",
    "body": "More text ...",
    "sent_at": "2010-02-21T21:23:43.970Z"
}],

    "stock": { /* ... */ },
    /* ... */
}
```

* クライアントは、2つのことを行って一貫性の取れたインターフェイスを提供する
    * 1.単一のトピックだけを観察可能する
        * 観察者がフィード全体ではない
    * 2.指定されたトピックのメッセージが届くたびに一度ずつ観察者を呼び出す

### observableオブジェクトと類似

* クライアントのインターフェイスは、形もふるまいも、observableオブジェクトと類似
* このクライアントを使うコード
    * データがサーバーからフェッチされる
    * サーバーに送られることを意識しなくて済む
* このクライアントを使うコードのテストでは、通常の`observable`を使用可能 
    * テストでのサーバー接続を避けるためにスタブの`XMLHttpRequest`を使用不要
    * さらに、2つの同じインターフェイスを作ったため
    
### ajax.cometClientを作る

* 問題のオブジェクトが存在することのアサート
* 名前としては、ajax.cometClientが妥当
* 以下は、このajax.cometClientが存在するかどうかをテストしている
    * このテストは、test/comet_client_test.jsという新しいファイルに格納してある

```javascript
//ajax.cometClientは存在するはず
(function () {
    var ajax = tddjs.ajax;

    TestCase("CometClientTest",{
        "test should be object":function () {
            assertObject(ajax.cometClient);
        }
    });
}());
```

* 実装は、ファイルの初期セットアップを作るだけ

```javascript
//comet_client.jsファイルをセットアップする
(function () {
    var ajax = tddjs.namespace("ajax");

    ajax.cometClient = {};
}());
```
### データをディスパッチする

* 観察者が追加されたら、クライアントからデータがディスパッチされるときに、観察者が呼び出されなければならない
* `observe()`の内部を規定するようなテストを書くことも可能
    * しかしそうすると、不必要に特定の実装に縛られたテストになってしまう
* さらに、observableのテストケース全体をレプリケートすることは避けたい
* そこで、dispatchの実装から始める
* dispatchは、後でobserveのふるまいを確かめるときに役に立つ
* ディスパッチとは、サーバーから受け取ったデータを分解して、観察者に送る処理のこと

#### ajax.cometClient.dispatchを追加する

* データのディスパッチの最初のテストは、単純にメソッドが存在することを確かめる

```javascript
//dispatchが存在することを確かめる
"test should have dispatch method":function () {
    var client = Object.create(ajax.cometClient);

    assertFunction(client.dispatch);
}
```

このテストは不合格になるので、以下を追加する

```javascript
//dispatch()を追加する
function dispatch () {
}

ajax.cometClient = {
    dispatch: dispatch
};
```
#### データを委譲する

* 次に、dispatchにオブジェクトを与える
* `dispatch`が観察者にデータをプッシュするのを確かめる
* しかし、まだobserveを書いていない
* そのため、2つのメソッドが正しく動作しなければ合格しないテストを書かない
    * どちらかが失敗時に困るため
* 本来、単体テストが不合格になれば、どこに問題があるかがはっきりとわかる
    * しかしまだ存在しない2つのメソッドで互いのふるまいをチェックしても何もわからない
* それよりも、`observable`を使うことを活用する
    * これら2つのメソッドを実装するため
    
## テストの追加

### 呼び出し確認

* 以下はdispatchが、`observers.notify()`を呼び出すことを確かめている
    * observers: observableオブジェクト
* このテストで使う単純なデータオブジェクトは、規定したフォーマットに従う

```javascript
//dispatchがnotifyを呼び出していることを確かめる
"test dispatch should notify observers":function () {
    var client = Object.create(ajax.cometClient);
    client.observers = { notify: stubFn() };

    client.dispatch({ someEvent: [{ id: 1234}] });

    var args = client.observers.notify.args;

    assert(client.observers.notify.called);
    assertEquals("someEvent", args[0]);
    assertEquals({id: 1234}, args[1]);
}
```

## ソース修正

* データオブジェクトのプロパティをループで処理
* さらに各トピックのイベントをループで処理
* 観察者に1つずつ渡していく
* これでテストには合格するようになる
* しかしこのメソッドは、明らかにかなりの前提条件を抱え込んでいる
* そのため様々な状況で簡単にエラーを起こす

```javascript
//データをディスパッチする
function dispatch(data) {
    var observers = this.observers;
    tddjs.each(data, function (topic, events) {
        for (var i = 0, l = events.length; i < l; i++) {
            observers.notify(topic, events[i]);
        }
    });
}
```

## テストの追加

### エラー処理を改善する

* observersがなくてもdispatchがエラーを起こさないことを確かめている 
* ディスパッチ関連のすべてのテストを独自のテストケースにまとめる
* テストケースは、2つのテストを追加している
    * observersオブジェクトが存在しないという条件にdispatchが対処できることをチェックするもの
    * observersオブジェクトが書き換えられていないことをチェックするもの
        * 後者は、observersが公開オブジェクト
        * 外部コードに書き換えられる可能性があるというだけの理由でここに追加されたもの

```javascript
//observersがなければどうなるか
TestCase("CometClientDispatchTest", {
    setUp: function () {
        this.client = Object.create(ajax.cometClient);
    },

    /* ... */

    "test should not throw if notify undefined":function () {
        this.client.observers = {};

        assertNoException(function () {
            this.client.dispatch({ someEvent: [{}] });
        }.bind(this));
    }
});
```

## ソース修正

```javascript
//observersに注意を払う
function dispatch(data) {
    var observers = this.observers;

    if (!observers || typeof observers.notify != "function") {
        return;
    }

    /* ... */
}
```

## テストの追加

* メソッドが受け取るデータ構造に対する思い込みを和らげる
* dispatchに誤ったデータを与えても、エラーが起きないことを確かめる
    * 今のところ成功する2つのテストを追加している
* 後の方のテストだけが不合格になる
* 以下のことに対処できている
    * dispatchはすでに引数としてnullが渡されること
    * 引数がまったく渡されなかったりすること
* tddjs.eachは、反復処理に適さない入力も処理可能に作られているため

```javascript
//dispatchに誤ったデータを渡す
TestCase("CometClientDispatchTest", {
    setUp: function () {
        this.client = Object.create(ajax.cometClient);
        this.client.observers = { notify: stubFn() };
    },

    /* ... */

    "test should not throw if data is not provided":
        function () {
            assertNoException(function () {
                this.client.dispatch();
            }.bind(this));
        },

    "test should not throw if event is null":function () {
        assertNoException(function () {
            this.client.dispatch({ myEvent: null });
        }.bind(this));
    }
});
```

## テストを実行

* 最後のテストに合格するよう修正

```javascript
//イベントデータの反復処理に注意を注ぐ
function dispatch(data) {
    /* ... */

    tddjs.each(data, function (topic, events) {
        var length = events && events.length;

        for (var i = 0; i < length; i++) {
            observers.notify(topic, events[i]);
        }
    });
}
```

## 残タスク

* ディスパッチテストケースを完成させるために不足しているテスト
    * `notify`がdata内のすべてのトピックに対して呼び出されていることを確かめる
    * トピックの観察者全部にすべてのイベントが渡されていることを確かめる
