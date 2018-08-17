# 任意のオブジェクトの観察

* 静的言語では、Observableクラスのサブクラスにすれば、任意のオブジェクトが観察対象になる

## 継承のねらい

* パターンのメカニズムを1か所で定義
    * 相互に関連のないオブジェクトの間でそのロジックを再利用する
* JSオブジェクトの間でコードを再利用する
    * そのためのオプションは複数あるので、継承モデルのエミュレーションに縛られない
        * Javaの真似をする必要はない
* JSのオブジェクトモデルを活用するために、Observableインターフェイスをリファクタリングする

## ニュースレターを観察対象にする

* 方法は、複数ある
* newsletterオブジェクトを作成するNewsletterコンストラクタがあるものとする

```javascript
//Observableのふるまいを共有するための方法はさまざま
var Observable = tddjs.util.Observable;
// 観察対象オブジェクトでニュースレターオブジェクトを拡張する
tddjs.extend(newsletter, new Observable());
//すべてのニュースレターオブジェクトが観察可能になるように拡張する
tddjs.extend(Newsletter.prototype, new Observable());
//ヘルパー関数を使う
tddjs.util.makeObservable(newsletter);
//コンストラクタを関数として呼び出す
Observable(newsletter);
//「静的」メソッドを使う
Observable.make(newsletter);
// オブジェクトに対して「自己修復」を指示する
// (NewsletterかObjectのプロトタイプのコードが必要)
newsletter.makeObservable();
// 古典的な継承風の方法
Newspaper.inherit(Observable);
```

* コンストラクタが提供する古典的な方法のエミュレーションから自由にする
* 以下のコードは、オブジェクトになっていることを前提としている
    * tddjs.util.observableがコンストラクタではない

```javascript
//Observableオブジェクトとふるまいを共有する

// 単一のObservableオブジェクトを作成する
var observable = Object.create(tddjs.util.observable);
// 1個のオブジェクトを拡張する
tddjs.extend(newspaper, tddjs.util.observable);
// 観察対象オブジェクトを作るコンストラクタ
function Newspaper() {
    /* ... */
}
Newspaper.prototype = Object.create(tddjs.util.observable);
//既存のプロトタイプの拡張
tddjs.extend(Newspaper.prototype, tddjs.util.observable);
```

* 単一のオブジェクトとしてObservableを実装すると、柔軟性が大幅に増す
* しかし、そこに至るためには、既存のソースをリファクタリングする
* コンストラクタを取り除く

## テストの追加

### コンストラクタを取り除く

* コンストラクタを取り除く
* まず、コンストラクタが何も仕事もしないようにObservableをリファクタリングする
* observersが初期化されていない場合にも対応可能にする必要がある
    * Observable.prototypeの全てのメソッドがobserversにアクセスするため
* これをテストするためには、メソッドごとに1ずつテストを書く
    * 他のことをする前に、対応するメソッドを呼び出す
* `notifyObservers()`は、addObserverが呼び出された後にしかテストされていない
* 観察者を追加する前にこのメソッドを呼び出せることをテストする

```diff
//addObserverの前に呼び出してもnotifyObserversは失敗しないことを確かめる
+ it('test should not fail if no observers', function () {
+     var observable = new Namespace.util.Observable();
+     expect(function (){
+         observable.notifyObservers();
+     }).not.toThrow(new Error("observer is not function"));
+ });
```

## ソース修正

* コンストラクタの内容を空にする
* テストを実行すると、1つを除きすべてのテストが失敗する

```diff
//コンストラクタを空にする
  function Observable() {
-     this.observers = [];
  }
```

### addObserver()の編集

* 更新した`addObserver()`によって、2つ以外のテストが緑になる

```diff
  //observers配列が存在しなければaddObserver内で配列を定義する
  function addObserver(observer) {
+     if (!this.observers) {
+         this.observers = [];
+     }
    /* ... */
  }
```

### hasObserver()の編集

* 緑にならない2つ
    * 他のメソッドを呼び出す前にaddObserverを呼び出さない
    * 他のメソッド: hasObserverやnotifyObserversなど
* Observers配列がなければhasObserverから直接falseを返させる

```diff
  //観察者がなければ、hasObserverにfalseを返させる
  function hasObserver(observer) {
+     if (!this.observers) {
+         return false;
+     }
      /* ... */
  }
```

### notifyObservers()の編集

* Observers配列がなければnotifyObserversから直接falseを返させる

```diff
//観察者がなければ、notifyObserversにfalseを返させる
- function notifyObservers() {
+ function notifyObservers(observer) {
+     if (!this.observers) {
+         return;
+     }
      /* ... */
  }
```
