# サブミットイベントの処理

## サブミットイベントの処理の流れ

* ユーザーがフォームをサブミットする
* イベントハンドラはフォームの最初のテキスト入力要素から値を取り出す
* 取り出したモデルのcurrentUserプロパティに代入
* "js-chat"というクラス名を取り除く
* ユーザーコンポーネントの終了を知らせる
* ブラウザが実際にフォームをポストしないように、イベントのデフォルトアクションを中止する

## デフォルトアクションを中止する

* イベントのデフォルトアクションは実行されないようにする
    * 標準に準拠したブラウザでは、イベントオブジェクトの`preventDefault()`を呼び出す
    * ただし、Internet Explorerはメソッドをサポートしていない
        * イベントハンドラからfalseを返さなければならない
    * しかし、addEventHandlerなら、基本的なイベントの正規化をしてくれる 

```javascript
//イベントのpreventDefault()が呼び出されることを確かめる

TestCase("UserFormControllerHandleSubmitTest", {
    "test should prevent event default action": function () {
        var controller = Object.create(userController);
        var event = { preventDefault: stubFn() };
        
        controller.handleSubmit(event);
        
        assert(event.preventDefault.called);
    }
});
```

* ここでも、使っているのはスタブ
* このテストに合格するには、1行追加する

```javascript
//デフォルトアクションを中止する
function handleSubmit(event) {
    event.preventDefault();
}
```

* これでテストには合格する
* 次に２つのテストケースでセットアップが重複していることに対処する
    * セットアップコードを抽出して両方のテストケースで共有できるようなローカル関数をつくる

```javascript
//セットアップを共有する

function userFormControllerSetUp() {
    this.controller = Object.create(userController);
    this.element = {};
    dom.addEventHandler = stubFn();
}

TestCase("UserFormControllerSetViewTest", {
    setUp: userFormControllerSetUp,
});

TestCase("UserFormControllerHandleSubmitTest", {
setUp: userFromControllerSetUp,

    "test should prevent event default action": function () {
        var event = { preventDefault: stubFn() };
        this.controller.handleSubmit(event);
        
        assert(event.preventDefault.called);
    }
});
```

## テストにHTMLを埋め込む

* 次に確かめるのは、モデルが入力要素に書き込まれた通りのユーザー名に更新されていること
* テストに入力要素を提供するには基本的には２つの選択肢がある
    * スタブを使い続けること
        * 例: スタブの`getElementsByTagName()`にスタブ要素を与えると、スタブ入力要素が返されるようにする
            * 好都合: テスト対象のメソッドに対する直接入力と間接入力の両方を完全にコントロール可能
            * 不都合: スタブと現実にずれが起きる危険が高い
                * ごく単純な場合でない限り、スタブを使おうとすると大量のスタブを書かなければならなくなる
    * テストに何らかのマークアップを埋め込むこと
        * テストにマークアップを埋め込めば、テストは本番環境に近くなり、スタブ作成の手作業の量も減る
        * テストケースのなかにユーザーフォームを追加すれば、テストケースはコントローラの使い方よりよくドキュメント可能 
* JsTestDriverは、テストにHTMLをインクルードする方法として２種類を提供している
    * インメモリ要素
    * 文書に追加される要素

```javascript
//テストにHTMLを埋め込む
"test should embed HTML": function () {
    /*:DOC element = <div></div> */
    
    assertEquals("div", this.element.tagName.toLowerCase());
}
```

* 等号の前の名前は、JsTestDriverが作ったDOM要素を代入するプロパティを指定している
* 番号の右には、1番のルート要素のなかに要素をネストする必要があることに注意しなければならない
* ここには複雑な構造を指定することができるが、ルートノードは1つしか存在できない
* 下記のようにすれば、文書に追加する形でテストにHTMLを組み込むことができる 

```javascript
//文書に要素を追加する

"test should append HTML to document": function () {
    /*:DOC += <div id="myDiv"></div> */
    var div = document.getElementById("myDiv");
    
    assertEquals("div", div.tagName.toLowerCase());
}
```

* 文書に追加しないほうが少し高速で、便利
    * そうすれば、JsTestDriverが自動的にテストケースのプロパティにHTMLを代入してくれる

## ユーザー名を取得

