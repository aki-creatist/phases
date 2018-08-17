# メッセージフォーム

* メッセージフォームは、ユーザーがメッセージをポストするために使うフォーム
* このフォームをテストは最初に作ったユーザーフォームコントローラのものと類似
* ビューとしてフォーム要素を必要とする
    * `handleSubmit()`を通じてフォームのサブミットイベントを処理する
* 最後にモデルオブジェクトのイベントとしてメッセージを発行し、それをサーバーに渡す 

## テストをセットアップする

* まず最初はテストケースをセットアップ
    * コントローラオブジェクトがあることを確かめる

```javascript
//messageFormControllerテストケースをセットアップする
(function () {
    var messageController = tddjs.chat.messageFormController;

    TestCase("FormControllerTestCase", {
        "test should be object": function () {
            assertObject(messageController);
        }
    });
}());
```

## ソース実装

```javascript
//メッセージフォームコントローラを定義する
(function () {
    var chat = tddjs.namespace("chat");
    chat.messageFormController = {};
}());
```

## ビューを設定する

* このコントローラはビューに"js-chat"というクラス名を追加
* コントローラにバインドされた`handleSubmit()`で"submit"イベントを観察する
    * ユーザーフォームコントローラと同様
    * 動作も全く同様

### リファクタリング：共通部分を抽出する

* ２つのコントローラが継承できるformControllerオブジェクトを抽出する
* ステップ１では、新しいオブジェクトを追加する
    * ユーザーフォームコントローラ全体のコピーを作る
    * ビューの設定とは無関係の部分を取り除いていった
    * しかし、ここではふるまいを追加したり削除したりしているわけではない
    * 単に実装の一部を移そうとしているだけ
        
```bash
touch ユーザーフォームコントローラと同様
```

```javascript
//フォームコントローラを抽出する
(function () {
    if (typeof tddjs == "undefined") {
        return;
    }

    var dom = tddjs.dom;
    var chat = tddjs.namespace("chat");

    if (!dom || !dom.addEventHandler ||
        !Function.prototype.bind) {
        return;
    }

    function setView(element) {
        element.className = "js-chat";
        var handler = this.handlerSubmit.bind(this);
        dom.addEventHandler(element, "submit", handler);
        this.view = element;
    }

    chat.formController = {
        setView: setView
    };
}());
```

* ステップ２
    * ユーザーフォームコントローラに新しいジェネリックなコントローラを使わせる
* ユーザーフォームコントローラのプロトタイプオブジェクトとして新しいコントローラを埋め込む 
* userFormController自身のsetView実装を取り除く
* userFormControllerは、formControllerからメソッドを継承
    * テストは合格する

```javascript
//userFormControllerの親を変更する
chat.userFormController = tddjs.extend(
    Object.create(chat.formController),
    util.observable
);
```

### messageFormControllerのビューを設定する

* リファクタリングは、テストも書き換えるまでは完了しない
* 元々ユーザーフォームコントローラのsetViewのために書いたテストを更新する
    * formControllerを直接テストするようにする
* ユーザーフォームコントローラが`setView()`を継承していることを確かめるテストを用意
    * ユーザーフォームコントローラがまだ動作することは確かめられる
* もとのテストを残しておいたほうがuserFormControllerのよいドキュメントが残る
    * しかし、そうするとメンテナンスのコストがかかる 
* formControllerを抽出
    * messageFormControllerが`setView()`を継承していることを確かめるテストを追加可能になる 

```javascript
// messageFormControllerがsetViewを継承していることを確かめる
(function () {
    var messageController = tddjs.chat.messageFormController;
    var formController = tddjs.chat.formController;

    TestCase("FormControllerTestCase", {
        /* ... */
        "test should inherit setView from formController":
            function() {
                assertSame(messageController.setView,
                    formController.setView);
            }
    });
}());
```

## ソース修正

* messageFormControllerの定義を書き換える 

```javascript
// formControllerを継承する
chat.messageFormController =
    Object.create(chat.formController);
```
## メッセージを発行する

* ユーザーがフォームをサブミット
    * その際、コントローラはモデルオブジェクトにメッセージを発行しなければならない
* モデルの`notify()`をスタブにしてhandleSubmitを呼び出す
    * スタブが呼び出されていることを確かめれば、メッセージが発行されていることをテスト可能
* コントローラはまだ`setModel()`を持っていない
* そこで、userFormControllerの`setModel()`をformControllerに移してこの問題を解決する

## ソースの修正

* 更新後のフォームコントローラ 
* userFormControllerのものは削除可能
    * setModelはフォームコントローラに移したため
* 壊した部分がないことを確かめるには、単純にテストを実行
* テストはすべて緑になる

