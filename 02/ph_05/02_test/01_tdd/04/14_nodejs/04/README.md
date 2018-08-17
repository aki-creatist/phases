# 要求に応答する

* コントローラは、メッセージを追加したら、応答を返して接続を閉じなければならない
* ほとんどのWebフレームワークでは、出力のバッファリングと接続のクローズは、水面下で自動的に行われる
* しかし、NodeのHTTPサーバーサポートは、データストリーミングとロングポーリングを意識して設計されている
* そのため、そのように指示しなければ、データはバッファリングされず、接続はクローズされない
* http.ServerResponseは、応答を出力するために役に立つメソッドを提供している
* writeHeadは、ステータスコードと応答ヘッダーを出力する
* writeは応答本体のチャンクを出力する
* そして、endがある 

## ステータスコード

* メッセージが追加されたときにユーザーに与えられるフィードバックはあまりないので、以下は、postが単純に空の「201 Created」を応答することを確かめるテスト 

```javascript
//ステータスコード201が返されることを確かめる
function controllerSetUp() {
    /* ... */
    var res = this.res = { writeHead: stub() };
    /* ... */
}

testCase(exports, "chatRoomController.post",{
    /* ... */
    "should write status header": function (test) {
        var data = { data: {user: "cjno", message: "hi"} };
    this.controller.post();
    this.sendRequest(data);
    
    test.ok(this.res.writeHead.called);
    test.equals(this.res.writeHead.args[0], 201);
    test.done();
    }
});
```

* 以下は、実際にwriteHeadを呼び出す

```javascript
//応答コードを設定する
post: function () {
    /* ... */
    
    this.request.addListener("end", function () {
    var data = JSON.parse(decodeURI(body)).data;
    this.chatRoom.addMessage(data.user, data.message);
    this.response.writeHead(201);
    }.bind(this));
}
```
## 接続をクローズする

* ヘッダーを書き込んだら、接続をクローズしなければならない
* 以下は、それを確かめるテスト 

```javascript
//応答がクローズされることを確かめる
function controllerSetUp() {
    /* ... */
    var res = this.res = {
    writeHead: stub(),
    end: stub()
    };
    
    /* ... */
};

testCase(exports, "chatRoomController.post",{
/* ... */
    "should close connection": function (test) {
        var data = { data: { user: "cjno", message: "hi"} };
        
        this.controller.post();
        this.sendRequest(data);
        
        test.ok(this.res.end.called);
        test.done();
    }
});
```

* このテストは不合格になるので`post()`を書き換えると、すべてテストに合格するようになる 

```javascript
//応答をクローズする
post: function () {
    /* ... */

    this.request.addListener("end", function () {
        this.response.end();
    }.bind(this));
}
```

* `post()`の処理は以上
* しかし、現実に使うシステムの場合は、入力のチェックとエラー処理をもっと厳格に行うことをお勧めする
* メソッドをもっと弾力的なものにすることは、練習問題としておく