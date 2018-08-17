# ビューを設定する

## テストの追加

* リストコントローラのsetViewの開発は、最初からDOM要素を使用
    * 今まではフェイクオブジェクトから初めていた
* `setView`がビュー要素に"js-chat"クラスを設定していることを確かめる 
* セットアップコードを別メソッドに抽出する
* このテストは、`setView()`が存在しないので不合格になる

```javascript
//setViewが要素のクラス名を設定していることを確かめる
function messageListControllerSetUp() {
    /*:DOC element = <dl></dl> */

    this.controller = Object.create(listController);
    this.model = { observe: stubFn() };
}

TestCase("MessageListControllerSetModelTest", {
    setUp: messageListControllerSetUp,
    /* ... */
});

TestCase("MessageListControllerSetViewTest", {
    setUp: messageListControllerSetUp,

    "test should set class to js-chat": function () {
        this.controller.setView(this.element);

        assertClassName("js-chat", this.element);
    }
});
```

## ソース修正

* `setView()`を追加
* テストは合格するようになる 
* 実際にビューを格納するメソッドもあとで必要になる

```javascript
//setView()を追加する
function setView(element) {
    element.className = "js-chat";
}

chat.messageListController = {
    setModel: setModel,
    setView: setView,
    addMessage: addMessage
};
```
