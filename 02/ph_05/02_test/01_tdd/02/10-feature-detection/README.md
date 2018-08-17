# 機能検出

* 堅牢なクロスブラウザスクリプトを書くためのアプローチ

## ブラウザの推測

* ブラウザの推測方法は、２通り
    * ユーザーエージェントによる推測
    * オブジェクトの検出

### ブラウザ推測の現状

* ブラウザの推測は、新しいバージョンのブラウザがリリースされると、簡単に条件が変わってしまう
* 新しいブラウザがリリースされるたびにそのコードをアップデートしなければならない
* ブラウザ推測に依存しているライブラリを使っていると、メンテナンスが難しい
    * さらにアップデートを行うと、下位互換性が保証されない

## よい目的でのオブジェクトの検出

* 機能検出の本質
    * ブラウザは、ある機能を使う前にその機能が使用可能か確認可能
    * 管理されたセットアップのもとでその機能が信頼できるものかどうかをテスト

### 存在するかどうかのテスト

* 以下は、オブジェクトの検出を使っている
    * 特定のブラウザだけに存在することがわかっているオブジェクトの有無をテストするのではない
    * 実際に使おうとしているオブジェクトの有無をテストしている

```javascript
//機能検出を使ってイベントの処理方法を変える
function addEventHandler(element, type, listener) {
    if(element.addEventListener) {
        element.addEventListener(type, listener, false);
    } else if (element,attachEvent && listener.call) {
        element.attachEvent("on" + type, function () {
            return listener.call(element, window.event);
        });
    } else {
        // イベントプロパティにグレードダウンするか処理を中止するか
    }
}
```

### 型チェック

* 以下は、オブジェクトを使う前に使えるかどうかをチェックしている
* addEventListenerプロパテイが存在するからといって、それが期待通りに動作するという保証はない
* このプロパテイが呼び出せるものかどうかをチェックすれば、テストはより正確になる

```javascript
//機能の型のチェック
function addEventHandler(ekement, type, listener) {
    if (typeof element.addEventListener == "function") {
        element.addEventListener(type, listener, false);
    } else if (typeof element.attachEvent == "function" && typeof listener.call == "function") {
        element.attachEvent("on" + type, function () {
        return listener.call(element, window.event);
    });
    } else {
        // イベントプロパティにグレードダウンするか処理を中止するか
    }
}
```

### ネイティブオブジェクトとホストオブジェクト

* ネイティブオブジェクト
    * ECMAScript仕様でセマンティクスを説明できるオブジェクトのこと
    * ネイティブオブジェクトのふるまいは一般に予測可能
    * 型チェックのような限定的な機能テストを実施すれば、価値のある情報が得られる
* ホストオブジェクト
    * 環境が提供しているものの、ECMAScript仕様では記述されていないオブジェクト
    * たとえば、ブラウザのDOM実装は、ホストオブジェクトだけで構成されている

```javascript
//Internet Explorerでのtypeofとホストオブジェクト
// ver.8 を含むInternet Explorerでtrueになる
assertEquals("object", typeof documents.attachEvent);
```

* フレンドリではないホストオブジェクトのふるまい
    * [test/host_object_test.js](test/host_object_test.js)
* ホストオブジェクトが呼び出し可能かどうかをチェックする
    * [src/tdd.js#173](src/tdd.js#173)
    * このヘルパーを使うと、クロスブラウザイベントハンドラは、以下のように改良可能
        * addEventHandlerの機能検出コードの改良
        * [src/events.js](src/events.js)

### サンプル実行テスト

* オブジェクトが存在し、型も正しいことをテストしても、それが正しく使えるという保証にはならない場合がある
* 以前作ったstrftimeは、`String.prototype.replace()`が第2引数として関数を受け付けることが動作の重要な前提条件になっていた
* 古いブラウザは必ずしもその機能をサポートしていない
* 以下は、コントロールされた形でreplaceを使ってみて、そのテストに合格したときに限りメソッドを定義するというstrftimeの実装
* [src/strftime.js](src/strftime.js)
* `Date.prototype.strftime()`は、正しくサポートできるブラウザのみで提供されるようになる
* 以下に示すように、機能テストは実際にその機能を使う前に実行しなければならない

```javascript
//strftimeの使い方
if (typeof Date.prototype.strftime == "function") {
    // Date.prototype.strftimeを信頼してよい
}

// ...または
if (typeof someDate.strftime == "function") {
    /* ... */
}
```

## DOMイベントが使用可能かどうかの判定方法

* 一部のブラウザでは、この方法を機能させるためには、テスト用の要素が必要
    * [src/tdd.js#191](src/tdd.js#191)

## CSSプロパティがサポートされているかどうかを判定方法

* サポートされているCSSプロパティごとに、要素のstyleオブジェクトは文字列プロパティを提供している
    * その値はキャメルケースの名前になっている
* 以下は、現在の環境がCSS3のbox-shadowプロパティをサポートするかどうかをチェックする
    * [src/tdd.js#221](src/tdd.js#221)

```javascript
// box-shadowをサポートしているブラウザならtrueになる
assert(tddjs.isCSSPropertySupported("boxShadow"));
```

* 以下は動作の例

```javascript
//サポートされているスタイルプロパティを取得する
// "MozBoxShadow" in Firefox
// "WebkitBoxShadow" in Safari
// undefined in Internet Explorer
getStyleProperty("boxShadow");
```

## クロスブラウザイベントハンドラ

* 機能検出を使ってスクリプトを堅牢にする
    * tddjs名前空間にクロスブラウザの`addEventHandler`関数を追加する
    * このメソッドを機能させるためには、`addEventListener`か`attachEvent`が必要
    * 機能検出に基づくクロスブラウザイベント処理
    * [src/tdd.js#239](src/tdd.js#239)
* 実装例
    * [src/tdd.js#280](src/tdd.js#280)

## 機能検出の使い方

* 機能検出は、クロスブラウザスクリプトを書くための強力なツール
* 機能検出を使えば、古いもの、新しいもの、将来のものを含め、非常に広い範囲のブラウザを対象として多くの機能を実装できる

### 検出できない機能

* 特定ブラウザの問題の解決方法がどのブラウザにも悪影響を及ぼさない場合
    * 問題を検出するよりも、すべてのブラウザに解決策を適用するほうが簡単
    * ただし、当然のようにそうする前に、パフォーマンスに与える影響を考えるようにするべき

## まとめ

* 特定のブラウザについて、とてもメンテナンスしきれないような知識を必要とするのは避けるべき
* ブラウザの推測に変わる方法として、機能検出、すなわちコードの自動テストを行う
* ネイティブ/ホストオブジェクトとそのメソッドのテスト
* サポートされているイベントやCSSプロパティのテスト、さらにはサポートされているCSS値のテスト
* 機能検出を完全にマスターするには、知識や経験だけでなく、判断力が必要