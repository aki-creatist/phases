# テストケースのセットアップ

* テストケースをセットアップして、初期状態のテストケースを追加する
    * userFormControllerがオブジェクトであることを確かめるテスト
* `test/user_form_controller_test.js`を作成する

```javascript
//オブジェクトが存在することを確かめる
(function () {
    var userController = tddjs.chat.userFormController;
    
    TestCase("UserFormControllerTest", {
        "test should be object": function () {
        assertObject(userController);
        }
    });
}());
```

* userFormControllerオブジェクトをセットアップ
* `src/uer_form_controller.js`

```javascript
//コントローラを定義する
tddjs.namespace("chat").userFormController = {};
```

テストでsetViewが関数だということを確かめる

```javascript
//serViewが関数だということを確かめる
"test should have setView method": function() {
    assertFunction(userController.setView);
}
```

テストに合格するために、空メソッドを追加する

```diff
//空のsetView()を追加する
+ (function() {
+    function setView(element){}
    
     tddjs.namespace("chat").userFormController = {
+        setView: setView
+    };
+ }());
```