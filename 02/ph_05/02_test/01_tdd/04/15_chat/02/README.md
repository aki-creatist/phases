# クラスを追加する

* 実際のふるまいについての最初のテスト
    * `js-chat`というクラス名がDOM要素に追加されることを確かめる
* Object.create実装を`lib/object.js`に作成
    * クロスブラウザでこのテストを同様に合格させるため
* このテストでは、DOM要素が含まれていない
    * しかし、assertClassNameアサーションを使用
    * スペースで区切られた値の中に引数の文字列が含まれているかどうかだけをチェック
* elementオブジェクトは、スタブオブジェクト
    * 本物のDOM要素は不要
    * ここでチェックしたいのは、何らかのプロパティが代入されていること
        * テスト中の実際のDOMイベントリスナーを追加は不要
        * 単純にaddEventHandlerをスタブに置き換える

```javascript
//ビューのクラス名が設定されていることを確かめる
TestCase("UserFormControllerSetViewTest", {
    "test should add js-chat class": function () {
        var controller = Object.create(userController);
        var element = {};
        
        controller.setView(element);
        
        assertClassName("js-chat", element); //要素が指定されたクラス名を持つかどうかをチェックする
    }
});
```

## ソース修正

* クラス名を代入するコードを追加する
* 前提ユースケース
    * すでにクラス名を持っている要素以外を使用しても構わない
    * クラス名は`js-chat`を使用してもよい
    * クラス名をオーバーライドしてもよい

```javascript
//クラス名を追加する
function setView(element) {
    element.className = "js-chat"; //クラス名をオーバーライド
}
```

