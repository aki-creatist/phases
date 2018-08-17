# イベントエミッタ

## 概要

* クライアントがサーバーをポーリングする際の事象は以下2通り
    * 新しいメッセージがあって要求に応答が返り、ただちに終了する
    * メッセージが手に入るまでサーバーが要求を保留にする
    
## 背景

* 今までは第1の条件を対象としてきた
* ロングポーリングを可能にする第2の条件についてはまだ触れていない
* chatRoomは、`waitForMessagesSince()`を提供するようになる
    * しかしこのメソッドは、`getMessagesSince()`と同様の動作する
        * 但し、メッセージがなければ、メッセージが現れるまでただ待つ点を除く

## 実装の要件

* `waitForMessagesSince()`を実装する
* 新しいメッセージが追加されたときにchatRoomがイベントを生成可能にする

## テストの作成

### chatRoomをイベントエミッタにする

* chatRoomがイベントエミッタであることを確かめる
* 最初のテスト
    * `chatRoomがaddListener()`、`emit()`を持つことを確かめる

```javascript
//chatRoomがイベントエミッタになっていることを確かめる
testCase(exports, "chatRoom", {
    "should be event emitter": function (test) {
        test.isFunction(chatRoom.addListener);
        test.isFunction(chatRoom.emit);
        test.done();
    }
});
```

## ソース修正

### プロトタイプの指定

* `chatRoom`のプロトタイプとして`EventEmitter.prototype`を指定する

```javascript
//chatRoomにEventEmitter.prototypeを継承する
/* ... */
var EventEmitter = require("events").EventEmitter;
/* ... */

var chatRoom = Object.create(EventEmitter.prototype);

chatRoom.addMessage = function (user, message) {/* ... */};
chatRoom.getMessagesSince = function (id) {/* ... */};
```

### プロパティ記述子で定義

* プロパティ記述子を使ってメソッドを追加可能
* V8はECMAScript5のObject.createを完全にサポートするため

```javascript
//プロパティ記述子で定義したchatRoom
var chatRoom = Object.create(EventEmitter.prototype,{
    addMessage: {
        value: function (user, message){
            /* ... */
        }
    },

    getMessagesSince: {
        value: function(id){
            /* ... */
        }
    }
});
```

## テストの追加

* 現時点では、プロパティ記述子が提供してくれるものはない
    * ドキュメントされたニーズに応えられていない
* プロパティ記述子は、デフォルトプロパティ属性値をオーバーライド可能
* ここではインデントが増えるコードを避け、単純な代入を使う
* 次に、addMessageがイベントを生成することを確認する

```javascript
//addMessageが"message"イベントを生成することを確かめる
testCase(exports, "chatRoom.addMessage", {
    /* ... */

    "should emit 'message' event": function (test) {
        var message;

        this.room.addListener("message", function (m){
            message = m;
        });

        this.room.addMessage("cjno", "msg").then(function (m) {
            test.same(m, message);
            test.done();
        });
    }
});
```

## ソース修正

* プロミスを解決する直前にemit呼び出しを追加が必要
* イベントを生成可能になったら、`waitForMessagesSince()`作成可能

```javascript
//メッセージイベントを生成する
chatRoom.addMessage= function (user, message, callback) {
    var promise = new Promise()
    process.nextTick(function () {
        /* ... */

        if (!err) {
            /* ... */
            this.emit("message",data);
            promise.resolve(data);
        } else {
            promise.reject(err, true);
        }
    }.bind(this));

    return promise;
};
```

## テストの追加

### メッセージを待つ

* waitForMessagesSinceは、2つのうちのどちらかを行う
    * 指定されたID以降のメッセージがある場合
        * 返されたプロミスをただちに解決する
    * メッセージがない場合
        * メソッドは"message"イベントのためにリスナーを追加
        * 新しいメッセージが追加されたら、戻り値のプロミスを解決する
* 以下はメッセージがある際、ただちにプロミスが解決されることを確かめる 
    * `getMessagesSince()`をスタブ化する
        * `getMessagesSince`の結果があればそれを使うことを確かめるため
