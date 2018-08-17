# 複数イベントの観察

* 現在のobservableは、1個の観察者リストしか管理できないという点で限界がある
* 複数のイベントを観察する
    * 観察者は受取ったデータからの推測に基づき、どのイベントが起きたのかを判断が必要
* `observable`をリファクタリングする
    * イベント名ごとに観察者グループを作れるようにする
* イベント名は、observableが自分の基準で使う任意の文字列

## ソース修正

### observeでのイベントサポート

* `observe()`は、関数引数に加えて文字列引数も受け付けられるようにする
    * イベントをサポートするため
* 新しいobserveは、第1引数としてイベントを受け付ける
* `全てのobserve()`呼び出しに第1引数として文字列を追加していく
* 全てのテストがエラーを起こす
* observeは例外を投げる
    * observeが観察者だと思っている引数が関数ではなくなっているため
* 同様にその他のメソッドについても実引数を追加する
    * `hasObserver()`
    * `notify()`

```diff
  describe('Observable.AddObserverTest', function () {
      it('test should store function', function () {
-         this.observable.observe(observers[0]);
+         this.observable.observe("event", observers[0]);
-         this.observable.observe(observers[1]);
+         this.observable.observe("event", observers[1]);
        });
    });
```

### observeに仮引数を追加する

* 実際のイベントを指定したテストを作れるようにする
* 作業が終わった後も、1つのテストが失敗し続ける

```diff
//observeに仮引数eventを追加する
- function observe(observer) {
+ function observe(event, observer) {
- function hasObserver(observer) {
+ function hasObserver(event, observer) {
- function notify(observer) {
+ function notify(event, observer) {
```

## ソース修正

### notifyでのイベントのサポート

* 現在、`notify`に渡された引数と観察者が受け取った引数を比較するテストが不合格のまま
    * 観察者に通知するイベントを指定できるように`notify`を書き換えたときのもの
    * 問題の原因
        * notifyは受け取った引数をただ横流ししていること
        * 観察者は本来受け付けるつもりでいた引数に加えてイベント名を受け取っていること
* `Array.prototype.slice`を使って第1引数以外の引数を渡す
* これでテストは合格する
* observableはイベントをサポートするためのインターフェイスを手に入れる

```diff
  //第1引数以外の引数を観察者に渡す
  function notify(event) {
      /* ... */
+     var args = Array.prototype.slice.call(arguments, 1);
      for (var i = 0, l = this.observers.length; i < l; i++) {
          try {
-             observers[i].apply(this, arguments);
+             observers[i].apply(this, args);
```
    

