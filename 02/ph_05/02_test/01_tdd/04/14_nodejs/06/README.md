## メッセージを追加する

* chatRoomオブジェクトは、`addMessage()`を持つ必要がある
    * `addMessage()`: ユーザー名とメッセージを受け付ける
* これはチャットルームを使うコントローラが指示している

## NodeのI/O

* chatRoomインターフェイスはストレージバックエンドの役割を果たす
    * I/Oインターフェイスとして分類可能
* Nodeの非同期インターフェイスは、最後の引数としてオプションのコールバックを受け付ける
* コールバックに渡される第1引数は、いつもnullかエラーオブジェクト
    * そのため、専用の「エラーバック」関数は不要
* 以下は、ファイルシステムモジュールを使った例を示している

```javascript
//Nodeでのコールバックとエラーバックの区別の方法
var fs = require("fs");

fs.rename("./text.txt","./text.txt", function (err) {
    if (err) {
        throw err;
    }

//名称変更に成功したので、処理を続行する
});
```

#### 問題のあるデータの処理

* `addMessage()`は、ユーザー名かメッセージのどちらかが無い場合には、エラーを起こさなければならない
    * データの基本的な一貫性を保つため
* しかし、非同期I/Oインターフェイスなので、単純に例外を投げるわけにはいかない
* Nodeの方法に従い、addMessageに登録されたコールバックの第1引数としてエラーを渡す必要がある
* 以下は、ユーザー名が指定されていないときのためのテスト
* このコードは、test/chapp/chat_room_test.jsに保存する

```javascript
//addMessageがユーザー名を必要とすることを確かめる
var testCase = require("nodeunit").testCase;
var chatRoom = require("chap/chat_room");

testCase(exports, "chatRoom.addMessage", {
    "should require username": function (test) {
        var room = Object.create(chatRoom);

        room.addMessage(null, "a message", function (err) {
            test.isNotNull(err);
            test.inherits(err,TypeError);
            test.done();
        });
    }
});
```

## user引数のチェックを追加する

```javascript
//ユーザー名があることをチェックする
var chatRoom = {
    addMessage: function (user, message, callback) {
        if (!user) {
            callback(new TypeError("user is null"));
        }
    }
};
```

## テストの追記

* addMessageがメッセージを必要とすることを確かめる 
* このテストは、コードの重複を引き起こす
    * それはすぐ後で対処する

```javascript
//addMessageがメッセージを必要とすることを確かめる
"should require message": function (test) {
    var room = Object.create(chatRoom);

    room.addMessage("cjno", null, function (err) {
        test.isNotNull(err);
        test.inherits(err,TypeError);
        test.done();
    });
}
```

## テストの修正

* まずチェックを行って、テストに合格させる 

```diff
//メッセージをチェックする
  addMessage: function (user, message, callback) {
      /* ... */

-     if (!user) {
+     if(!message) {
-         callback(new TypeError("user is null"));
+         callback(new TypeError("message is null"));
      }
  }
```

## setUp()を追加

* `setUp()`を追加する
    * chatRoomオブジェクト作成コードの重複を取り除くため

```javascript
//setUp()を追加する
testCase(exports, "chatRoom.addMessage", {
    setUp: function () {
        this.room = Object.create(chatRoom);
    },

    /* ... */
});
```

* 先ほど決めたように、コールバックはオプションでなければならない
* コールバックが指定されていなくてもメソッドが失敗しないことを確かめる 

```javascript
//addMessageがコールバックを必要としないことを確かめる
/* ... */
require("function-bind");

/* ... */

testCase(exports, "chatRoom.addMessage", {
    /* ... */

    "should not require a callback": function (test) {
        test.noException(function () {
            this.room.addMessage();
            test.done();
        }.bind(this));
    }
});
```

* カスタムbindをロード
    * 無名コールバックをtest.noExceptionにバインドするため
* コールバックを呼び出す前にコールバックが呼び出せることをチェックする

```javascript
//コールバックを呼び出す前にコールバックが呼び出せることをチェックする
addMessage: function (user, message, callback) {
    var err = null;

    if(!user){ err = new TypeError("user is null"); }
    if(!message){ err = new TypeError("message is null"); }

    if(typeof callback == "function") {
        callback(err);
    }
}
```

## メッセージの追加に成功する

* メッセージを取得するための方法を作るまでは、メッセージが実際に格納されたことを確認不可
* しかしメッセージの追加が成功したかどうかを示す手がかりは得られるはず
* そこで、`addMessage()`がメッセージオブジェクトを引数としてコールバックを呼び出していること確認
* オブジェクトはIDとともに渡したデータを格納しているはず

```javascript
// addMessageが作成されたメッセージを渡すことを確かめる
"should call callback with new object": function (test) {
    var txt = "Some message";
    this.room.addMessage("cjno", txt, function (err, msg){
        test.isObject(msg);
        test.isNumber(msg.id);
        test.equals(msg.message,txt);
        test.equals(msg.user,"cjno");
        test.done();
    })
}
```

## テストに合格するためのコード

* オブジェクトを引数としてコールバックを呼び出す
    * IDは1とハードコードしてごまかす

```javascript
//コールバックにオブジェクトを渡す
addMessage: function (user, message, callback) {
    /* ... */
    var data;

    if(!err){
        data = { id: 1, user: user, message: message };
    }

    if (typeof callback == "function") {
        callback(err, data);
    }
}
```

## IDが一意であることを確かめる

* 個々のメッセージにそれぞれ一意なIDが与えられることを確かめるテスト
* ネストされたコールバックを使う
* 2つのメッセージを追加してからそれを比較する
* IDはすべてのメッセージを通じて一意でなければならない

```javascript
//メッセージIDが一意になっていることを確かめる
"should assign unique ids to messages": function (test) {
    var user = "cjno";

    this.room.addMessage(user, "a", function (err, msg1){
        this.room.addMessage(user, "b", function (err, msg2){
            test.notEquals(msg1.id, msg2.id);
            test.done();
        });
    }.bind(this));
}
```

## ソースを修正する

* このテストを実行すると、さきほどのずるがばれてしまう
* IDを生成するもっとよい方法を見つけなければならない
* メッセージが追加されるたびにインクリメントされる単純な変数を使用
* これでテストは再び合格する

```diff
  // 一意な整数IDを割り当てる
+ var id = 0;

  var chatRoom = {
      addMessage: function (user, message, callback) {
          /* ... */

          if (!err) {
-             data = { id: 1, user: user, message: message };
+             data = { id: id++, user: user, message: message };
          }
+         if (typeof callback == "function") {
+             callback(err, data);
+         }
        /* ... */
      }
  };
```