* コントローラではユーザーが最初のテキストフィールドに入力した内容をhandleSubmitが取り出す
* それをユーザー名として使うことを確かめる
* そのためには、まず、今まで使ってきた要素スタブを削除し、実際のフォームを使用する

```javascript
//setUpにユーザーフォームを埋め込む

function userFormControllerSetUp() {
    /*:DOC element = <form>
      <fieldset>
        <label for="username">Username</label>
        <input type="text" name="username" id="username">
        <input type="submit" value="Enter">
      </fieldset>
    </form> */
    
    this.controller = Object.create(userController);
    dom.addEventHandler = stubFn();
}
```

* テストを実行すると、まだ緑
* 実際のフォームを用意した
* handleSubmitがテキストフィールドを読み出していることを確かめるテストが追加可能になった 

```javascript
//handleSubmitがフィールドからユーザー名を読み出していることを確かめる

"test should set model.currentUser": function() {
    var model = {};
    var event = { preventDefault: stubFn() };
    var input = this,element.getElementsByTagName("input")[0];
    input.value = "cjno";
    this.controller.setModel(model);
    this.controller.setView(this.element);
    
    this.controller.handleSubmit(event);
    
    assertEquals("cjno", model.currentUser);
}
```

* このテストは、まだ作っていない`setModel()`を使って、スタブのモデルオブジェクトを追加する
* しかし、`setModel()`がないのでテストは不合格になる

## ソース修正

### メソッドを追加

```javascript
//setModelを追加する

/* ... */

function setModel(model){
    this.model = model;
}

tddjs.namespace("chat").userFormController = {
    setView: setView,
    setModel: setModel,
    handleSubmit: handelSubmit
};
```

* setView、`setModel()`には、インターフェイスが一貫していて予測可能になる意味がある
* ネイティブセッターを使えるようになり、明示的なメソッド呼び出しが不要になる

## ソース修正

* 次に、`handleSubmit()`が本当にテキストフィールドの現在の値を取り出しが必須
* しかし、まだ合格しない
    * さらにこの行を追加したおかげで前のテストにも不合格になる
    * それはビューを設定していないため
    
```javascript
//ユーザー名を取り出す
function handleSubmit(event) {
    event.preventDefault();

    var input = this.view.getElementsByTagName("input")[0];
    this,model.currentUser = input.value;
}
```

## ソース修正

* 要素を要求する前にビューが設定されているかどうかをチェックする
* これで前のテストは緑に戻るが、現在のテストはまだ不合格になり続ける
    * setViewが実際にビューをセットしていないため

```javascript
//this.viewにアクセスできるかどうかをチェックする
function handleSubmit(event) {
    event.preventDefault();

    if (this,view) {
        var input = this.view.getElementsByTagName("input")[0];
        this.model.currentUser = input.value;
    }
}
```

### setViewを修正

* この変更によってすべてのテストが合格する

```javascript
//ビューの参照を格納する
function setView(element) {
    /* ... */
    this.view = element;
}
```

## テストを修正

* 重複が見つかるテストケースに再び注意を向ける
* 両方のテストがスタブのイベントオブジェクトを作っている
    * このコードはsetUpに吸い上げられるし、吸い上げるべき
* 以下は、更新後のsetUpを示したもの

```javascript
//setUpのなかでイベントをスタブにする
function userFromControllerSetUp() {
    /* ... */
    
    this.event = { pregentDefault: stubFn() };
}
```

## 観測者にユーザーについての情報を通知する

* ユーザーが設定されたら、コントローラはすべての観察者にそれを通知しなければならない
* 以下は、イベントを処理し、観察者が呼び出されたことを確かめる 
* このテストに含まれている重複はすぐあとで取り除く
* テストは予想通りに不合格になる
    * * コントローラに`observe()`がないため
* この問題は、コントローラにtddjs.util.observableを継承させれば解決
* そのためには、observableの実装を`lib/observable.js`が必須

```javascript
//handleSubmitが観察者に通知を送ることを確かめる 
"test should notify opservers of username": function () {
    var input = this.element.getElementsByTagName("input")[0];
    input.value = "Bullrog";
    this.controller.setModel({});
    this.controller.setView(this.element);
    var observer = stubFn();
    
    this.controller.observe("user", observer);
    this.controller.handleSubmit(this.event);
    
    assert(observer.called);
    assertEquals("Bullrog", observer.args[0]);
}
```

