# プロミス

* プロミスを使うようにaddMessageをリファクタリングする

## テストの追加

* エラーハンドリング
    * オブジェクトを渡さずにsetModelを呼び出したらどうなるか
    * observeをサポートしないオブジェクトを引数としたらどうなるか
* テストを書き、必要に応じて実装も更新する

### プロミスを返す

* 新しいテストを追加する
* addMessageがプロミスオブジェクトを返すことを確かめる

```javascript
//addMessageがプロミスを返すことを確かめる
testCase(exports, "chatRoom.addMessage",{
    /* ... */

    "should return a promise": function (test) {
        var result = this.room.addMessage("cjno", "message");

        test.isObject(result);
        test.isFunction(result.then);
        test.done();
    }
});
```

* テストケースは、this.roomにセットアップメソッドを使用使ってchatRoomオブジェクトを作っているはず
* しかし、今のaddMessageはオブジェクトを返していないので、テストは不合格になる
* そこで、空のプロミスオブジェクトを返して、この問題を解決する

```javascript
//空のプロミスオブジェクトを返す
require("function-bind");
var Promise = require("node-promise/promise").Promise;
var id = 0;

var chatRoom = {
    addMessage: function (user, message, callback) {
        process.nextTick(function () {
            /* ... */
        }.bind(this));

        return new Promise();
    },

    /* ... */
};
```

## テスト修正

### プロミスを拒否する

* 次からは、プロミスを使えるようにもとのテストを書き換えていく
* 最初は`addMessage`がエラーを引数としてコールバックを呼び出すことを確認する
    * ユーザー名がaddMessageに渡されなかった際に動作
* 更新後のテストは、以下のようになる 
* プロミスは`then()`を持っている
    * 呼び出しの処理が終わったときに呼び出されるコールバックを追加可能
* コールバックは1つまたは2つの関数を受け付ける
* 第1の関数は成功コールバック、第2の関数はエラーコールバック
* addCallback、`addErrback()`でも同じことが可能
    * thenなら、`addMessage(user, msg).then(callback)`ように読める

```javascript
//返されたプロミスを使う
"should require username": function (test) {
    var promise = this.room.addMessage(null, "message");

    promise.then(function () {}, function (err) {
        test.isNotNull(err);
        test.inherits(err, TypeError);
        test.done();
    });
}
```

## ソース修正

* テストに合格するには、`addMessage`に重複するコードを組み込む
    * まだ古い実装を取り除く段階には入っていないため
* エラーを引数としてプロミスの`reject()`を呼び出す
    * 通常、rejectが呼び出される
    * エラーハンドラが登録されていなければ、プロミスは例外を投げる
* しかし、その他のテストはまだプロミスを使うように更新していない
    * 例外を投げないように第2引数としてtrueを渡す
        * エラーを処理しなくてもよいということに決めていたため
* これでテストに合格するようになる

```diff
  //addMessageを更新する
  addMessage: function (user, message, callback) {
+     var promise = new Promise();
      process.nextTick(function () {
          /* ... */

          if (err) {
              promise.reject(err, true);
          }
      }.bind(this));
-     return new Promise();
+     return promise;
  }
```

## テストの修正

* メッセージを省略するとエラーが起きるようにする
* プロミスを使ってこのテストに合格するようにするためにaddMessageに加える

### プロミスを解決する

* 新しく追加されたメッセージオブジェクトがコールバックに渡されるのを確かめる
* プロミスは、コールバックのエラー引数を取り除ける
    * 成功ハンドラと失敗ハンドラを別々に持っているため

```javascript
//プロミスが成功の処理をすることを確かめる
"should call callback with new object": function (test) {
    var txt = "Some message";

    this.room.addMessage("cjno", txt).then(function (msg){
        test.isObject(msg);
        test.isNumber(msg.id);
        test.equals(msg.message, txt);
        test.equals(msg.user, "cjno");
        test.done();
    });
}
```

## ソース修正

* 実装は、プロミスの`resolve()`を呼び出すコードを追加するのみ
* これでまた1つ書き換えたテストに合格する

```diff
  //プロミスを解決する
  if (err) {
-     promise.reject(err, true);
+     this.message.push(data);
+     promise.resolve(data);
  }
```

## リファクタリング要素

* すべてのテストを更新したら、コールバックを取り除くべきかどうかを決める必要がある
* 残しておけば、どちらのパターンを使いたいかをユーザーが決められる
    * しかし開発側からすると、メンテナンスしなければならないコードが増える
* 手作業のコールバックの方を取り除けば、それがテストに合格したか気にする必要がなくなる
    * プロミスがすべてのコールバックの仕事を処理してくれるため
* プロミス版だけを使う方がお勧め

## プロミスを消費する

* ここで複数のメッセージを追加しなければならないコードを単純化可能
    * `addMessage()`がプロミスを使うようになったため
* Node-promiseは、任意の個数のプロミスを受け付け、新しいプロミスを返すall関数を持っている
* この新しいプロミスは、すべてのプロミスが完了したときに成功となる
* これを利用すれば、一意なIDテストは、以下のような書き方も可能

```javascript
//allでプロミスを1つにまとめる
/* ... */
var all = require("node-promise/promise").all;

/* ... */

testCase(exports, "chatRoom.addMessage", {
    /* ... */

    "should assign unique ids to messages": function (test) {
        var room = this.room;
        var message = [];
        var collect = function (msg) { message.push(msg); };

        var add = all(room.addMessage("u", "a").then(collect),
            room.addMessage("u", "b").then(collect));
        add.then(function () {
            test.notEquals(messages[0].id, messages[1].id);
            test.done();
        });
    },

    /* ... */
});
```

## ソース修正

* 一貫性を保つために、`getMessagesSince()`もプロミスを使うように書き換えなければならない
* リファクタリング中は、同時に複数のテストに不合格になることがないように注意
* 作業が終わったら、以下のようになっているはず

```javascript
//プロミスを使ってリファクタリングしたgetMessagesSince
getMessagesSince: function (id) {
    var promise = new Promise();

    process.nextTick(function () {
        promise.resolve((this.messages || []).slice(id));
    }.bind(this));

    return promise;
}
```