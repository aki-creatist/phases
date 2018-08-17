# 観察者をチェックする

* ObservableにhasObserverという新しいメソッドを使用
* `addObserver`を実装したときの混乱を取り除く

## 新しいテストの作成

* `hasObserver()`の望ましいふるまいを規定
* このテストは、`hasObserver()`が存在しないため不合格になる

```bash
vim spec/ObservableSpec.js
```

```diff
  //既存の観察者があるときにはhasObserverがtrueを返すことを確かめる
+ describe('ObservableHasObserverTest', function () {
+     var Namespace = require('../libs/Namespace');
+     var Observable = require('../src/Observable');
+     it('test should return true when has observer', function () {
+         var observable = new Namespace.util.Observable();
+         var observer = function () {};
+         observable.addObserver(observer);
+         expect(observable.hasObserver(observer)).toBeTruthy();
+     });
+ });
```

### テストを合格させる

* 現在のテストを合格させられるソースで最も単純
* テストは要件であり、現在のところ、`hasObserver`がtrueを返しさえすればよい

```bash
vim src/Observable.js
```

```diff
  //hasObserverからの応答をハードコードする
+ function hasObserver(observer) {
+     return true;
+ }

+ Observable.prototype.hasObserver = hasObserver;
```

### 新しいテストを追加

* 観察者が存在しないときにはhasObserverがfalseを返すものと想定する
* このテストは、hasObserverがtrueを返しているため、不合格になる
* addObserverに最初に渡されたthis.observers配列がオブジェクトを含んでいるかどうかをチェック
    * 観察者が登録されているかどうかを確認する

```bash
vim  spec/ObservableSpec.js
```

```diff
  //観察者がいないときにhasObserverがfalseを返すことを確かめる
+ it('test should return false when no observers', function () {
+     var observable = new Namespace.util.Observable();
+     var observer = function () {};
+     observable.addObserver(observer);
+     expect(observable.hasObserver(function () {})).toBeFalsy();
+ });
```

* `Array.prototype.indexOf()`は、配列に要素が含まれていなければ負数を返す
    * 戻り値が0以上かどうかをチェックすれば、観察者がいるかどうかがわかる

```bash
vim src/Observable.js
```

```diff
+ //観察者がいるかどうかを実際にチェックする
+ function hasObserver(observer) {
+     return this.observers.indexOf(observer) >= 0;
+ }
```

### ブラウザ間の非互換性を解決する

* indexOf呼び出しではなく、ループを使ってhasObserverを実装する
    * Observableを自己完結的なままにしておくため

```bash
vim src/Observable.js
```

```diff
  //手作業で配列をループで処理する
- return this.observers.indexOf(observer) >= 0;
+ for (var i = 0, l = this.observers.length; i < l; i++) {
+     if(this.observers[i] == observer) {
+         return true;
+     }
+ }
+ return false;
```

## リファクタリング

* 最初のテストとの間の違いは2つ
    * 第1のテストは、Observableオブジェクトの中のobservers配列に直接アクセスしている
    * 最初のテストは、2つの観察者を追加し、両方が追加されることを確かめている
* これら2つのテストを1つにまとめる
* Observableに追加されたすべての観察者が本当に追加されていることを確かめる

```bash
vim  spec/ObservableSpec.js
```

```diff
  //重複するテストを取り除く
+ it('test should return true when has observer', function () {
+     var observable = new Namespace.util.Observable();
+     var observers = [function () {}, function () {}];
+     observable.addObserver(observers[0]);
+     observable.addObserver(observers[1]);
+     expect(observable.hasObserver(observers[0])).toBeTruthy();
+     expect(observable.hasObserver(observers[1])).toBeTruthy();
+ });
```
