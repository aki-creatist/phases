# 観察者の追加

* オブジェクトに観察者を追加（登録）する手段を実装する
* 手順は、最初のテストを書き、それが不合格になることを確認
* 最後にリファクタリング

## 最初のテスト

* 最初のテストは、Observableコンストラクタで観察対象オブジェクトを作る
* `Observable`の`addObserver()`を呼び出して観察者を追加する
* この処理が機能することを確かめる
    * Observableが配列内に観察者を格納
    * `観察者`が配列内の唯一の要素だということをチェックする

```bash
touch spec/ObservableSpec.js
```

```javascript
//addObserverが内部配列に観察者を追加することを確かめる
describe('Observable.AddObserverTest', function () {
    var Namespace = require('../libs/Namespace');
    var Observable = require('../src/Observable');
    it('test should store function', function () {
        var observable = new Namespace.util.Observable();
        var observer = function () {};
        observable.addObserver(observer);
        expect(observer).toBe(observable.observers[0]);
    });
});
```

### 不合格を確認

```bash
npm test
```

```text
Cannot read property 'Observable' of undefined
```

### ネームスペースの追加

* 現時点ではNamespace.utilが存在しない
* `tddjs.namespace()`を使ってこのオブジェクトを追加する
    * src/observable.js
    
```bash
touch src/observable.js
```

```javascript
var Namespace = require('../libs/Namespace');
Namespace.namespace("util"); //util名前空間を作る
```

```bash
npm test
```

```text
undefined is not a function
```

### コンストラクタとメソッドを追加

* ただちに呼び出されるクロージャ内の関数宣言を使って定義
    * 名前つき関数式の問題を回避するため

```bash
vim src/Observable.js
```

```diff
  //コンストラクタを追加する
+ function Observable() {
+     this.observers = [];
+ }
+ Namespace.util.Observable = Observable;
+ 
+ function addObserver(observer) {
+     this.observers = [observer];
+ }
+ Observable.prototype.addObserver = addObserver;
```

## リファクタリング
    
### ハードコード箇所の修正

* addObserverはテストに実装がハードコードされている点を修正する
* ハードコードを解決するため1つではなく2つの観察者を追加
    * テストは不合格になる

```bash
vim spec/ObservableSpec.js
```

```diff
  var observable = new Namespace.util.Observable();
- var observer = function () {};
+ var observers = [function () {}, function () {}];
- observable.addObserver(observer);
+ observable.addObserver(observers[0]);
+ observable.addObserver(observers[1]);
- expect(observer).toBe(observable.observers[0]);
+ expect(observers).toEqual(observable.observers);
```

### 配列を正しく追加する

* テストは、観察者として追加された関数が、積み上がると期待している
* `addObserver`では配列の`push()`を使う

```bash
vim src/Observable.js
```

```diff
  //配列を正しく追加する
  function addObserver(observer) {
-     this.observers = [observer];
+     this.observers.push(observer);
  }
```

## 残タスク

* 現状の問題点
    * 公開プロパティにアクセスしている
* 観察対象オブジェクトは、観察者がいくつあってもそれらから観察できなければならない
    * 観察対象オブジェクトが観察者をどこにどのように格納するかは、外部コードが知るべきことではない
* 特定の観察者が登録された際、観察対象オブジェクトの内部を探らずに観察対象オブジェクトをチェックできるとよい
