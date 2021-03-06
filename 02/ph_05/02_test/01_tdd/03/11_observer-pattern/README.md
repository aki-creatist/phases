# Observerパターン

## 環境のセットアップ

* [観察者の追加](01)
* [観察者をチェックする](02)
* [観察者に通知する](03)
* [エラー処理](04)
* [任意のオブジェクトの観察](05)
* [コンストラクタからオブジェクトへ](06)
* [複数イベントの観察](07)

## テストの追加

### イベントの機能を規定する

* イベントがどのように機能するかを規定する
    * このテストは、2つの異なるイベントに2つの観察者を登録する
    * そのイベントに登録された観察者だけが呼び出される
        * 片方のイベントに対する`notify`だけを呼び出すため
* テストは不合格になる
    * observableがすべての観察者に通知を送ってしまうため

```javascript
//登録された観察者だけが呼び出されることを確かめる
it('test should notify relevant observers only', function () {
    var calls = [];
    this.observable.observe("event", function (){
        calls.push("event");
    });
    this.observable.observe("other", function (){
        calls.push("other");
    });
    this.observable.notify("other");
    expect(calls).toEqual(["other"]);
});
```

## ソース修正

* この問題を簡単に修正できる方法はない
* `observable`配列をオブジェクトに置き換える
* 新しいオブジェクトは、キーがイベント名になっているプロパティに観察者配列を格納する
    * 全てのメソッドでオブジェクトと配列を条件に基づいた初期化は不要
* イベントに正しく対応している配列を受け取る内部ヘルパー関数を追加する
    * 必要に応じて配列とオブジェクトの両方を作る
* 配列ではなくオブジェクトに観察者を格納する
    * [src/observable.js](src/observable.js)

## まとめ

* 動作するもっとも単純なことからスタート
* 本番コードとテストの両方が洗練されるのは、リファクタリングを通じてされる
