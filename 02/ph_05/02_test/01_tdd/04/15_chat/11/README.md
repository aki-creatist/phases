# 機能テスト

* メッセージリストコントローラは、基本DOMサポートのある環境でなければ正しく動作しない

## ソース修正

* 機能テストを追加したコントローラ

```javascript
//messageListControllerのための機能テスト
(function () {
    if (typeof tddjs == "undefined" ||
        typeof document == "undefined" ||
        !document.createElement) {
        return;
    }

    var element = document.createElement("dl");

    if (!element.appendChild ||
        typeof element.innerHTML != "string") {
        return;
    }

    element = null;
    /* ... */
}());
```

## 動作確認

* コントローラが動くようになった
* chappを書き換える
    * ユーザーが名前を入力した後で、メッセージリストコントローラを初期化するようにする
* まず、新しい依存コードが必要

```bash
cp json2.js public/js/
cp url_params.js public/js/
cp ajax.js public/js/
cp request.js public/js/
cp poller.js public/js/
cp message_list_controller.js public/js/
```

* index.htmlにscript要素を追加していく
* 以前のscript要素の後ろに、上に書かれている順序で取り込む
* 但し、js/chat_client.jsファイルがインクルードリストの最後になるようにする
* index.htmlに、空のdl要素を1つ追加し、id="messages"を指定する
* そして、chat_client.jsファイルを下記に更新する 

```javascript
//更新後のブートストラップスクリプト
(function () {
    if (typeof tddjs == "undefined" ||
        typeof document == "undefined") {
        return;
    }

    var c = tddjs.namespace("chat");

    if (!document.getElementById || !tddjs ||
        !c.userFormController || !c.messageListController) {
        alert("Browser is not supported");
        return;
    }

    var model = Object.create(tddjs.ajax.cometClient);
    model.url = "/comet";

    /* ... */

    userController.observe("user", function(user) {
        var messages = document.getElementById("messages");
        var messagesController =
            Object.create(c.messageListController);
        messagesController.setModel(model);
        messagesController.setView(messages);

        model.connect();
    });
}());
```

* curlを使ってメッセージをポストすると、それがすぐにブラウザに表示される
* 十分な数のメッセージをポストする
    * 文書にスクロールバーがつき、メッセージが囲みの下に表示されることに気付く