## ファイルの準備

* jsTestDriver.confも更新しなければならない 
    * さらに、lib/tdd.jsは、必ずほかのモジュールの前にロードしなければならないため

```javascript
//更新後のjsTestDriver.conf

server: http://localhost:4224

load:
- lib/tdd.js
- lib/*.js
- src/*.js
- test/*.js
```

* これでコントローラの実装を更新できるようになる

## ソース修正

### コントローラが観察対象にする

```javascript
//serFormControllerを観察対象にする
(functiron () {
    var dom = tddjs.namespace("dom");
    var util = tddjs.util;
    var chat = tddjs.namespace("chat");

    /* ... */
    chat.userFormController = tddjs.extend({}, util.observable);
    chat.userFormController.setView = setView;
    chat.userFormController.handleSubmit = handleSubmit;
}());
```

* 観察者を"user"イベントを通知させられるようになった 
* これでテストに合格する

```javascript
//"user"の観察者に通知を送る
function handleSUbmit(event) {
    event.preventDefault();

    if (this.view) {
        var input = this.view.getElementsByTagName("input")[0];
        this.model.currentUser = input.value;
        this.notify("user", input.value);
    }
}
```

## テストsの修正

* しかしその前に作った２つのテストと共通するコードが多い
* 共通セットアップコードを外に出す
* 前のテストケースは、実際には新しいセットアップを必要とせず、一部はテストの邪魔になる
* このテストに固有なセットアップとする
* テストケースをthisとして共通セットアップを呼び出すコードを追加
* さらにセットアップコードを追加するようにしてある 
    * 共通セットアップを使えるようにするため
    
```javascript
//共通のセットアップコードをまとめる
TestCase("UserFormControllerHandleSubmitTest", {
    setUp: function () {
        userFormControllerSetUp.call(this);
        this.input =
            this.element.getElementsByTagname("input")[0];
        this.model = {};
        this.controller.setModel(this.model);
        this.controller.setView(this.element);
    },

    /* ... */
});
```

### 追加したクラスを取り除く

* ユーザーフォームコントローラが最後にしなければならないこと
* ユーザーの設定に聖子うしたら、"js-chat"クラス名を取り除くこと
* 以下は、クラス名が取り除かれていることを確かめるテスト

```javascript
//処理が終わったらクラス名が取り除かれていることを確かめる
"test should remove class when successful": function () {
    this.input.value = "Sharuhachi";

    this.controller.handleSubmit(this.event);

    assertEquals("", this.element.className);
}
```

## ソース修正

* テストに合格するには、ユーザー名が見つかったクラス名をリセットするコードを書く
* 以下は、そのように更新したhandleSubmit

```javascript
//ビューのクラス名をリセットする
function handleSubmit(event) {
    event.preventDefauld();

    if ( this.view) {
        var input = this.view.getElementsByTestName("input")[0];
        var username = input.value;
        this.view.className = "";
        this.model.currentUser = userName;
        this.notify("user", userName);
    }
}
```

## テストを追加

### 空のユーザー名を拒否する

* ユーザーがユーザー名を入力せずにフォームをサブミットしたらエラーを起こす
    * サーバーは空のユーザー名を認めないため
* ユーザーフォームコントローラで空のユーザー名を認ると、無関係な部分のコードでエラーが起こす
* そうなると、デバッグ非常に難しい
* 以下は、コントローラが空のユーザー名をセットしていないことを確かめるテスト

```javascript
//handleSubmitが空のユーザー名を使って通知を送らないことを確かめる
"test should not notify observers of empty username":
function () {
    var observer = stubFn();
    this.controller.observe("user", observer);

    this.controller.handleSubmit(this.event);

    assertFalse(observer.called);
}
```

## ソース修正

* テキストフィールドの値をチェックする必要がある
* ただしhandleSubmitは、ユーザー名が空なら"js-chat"というクラス名を取り除くこともできない

```javascript
//空のユーザー名を禁止する
function handleSubmit(event) {
    event.preventDefault();

    if (this.view) {
        var input = this.view.getElementsByTagName("input")[0];
        var userName = input.value;

        if(!userName) {
            return;
        }

        /* ... */
    }
}
```

