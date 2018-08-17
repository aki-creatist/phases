# 動作確認

* サーバーに若干の調整を加えると、アプリケーションを動かすことができる
* もとのリストでは、サーバーはコントローラのためにchatRoomをセットアップしていなかった
* アプリケーションをうまく実行するには書き換えなければならない

```javascript
//サーバーの最終的な形
var http = require("http");
var url = require("url");
var crController = require("chapp/chat_room_controller");
var chatRoom = require("chapp/chat_room");
var room = Object.create(chatRoom);

module.exports = http.createServer(function (req, res) {
    if(url.parse(req.url).pathname == "/comet") {
        var controller = crController.create(req, res);
        controller.chatRoom = room;
        controller[req.method.toLowerCase()]();
    }
});
```

* このコードは動作させるためには、フェイクのchatRoomモジュールを追加する必要がある
* 以下の内容をlib/chapp/chat_room.jsに保存しよう 

```javascript
//フェイクのチャットルーム
var sys = require("sys");

var chatRoom = {
    addMessage: function (user, message){
        sys.puts(user + ": " + message);
    }
};

module.exports = chatRoom;
```

* 以下は、対話的Nodeシェルのnode-replを使用
* POSTデータをエンコード
* CLI HTTPクライアントのcurlを使ってアプリケーションにポストする方法を示したもの
* この部分を別のシェルで実行し、アプリケーションを実行しているシェルの出力を見てみよう 

```bash
#CLIから手作業でアプリケーションをテストする
node-repl
```

```text
node> var msg ={ user:"cjno", message:"Enjoying Node.js" };
node> var data = { topic: "message", data: msg };
node> var encoded = encodeURI(JSON.stringify(data));
node> require("fs").writeFileSync("chapp.txt", encoded);
node> Ctrl-d
```

```bash
curl -d 'cat chapp.txt' http://localhost:8000/comet
```

* 最後のコマンドを入力すると、すぐに応答が返ってくる（つまり、すぐにプロンプトが表示される）
* そして、サーバーを実行しているシェルには、「cjno: Enjoying Node.js」と表示される
