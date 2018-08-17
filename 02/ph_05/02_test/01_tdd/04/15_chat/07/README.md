# コントローラとメソッドを定義する

## テストの追加

### コントローラが存在することを確かめる

* コントローラが存在することを確かめる

```bash
touch test/message_list_controller_test.js
```

```javascript
//messageListControllerがオブジェクトであることを確かめる
(function () {
    var listController = tddjs.chat.messageListController;

    TestCase("MessageListControllerTest", {
        "test should be object": function () {
            assertObject(listController);
        }
    });
}());
```

### ソースを実装

```bash
touch lib/message_list_controller.js
```

```javascript
//messageListControllerを定義する
(function() {
    var chat = tddjs.namespace("chat");
    chat.messageListController = {};
}());
```

## テストの追加

### コントローラがsetModel()を持つことを確かめる 

```javascript
//setModelが関数だということを確かめる
"test should have setModel method": function () {
    assertFunction(listController.setModel);
}
```

## ソース修正

```javascript
//空のsetModelを追加する
function setModel(model) {}

chat.messageListController = {
    setModel: setModel
};
```

## テストの追加

### メッセージの購読

* setModelは、モデルの"message"チャネルを観察しなければならない
* 本番コードでは、モデルオブジェクトは`cometClient`
    * `cometClient`: サーバーからメッセージをストリーム転送する
* `observe`が呼び出されていることを確かめる 
* このテストは不合格になる

```javascript
//setModelが"message"チャネルを観察していることを確かめる
TestCase("MessageListControllerSetModelTest", {
    "test should observe model's message channel":
        function() {
            var controller = Object.create(listController);
            var model = { observe: stubFn() };

            controller.setModel(model);

            assert(model.observe.called);
            assertEquals("message",model.observe.args[0]);
            assertFunction(model.observe.args[1]);
        }
});
```

## ソース修正

* observe呼び出しをして、テストを合格させる 

```javascript
//observeを呼び出す
function setModel(model){
    model.observe("message", function() {} );
}
```

## テストの追加

* ハンドラがバインドされた`addMessage()`だということを確かめる
* ユーザーフォームコントローラでDOMイベントハンドラに対してしたのと同じようなテスト
* このテストはフライング気味
    * テストのセットアップコードの重複を避けるためにすぐにsetUpが必要なのが自明なため

```javascript
//バインドされたaddMessageが"message"ハンドラだということを確かめる
TestCase("MessagelistControllerSetModelTest", {
    setUp: function () {
        this.controller = Object.create(listController);
        this.model = { observe:stubFn() };
    },

    /* ... */

    "test should observe with bound addMessage": function() {
        var stub = this.controller.addMessage = stubFn();

        this.controller.setModel(this.model);
        this.model.observe.args[1]();

        assert(stub.called);
        assertSame(this.controller, stub.thisValue);
    }
});
```

## ソース修正

### 正しいハンドラを追加

* model.observeに正しいハンドラを追加する
* このテストは合格するが、前のテストは不合格になる

```javascript
//バインドされたメソッドで"message"チャネルを観察する
function setModel(model) {
    model.observe("message", this.addMessage.bind(this));
}
```

### addMessageを追加

* コントローラにバインドしているaddMessageを追加する
* `addMessage`をスタブに置き換えていないテストが不合格にならないようにする
* `addMessage()`のテストに移る前に、ビューを追加が必要
    * addMessageの役割は、ビューに注入するDOM要素を作ることであるため
    
```javascript
//空のaddMessageを追加する
/* ... */
function addMessage(message) {}

chat.messageListController = {
    setModel: setModel,
    addMessage: addMessage
};
```



