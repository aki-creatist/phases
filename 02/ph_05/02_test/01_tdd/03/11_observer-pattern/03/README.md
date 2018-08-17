# 観察者に通知する

## 前提条件

* 観察者を追加され手織り、存在チェック可能

## 背景

* 変化が起きた際、観察者に通知を送れなければObservableは役に立たない
* Javaとの並行性にこだわるなら、新しいメソッドは`notifyObservers`という名前になる

## 概要

* ライブラリに新たなメソッドを追加する

## 観察者が確実に呼び出されるようにする

* notifyObserversの役割は`全ての観察者を呼び出す`こと
    * 事後に観察者が本当に呼び出されたことを確かめる手段が必要
    
## テストの追加

### notifyObserversの最初のテスト

* 呼び出される関数のプロパティを設定する
* プロパティが設定されているかをチェックする
    * 関数が呼び出されたことを確認可能になる

```bash
vim  spec/ObservableSpec.js
```

```diff
+ //notifyObserversがすべての観察者を呼び出していることを確かめる
+ describe('ObservableNotifyObserversTest', function () {
+     var Namespace = require('../libs/Namespace');
+     var Observable = require('../src/Observable');
+     it('test should call all observers', function () {
+         var observable = new Namespace.util.Observable();
+         var observer1 = function () { observer1.called = true; };
+         var observer2 = function () { observer2.called = true; };
+         observable.addObserver(observer1);
+         observable.addObserver(observer2);
+         observable.notifyObservers();
+         expect(observer1.called).toBeTruthy();
+         expect(observer2.called).toBeTruthy();
+     });
+ });
```

## ソース修正

* observers配列をループで処理して、個々の関数を呼び出す

```bash
vim src/Observable.js
```

```diff
//すべての観察者を呼び出す
+ function notifyObservers() {
+     for (var i = 0, l = this.observers.length; i < l; i++) {
+         this.observers[i]();
+     }
+ }

+ Observable.prototype.notifyObservers = notifyObservers;
```

## テストの追加

### 引数を渡す

* 現在、観察者は呼び出されているが、何もデータを与えられていない
* 観察者は`何かが起きたこと`はわかる
* 観察者は`何が起きたのか`はわからない
* notifyObserversが任意の個数の引数を取得可能にする
    * それらの引数を各観察者に渡す
* 受け取った引数をテスト内のローカル変数に代入
* 渡した引数と受取った引数を比較する
* notifyObserversの中で引数に触れる

```bash
vim  spec/ObservableSpec.js
```

```diff
  //notifyObserversに渡された引数が観察者に渡されることを確かめる
+ it('test should pass through arguments', function () {
+     var observable = new Namespace.util.Observable();
+     var actual;
+     observable.addObserver(function (){
+         actual = [].slice.call(arguments);
+     });
+     observable.notifyObservers("String", 1, 32);
+     expect(["String", 1, 32]).toEqual(actual);
+ });
```

## ソース修正

* 観察者を呼び出しに`apply()`を使用
    * applyの第1引数として`this`を指定していることに注意
    * これは、観察者が観察対象をthisとして呼び出されることを意味する
    
```bash
vim src/Observable.js
```

```diff
//applyを使ってnotifyObserversに渡された引数を渡す
  for (var i = 0, l = this.observers.length; i < l; i++) {
-     this.observers[i]();
+     this.observers[i].apply(this, arguments);
  }
```