```javascript
//setModelを移す
/* ... */
function setModel(model) {
    this.model = model;
}

chat.formController = {
    setView: setView,
    setmodel: setModel
};
```

## テストの追加

* コントローラが`handleSubmit()`を持つことを試す

```javascript
//コントローラがhandleSUbmit()を持つことを確かめる
"test should have handleSubmit method": function () {
    assertFunction(messageController.handleSubmit);
}
```

## ソース修正

* 以下は、空関数を追加して、テストを合格させる 
* メソッドが追加されたので、そのふるまいをテスト可能

```javascript
//空関数を追加する
function handleSUbmit(event) {}

chat.messageFormController =
    Object.create(chat.formController);
chat.messageFormController.handleSubmit = handleSubmit;
```

## テストの追加

* handleSubmitがモデルにメッセージイベントを発行することを確かめるテスト

```javascript
//コントローラがメッセージイベントを発行することを確かめる
TestCase("FormControllerHandleSubmitTest", {
    "test should publish message": function () {
        var controller = Object.create(messageController);
        var model = { notify: stubFn() };

        controller.setModel(model);
        controller.handleSubmit();

        assert(model.notify.called);
        assertEquals("message", model.notify.args[0]);
        assertObject(model.notify.args[1]);
    }
});
```

##  ソース修正

* 以下は、テストに合格するためのメソッド呼び出しを追加している 
* これですべてのテストに合格する

```javascript
//モデルのnotifyを呼び出す
function handleSubmit(event) {
    this.model.notify("message", {});
}
```

## テストの追加

* 発行されたメッセージがuserプロパティとしてcurrentUserを含んでいることを確かめる 
* ここでも、テストを追加しつつ、共通セットアップコードを`setUp()`に抽出

```javascript
//userプロパティがcurrentUserになっていることを確かめる
TestCase("FormControllerHandleSubmitTest", {
    setUp: function () {
        this.controller = Object.create(messageController);
        this.model = { notify: stubFn() };
        this.controller.setModel(this.model);
    },
    /* ... */

    "test should publish message from current user":
        function () {
            this.model.currentUser = "cjno";

            this.controller.handleSubmit();

            assertEquals("cjno", this.model.notify.args[1].user);
        }
});
```

## ソース修正

* 下記のようにすれば、テストに合格する 

```javascript
//発行されるメッセージにカレントユーザーを組み込む
function handleSubmit(event) {
    this.model.notify("message", {
        user: thi.model.currentuser
    });
}
```

## テストの追加

* 最後に残ったのは、メッセージの取り込み
* このテストにはマークアップを埋め込む必要がある
    * メッセージはメッセージフォームから取り出されるため

```javascript
//発行されたメッセージがフォームから送られれてくることを確かめる
TestCase("FormControllerHandelSubmitTest", {
    setUp: function() {
        /*:DOC element = <form>
          <fieldset>
            <input type="text" name="message" id="message">
            <input type="submit" value="Send">
          </fieldset>
        </form> */

        /* ... */
        this.controller.setView(this.element);
    },
    /* ... */

    "test should publish message from form": function () {
        var el = this.element.getElementsByTagName("input")[0];
        el.value = "What are you doing?";

        this.controller.handleSubmit();

        var actual = this.model.notify.args[1].message;
        assertEquals("What are you doing?", actual);
    }
});
```

## ソース修正

* 最初の入力要素を取り出し、その現在の値をメッセージとして渡さなければならない
* handleSubmitを更新する
* これでテストは合格するようになる
* フォームは、サーバーへのサブミットというデフォルトアクションを禁止しなければならない 
* フォームは空メッセージを送ってはいけない
* 全てのメソッドにエラー処理を追加する
* フォームがポストされたら、メッセージからイベントを生成する
    * このイベントを観察し、ローダーGIFを表示する
    * ローディングインジケータを取り除くために同じメッセージが表示される
        * その際にメッセージリストコントローラから対応するイベントを生成する

```javascript
//メッセージを取り出す
function handleSubmit(event) {
    var input = this.view.getElementsByTagName("input")[0];

    this.model.notigy("message", {
        user: this.model.currentUser,
        message: input.value
    });
}
```

## 必要な機能テストを追加

* ほとんどの機能は、汎用フォームコントローラが提供する
* 直接の依存コードは、`tddjs、formController`、`getElementsByTagname`のみ

```javascript
// messageFormControllerの機能テスト
if (typeof tddjs == "undefined" ||
    typeof document == "undefined") {
    retunr;
}

var chat = tddjs.namespace("chat");

if (!chat.formController ||
    !document.getElementByTagName) {
    return;
}

/* ... */
```