```javascript
//メッセージがあればすぐに解決されることを確かめる
/* ... */
var Promise = require("node-promise/promise").Promise;
var stub = require("stub");
/* ... */

testCase(exports, "chatRoom.waitForMessagesSince", {
    setUp: chatRoomSetup;

    "should yield existing message": function (test) {
        var promise = new Promise();
        promise.resolve([{id: 43}]);
        this.room.getMessagesSince = stub(promise);
    
        this.room.waitForMessagesSince(42).then(function (m) {
            test.same([{id: 43}], m);
            test.done();
        });
    }
});
```

## ソース修正

* `getMessagesSince`から返されたプロミスを単純に返す

```javascript
//getMessagesSinceをプロキシにする
chatRoom.waitForMessagesSince = function (id) {
    return this.getMessagesSince(id);
};
```

## テストの追加

* 既存のメッセージをフェッチが失敗した場合
    * メソッドは"message"イベントのためにリスナーを追加
    * スリープに入る
* 以下は、addListenerをスタブ化してこのことを確かめようとしている 
    * ここでも、`getMessagesSince()`をスタブ化する
        * 出力をコントロールするため
    * 次に、空配列を引数としてプロミスを解決する
        * プロミスは制御を返すだけのスタブにしてある
    * こうすると、`waitForMessagesSince()`は"message"イベントのためにリスナーを登録する
    * しかし、waitForMessagesSinceがリスナーを追加しないのを見て、このテストは不合格になる

```javascript
//ウェイトメソッドがリスナーを追加することを確かめる
"should add listener when no messages": function (test) {
    this.room.addListener = stub();
    var promise = new Promise();
    promise.resolve([]);
    this.room.getMessagesSince = stub(promise);

    this.room.waitForMessagesSince(0);

    process.nextTick(function () {
        test.equals(this.room.addListener.args[0], "message");
        test.isFunction(this.room.addListener.args[1]);
        test.done();
    }.bind(this));
};
```

## ソース修正

* 今追加するリスナーは空
    * 何をしなければならないのかを指示するテストがまだないため


```javascript
//メッセージがなければリスナーを追加する
chatRoom.waitForMessagesSince = function (id) {
    var promise = new Promise();

    this.getMessagesSince(is).then(function (messages) {
        if(messages.length > 0) {
            promise.resolve(messages);
        } else {
            this.addListener("message", function () {});
        }
    }.bind(this));

    return promise;
};
```

## テストの追加

### 動作を指示するテスト

* メッセージを追加すると、`waitForMessagesSince`がプロミスを解決することを確かめる
    * この際、新メッセージを引数とする
* `getMessagesSince`に合わせて、1つのメッセージが配列の形で届くものとする
* テストはも合格しない
    * 追加したばかりの"message"リスナーの中身を作れと要求してくる
    
```javascript
//メッセージが追加されると待ち要求が解決する
"new message should resolve waiting": function (test) {
    var user = "cjno";
    var msg = "Are you waiting for this?";
    this.room.waitForMessagesSince(0).then(function (msgs) {
        test.isArray(msgs);
        test.equals(msgs.length, 1);
        test.equals(msgs[0].user, user);
        test.equals(msgs[0].message, msg);
        test.done();
    });

    process.nextTick(function () {
        this.room.addMessage(user, msg);
    }.bind(this));
}
```

## ソース修正

* 動作するリスナーのコードを追加する
* これで全てのテストに合格する

```javascript
//メッセージリスナーを実装する
/* ... */

this.addListener("message", function (message) {
    promise.resolve([message]);
});

/* ... */
```


* `waitForMessagesSince`から返されたプロミスが解決されたら、"message"イベントに追加されたリスナーはクリアする必要がある
* そうでなければ、現在の要求の終了後も、最初のwaitForMessagesSince呼び出しは、メッセージが追加されるたびにリスナーのコールバックを呼び出し続けてしまう
* リスナーをクリアするには、ハンドラとして追加した関数の参照を管理して、this.removeListenerを呼び出さなければならない
* クリアのテストには、`root.listeners()`がリスナーの配列を返すことを知っていると役に立つ
