# エラー処理

## 概要

* エラー処理を追加する

## 前提条件

* Java APIとJSには差異がある
    * `Java API`: 登録可能な観察者はObserverIFを実装するオブジェクトのみ
    * `JS`: 登録可能な観察者は任意の関数(ただの値を処理は不可)
    
## 背景

* 現時点のテストが想定外の入力に対して未対応
* 現在は`addObserver`は引数としてどのようなタイプの値でも受け付ける

## ゴール

* クライアントの操作に誤りがあるときの正しい動作も保証する

### 例外処理の実装

* 呼び出せない観察者を追加しようとする
* Observableが例外を投げるものと想定する
* 全てのテストが全て失敗するようになる
    * 全てのaddObserver呼び出しに対して例外を投げるため

```diff
  //呼び出せない引数を指定すると例外が投げられることを確かめる
+ it('test should throw for uncallable observer', function () {
+     var observable = new Namespace.util.Observable();
+     expect(function (){
+         observable.addObserver({}); //無効となることを期待する観察者を追加する
+     }).toThrow(new Error("observer is not function"));
+ });
```

#### addObserverの事前条件

* 入力が呼び出し可能であること

#### 事後条件

* 観察者が観察対象に追加されること
* 観察対象がnotifyObsevers呼び出し時に呼び出されること

#### ゴール

* 今回は実装をフェイク不可
* addObserverがリストに追加する前に、観察者が本当に関数かチェックする
* `観察者`が全て呼び出し可能であることを保証する
    * 観察者: `Observable`が`addObserver`によって追加された観察者

```diff
  //呼び出せない観察者を追加したときに例外をなげる
  function addObserver(observer) {
+     if (typeof observer != "function") {
+         throw new TypeError("observer is not function");
+     }
      this.observers.push(observer);
  }
```

## テストの追加

* 観察者が例外を投げると、notifyObserversはエラーを起こす可能性が残っている
* 関数の中のどれかが例外を投げても、全ての観察者が呼び出されることを確かめる
* `notifyObservers()`は第2の観察者は呼び出せず、エラーになる
    * `追加に成功した観察者をいつでも全て呼び出す`という約束を守れないため
* しかし、Observableのドキュメントされていない機能を前提している
    * つまり、観察者が追加された順序で呼び出される

```diff
//クラッシュした観察者があってもnotifyObserversが最後まで処理をすることを確かめる
+ it('test should notify all even when some fail', function () {
+     var observable = new Namespace.util.Observable();
+     var observer1 = function () { throw new Error("Oops"); };
+     var observer2 = function () { observer2.called = true; };
+     observable.addObserver(observer1);
+     observable.addObserver(observer2);
+     observable.notifyObservers();
+     expect(observer2.called).toBeTruthy();
+ });
```

```bash
npm test
```

```text
- Error: Oops #第1の観察者を呼び出したところでエラーを起こす
```

### 問題の修正

* notifyObserversを最悪の条件にも対応可能にする
* エラーを正しく処理するのは観察者の仕事
    * 観察対象は、クラッシュする観察者から自分を守れればよい
* 適切なエラー処理を与えてObservableの堅牢性を改善
* このモジュールは、まともな入力を与えられれば必ず処理を行うことを保証可能にする
* また、観察者が要件を満たさなくても、修復して他の観察者を呼び出し可能にする
* 現在は正しく動作している
    * observersリストの実装のために配列を使っているため

```diff
  //クラッシュした観察者が投げた例外をキャッチする
  for (var i = 0, l = this.observers.length; i < l; i++) {
+     try {
          this.observers[i].apply(this, arguments);
+     } catch (e) {
+         //
+     }
  }
```

## 呼び出し順の保証

* 現在、リストの内部での実装方法を変えると、テストがエラーを起こす危険がある
* 想定できる解決方法は以下の2通り
    * 呼び出し順を前提条件としないようにテストをリファクタリング
    * 呼び出し順を前提条件とするテストを単純に追加
        * 呼び出し順を機能としてドキュメントする
* Observableが呼び出し順に関するふるまいを保ち続けるテストを追加する
    * 呼び出し順は意味のある機能と考えられるため
* 実装がすでにobserversとして配列を使っているので、このテストは成功する

```diff
//呼び出し順を機能として保証する
+ it('test should call observers in the order they were added', function () {
+     var observable = new Namespace.util.Observable();
+     var calls = [];
+     var observer1 = function () { calls.push(observer1); };
+     var observer2 = function () { calls.push(observer2); };
+     observable.addObserver(observer1);
+     observable.addObserver(observer2);
+     observable.notifyObservers();
+     expect(observer1).toBe(calls[0]);
+     expect(observer2).toBe(calls[1]);
+ });
```


