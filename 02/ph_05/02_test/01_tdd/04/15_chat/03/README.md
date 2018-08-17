# イベントリスナーを追加する

## 概要

* フォームのサブミットイベントにイベントリスナーを追加する
    * イベントリスナーの追加には、tdd.js.dom.addEventHandlerインターフェイスを使用
    * イベントハンドラのテスト
        * アプリケーションコードでイベントハンドラの単体テストを行う

## TODO

* tddjs.dom.addEventHandlerのような抽象を通じてイベントハンドラを追加する
    * 確かめこと: このメソッドが正しく呼び出されること
* tddjs.dom.addEventHandlerをスタブに置き換える
    * tddjs.dom.addEventHandlerに渡される引数を操作可能にするため
    * ハンドラを手作業で呼び出せる

## 備考

* マウス座標、隣の要素などのイベントデータに強く依存するテストは、複雑なセットアップを必要とする
    * セットアップは、テスト専用のフェイクのイベント実装などで隠せる
    * アプリケーションの単体テストスイートは、イベントデータに強く依存するテストには適さない

## テストの追加

* 依存コードにまだaddEventHandlerを含めていない
    * addEventHandlerをスタブに置き換える前に、`namespace()`を使ってdom名前空間を取り込む
        * トラブルを避けるため

```javascript
//要素のサブミットイベントが処理されることをを確かめる
"test should handle submit event": function () {
    var controller = Object.create(userController);
    var element = {};
    var dom = tddjs.namespace("dom");
    dom.addEventHandler = stubFn();
    
    controller.setView(element);
    
    assert(dom.addEventHandler.called);
    assertSame(element, dom.addEventHandler.args[0]);
    assertEquals("submit", dom.addEventHandler.args[1]);
    assertFunction(dom.addEventHandler.args[2]);
}
```

## ソース修正

### メソッド呼び出しを追加

* 入力を削減し、識別子の解決をスピードアップするためにローカルエリアスを使うのは効果的
    * しかし、そうすると使う前にオブジェクトがキャッシュされてしまう
    * tddjs.domオブジェクトは、ローカル変数のdomに代入時には手が届かない
        * ソースファイルが先にロードされるため
    * しかし、テストがdom.addEventHandlerを呼び出すまでに、テストは空白を埋めている
* `namespace()`を使う
    * 両方のファイルで同じオブジェクトを参照できる
    * どちらが先にロードされるかを気にする必要がない
* このテストは合格する
    * しかし、前のテストがエラーを起こすようになる
        * 前のテストを実行する時点では、`addEventHandler()`が存在しないため

```javascript
//サブミットイベントハンドラを追加する
var dom = tddjs.namespace("dom");

function setView(element) {
    element.className = "js-chat";
    dom.addEventHandler(element, "submit", function() {});
}
```

### 重複をsetUpにまとめる

* 共通するコードを`setUp()`にまとめ、問題解決
    * テストコードの重複も取り除ける 
* このリファクタリングによって、両方のテストが合格するようになる
    * 2つのテストはsetViewを使用方法は同様
        * setView呼び出しは`セットアップ処理の一部ではなく、テスト自体の一部`
        * そのためsetUpには含めない

```diff
//重複するコードをsetUpにまとめる
  /* ... */
+ var dom = tddjs.namespace("dom");
  /* ... */
  TestCase("UserFormControllerSetViewTest", {
+     setUp: function() {
          this.controller = Object.create(userController);
          this.element = {};
          
+         dom.addEventHandler = stubFn();
+     },
    
      "test should add js-chat class": function () {
-         controller.setView(element);
+         this.controller.setView(this.element);
        
+         assertClassName("js-chat", this.element);
+     },
    
      "test should handle submit event": function() {
-         var controller = Object.create(userController);
-         var element = {};
-         var dom = tddjs.namespace("dom");
-         dom.addEventHandler = stubFn();
+         this.controller.setView(this.element);
        
          assert(dom.addEventHandler.called);
          assertSame(this.element, dom.addEventHandler.args[0]);
          assertEquals("submit",dom.addEventHandler.args[1]);
          assertFunction(dom.addEventHandler.args[2]);
      }
  });
```

## ソース修正

* イベントハンドラがコントローラオブジェクトにバインドされていることを確かめる必要がある
    * そのためには、stubFnに呼び出し時のthisの値を記録させなければならない

```javascript
//stubFnのなかでthisを記録する
function stubFn(returnValue){
    var fn = function () {
        fn.called = true;
        fn.args = arguments;
        fn.thisValue = this;
        retunr returnValue;
    };

    fn.called = false;
    
    return fn;
}
```

## テストの追加

* 次は、改良したstubFnを使う
    * イベントハンドラがコントローラの`handleSubmit()`
    * コントローラオブジェクトにバインドされていることを確かめる
* このテストは、setView呼び出しを`setUp()`に入れないもう１つの理由を示している
* setViewを呼び出す前に、追加のセットアップ処理が必須
    * `handleSubmit()`をスタブ化する
* 本来のhandleSubmitを使うと、テストが不合格になったりならなかったりするようになってしまう

```javascript
//イベントハンドラはコントローラにバインドされたhandleSubmitだということを確かめる

"test should handle with bound handleSubmit":
function () {
    var stub = this.controller.handleSubmit = stubFn();
    
    this.controller.setView(this.element);
    dom.addEventHandler.args[2]();
    
    assert(stub.called);
    assertSame(this.controller, stub.thisValue);
}
```

## ソース修正

### setViewを書き換える

* これで今のテストは合格するようになる
* また前のテストが不合格になる
    * コントローラが実際には`handleSubmit()`を定義していないため
    * そこで、handleSubmitをスタブに置き換えていないテストは不合格になる
    
```javascript
//イベントハンドラとしてhandleSubmitをバインドする

function setView(element) {
    element.className = "js-chat";
    var handler = this.handleSubmit.bind(this);
    dom.addEventHandler(element, "submit", handler);
}
```

### handleSubmitを定義する

* handleSubmitをスタブに置き換えていない問題の解決
* コントローラのメソッドとしてhandleSubmitを定義する

```diff
//空のhandleSubmit()を追加する
+ function handleSubmit(event) { //setViewが通る道
+ }

 tddjs.namespace("chat").userFormController = {
-    setView: setView
+    setView: setView,
+    handleSubmit: handleSubmit
```