# メッセージをフェッチする

* 後々、cometClientを使ってチャットバックエンドとやり取りする
* そのため、chatRoomは、トークン以降の全てのメッセージを取り出す方法が必要
    * `getMessagesSince()`を追加する
        * 引数としてIDを受け付ける
        * コールバックにメッセージの配列を渡す

## getMessagesSince()

* メソッドの最初のテスト
    * 2つのメッセージを追加
    * 第1のメッセージのID以降に追加されたすべてのメッセージを取得しようとする
    * `IDがどのようにして生成されているか`の想定をテストに持ち込まなくて済む
* getMessageSinceがないので、このテストは不合格になる

```javascript
//メッセージが取得されていることを確かめる
testCase(exports, "chatRoom.getMessagesSince",{
    "should get messages since given id": function (test) {
        var room = Object.create(chatRoom);
        var user = "cjno";
        room.addMessage(user, "msg", function (e, first){
            room.addMessage(user, "msg2", function (e, second){
                room.getMessagesSince(first.id, function (e, msgs){
                    test.isArray(msgs);
                    tes.same(msgs.[second]);
                    test.done();
                });
            });
        });
    }
});
```

## ソース修正

### 空メソッドを追加

* 引数なしで単純にコールバックを呼び出す空メソッドを追加

```javascript
//getMessagesSinceを追加する
var chatRoom = {
    addMessage: function (user, message, callback){ /* ... */ },

    getMessagesSince: function (id, callback) {
        callback();
    }
};
```

### addMessageを修正

* addMessageは実際にメッセージをどこかに格納しているわけではない
    * getMessagesSinceにはメッセージの取得のしようがないため
* addMessageを修正が必要

```javascript
//本当にメッセージを追加する
addMessage: function (user, message, callback) {
    /* ... */
    if(!err){
        if(!this.message){
            this.message = [];
        }
        var id = this.messages.length + 1;
        data = { id: id, user: user, message: message };
        this.messages.pudh(data);
    }
    /* ... */
}
```

### メッセージをフェッチする

* `getMessagesSince`
    * 何らかのIDよりも後に追加されたすべてのメッセージを取り出す
* 専用のカウンタを管理しなくても、配列の添字からIDを取得できる
    * メッセージを格納するための配列を作ったため
    * 添字に1を加えた値をIDにすれば、0でなく1が先頭になる
    * 0が先頭のIDを使うと、すべてのメッセージを取得時に、-1を指定しなければならない
* IDは、messages配列の添字に直接関係のあるものになったので、データの取得は簡単

```diff
//メッセージをフェッチする
  getMessageSince: function (id, callback) {
-     callback();
+     callback(null, this.message.slice(id));
  }
```

* これで、getMessageSinceのテストを含むすべてのテストに合格する
* getMessageSinceが確実に動作するようにするには、以下の点を修正する
    * messages配列が存在しないときには空配列を生成しなければならない
    * 指定に合致するメッセージがないときには空配列を生成しなければならない 
    * コールバックが与えられていないときでも、例外を投げてはならない
* リファクタリングが必要
    * `addMessage`と`getMessagesSince`のテストケースは、セットアップメソッドを共有すべき

## テストを追加する

### addMessageを非同期にする

* `addMessage()`は、コールバックベースだが、まだ同期インターフェイスになっている
* このインターフェイスでコールバックで重い処理をすると`addMessage`をブロックする恐れがある
* Nodeの`rocess.nextTick(callback)`を活用すれば、この問題を緩和可能
* このメソッドは、イベントループの次のパスでコールバックを呼び出す
* addMessageはこの時点では同期的なので、このテストは不合格になる

```javascript
//addMessageが非同期になっていることを確かめる
"should be asynchronous": function (test) {
    var id;

    this.room.addMessage("cjno", "Hey", function (err, msg){
        id = msg.id;
    });

    this.room.getMessagesSince(id - 1, function (err, msgs) {
        test.equals(msgs.length, 0);
        test.done();
    });
}
```

## ソース修正

* `nextTick()`を使うようにaddMessageを書き換える
* これでテストには合格する
    * 合格するのは、getMessagesSinceがまだ同期的だからにすぎない
* このメソッドも非同期的にするとテストには合格しなくなる
    * すると、messages配列を直接チェックしなければならなくなる
    * 実装の詳細をテストすると、テストと実装が密結合になってしまうため、通常は問題がある
    * 非同期的なふるまいのテストも、実装と密結合している
* そこで、実装を掘り下げるテストを追加するのではなく、不合格になるテストを取り除く

```javascript
//addMessageを非同期にする
require("function-bind");
var id = 0;

var chatRoom = {
    addMessage: function (user, message, callback) {
        process.nextTick(function () {
            /* ... */
        }.bind(this));
    },

    /* ... */
}
```
