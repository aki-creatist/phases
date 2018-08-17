# コンストラクタからオブジェクトへ

## 概要

* コンストラクタが何もしなくなったコンストラクタを取り除く
* 全メソッドを直接Namespace.util.observableオブジェクトに追加する

## 備考

* 名前の先頭が大文字ではないことに注意
    * コンストラクタではなくるため
* Namespace.util.observableは、observableオブジェクトを作成可能
    * Object.createやtddjs.extendとともに使用

## テストの作成

* `beforeEach()`を追加
* `afterEach()`を追加
* 全てのspecから`new`の行を削除する
* observableをthis.observableに置き換える

```diff
  describe('ObservableTest', function () {
+     beforeEach(function () {
-         var Namespace = require('../libs/Namespace');
+         this.Namespace = require('../libs/Namespace');
-         var Observable = require('../src/Observable');
+         require('../src/Observable');
+         this.observable = this.Namespace.util.observable;
+     });
+     afterEach(function () {
+         this.observable.observers = [];
+     });
      describe('Observable.AddObserverTest', function () {
          it('test should store function', function () {
-             var observable = new Namespace.util.Observable();
          });
      });
      describe('ObservableHasObserverTest', function () {
          it('test should return true when has observer', function () {
-             var observable = new Namespace.util.Observable();
          });
  });
```

## ソース修正

```diff
  //observableオブジェクト
  var Namespace = require('../libs/Namespace');
  Namespace.namespace('util');

  (function () {
-     function Observable() {
-         this.observers = [];
-     }
      function addObserver(observer) {
          //
      }
      function hasObserver(observer) {
          //
      }
      function notifyObservers(observer) {
          //
      }
+     Namespace.namespace("util").observable = {
+         addObserver: addObserver,
+         hasObserver: hasObserver,
+         notifyObservers: notifyObservers
+     };
  }());
```

## テストの修正

* `observable`の呼び出しを`this.observable`に変更
* 但し、即時実行関数の中は例外
    * `this`とするとプロパティが見つからなくなる

```diff
    describe('Observable.AddObserverTest', function () {
        it('test should store function', function () {
-           observable.addObserver(observers[0]);
+           this.observable.addObserver(observers[0]);
-           observable.addObserver(observers[1]);
+           this.observable.addObserver(observers[1]);
-           expect(observers).toEqual(observable.observers);
+           expect(observers).toEqual(this.observable.observers);
        });
    });
〜〜中略〜〜
    describe('ObservableNotifyObserversTest', function () {
        it('test should pass through arguments', function () {
-           observable.notifyObservers("String", 1, 32);
+           this.observable.notifyObservers("String", 1, 32);
        });
        it('test should throw for uncallable oserver', function () {
+           var observable = this.observable; //ポイント
            expect(function () {
                observable.addObserver({});   //thisをつけない
            }).toThrow(new Error("observer is not function"));
        });
    });
```

## ソースの修正

### メソッドの名称変更

```diff
//一新されたobservableインターフェイス
  (function () {

-     function addObserver(observer) {
+     function observe(observer) {
      function hasObserver(observer) {
-     function notifyObservers(observer) { 
+     function notify(observer) {
    
      Namespace.namespace("util").observable = {
-         addObserver: addObserver,
+         observe: observe,
          hasObserver: hasObserver,
-         notifyObservers: notifyObservers
+         notify: notify
      };
  }());
```

## テスト修正

* ソースに合わせてメソッド名を変更する

```bash
sed -ie 's/addObserver/observer/g' spec/ObservableSpec.js
sed -ie 's/notifyObservers/notify/g' spec/ObservableSpec.js
```