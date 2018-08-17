# メッセージを追加する

* それでは、コントローラの核心に入っていこう
* メッセージを受信し、メッセージのためのDOM要素を作り、それをビューに注入する作業だ

## テストの作成

* 最初のテスト
    * 定義リストに`＠`を前に付けたユーザー名を含むdt要素が追加されていること
* メッセージを追加してから、定義リストにdt要素が追加されていることを確かめる

```javascript
//ユーザー名がdt要素としてDOMに注入されていることを確かめる
TestCase("MessageListControllerAddMessageTest", {
    setUp: messageListControllerSetUp,

    "test should add dt element with @user": function () {
        this.controller.setModel(this.model);
        this.controller.setView(this.element);

        this,controller,addMessage({
            user: "Eric",
            message: "We are trapper keeper"
        });

        var dts = this.element.getElementsByTagName("dt");
        assertEquals(1, dts.length);
        assertEquals("@Eric", dts[0].innerHTML);
    }
});
```

## ソース修正

* 要素を作ってビューに追加しなければならない 
* テストは不合格になる
* this.viewがundefined
* ビューはプロパティでなければならない
    * ドキュメントされた要件
    
```javascript
//リストにユーザーを追加する
function addMessage(message) {
    var user = document.createElement("dt");
    user.innerHTML = "@" + message.user;
    this.view.appendChild(user);
}
```

## setViewを修正

* 要素の参照を格納するようにsetViewを修正
* ビューが参照を格納するようになると、すべてのテストが合格する
* しかし、まだメッセージをテストしていない


```javascript
//ビュー要素に参照を格納する
function setView(element) {
    element.className = "js-chat";
    this.view = element;
}
```

## テストの追加

* これもDOMに追加されなければならない
* 以下は、メッセージがDOMに追加されていることを確かめる 
* ここでも、セットアップコードの一部はすぐに`setUp()`に追加
    * テストの目的が明らかになるようにしている

```javascript
//メッセージがDOMに追加されていることを確かめる
TestCase("MessageListControllerAddMessageTest", {
    setUp: function() {
        messageListControllerSetUp.call(this);
        this.controller.setModel(this.model);
        this.controller.setView(this.element);
    },

    /* ... */

    "test should add dd element with message": function () {
        this.controller.addMessage({
            user: "Theodore",
            message: "We are one"
        });

        var dds = this.element.getElementsByTagName("dd");
        assertEquals(1, dds.length);
        assertEquals("We are one", dds[0].innerHTML);
    }
});
```

## ソース修正

* テキストの内容とタグ名を変えて、先ほどと同じ3行を繰り返す必要がある
* 現在のサーバーは、メッセージをどのような形でもフィルタリングしていない

```javascript
//メッセージをdd要素として追加する
function addMessage(message) {
    /* ... */
    var msg = document.createElement("dd");
    msg.innerHTML = message.message;
    this.view.appendChild(msg);
}
```

## テストの追加

* HTMLを含むメッセージがエスケープされることを確かめるテストを追加
    * ユーザーがチャットクライアントをハイジャックするのを避けるため
* テストは不合格になる

```javascript
//基本的なXSS防御が備わっていることを確かめる
"test should escape HTML in message": function () {
    this.controller.addMessage({
        user: "Dr. Evil",
        message: "<script>window.alert('p4wned!');</script>"
    });

    var expected = "<script>window.alert('p4wned!');" +
        "</script>";
    var dd = this.element.getElementsByTagName("dd")[1];
    assertEquals(expected, dd.innerHTML);
}
```

## ソース修正

* 悪い人がチャットクライアントを乗っ取るのを防ぐものはない
* 以下は、スクリプト注入に対する基本的な防御コードを追加

```javascript
//基本的なXSS保護を追加する
function addMesasge(message) {
    /* ... */
    msg.innerHTML = message.message.replace(/</g, &quot;<&quot;);
    this.view.appendChild(msg);
}
```
