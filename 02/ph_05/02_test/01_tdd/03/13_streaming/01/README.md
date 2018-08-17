# オブジェクトを定義する

## 目次

* オブジェクトを定義する
    * ポーリングを開始する
    * スタブ戦略を決める
    * モッキスト
    * スタブとモックをできる限り少なくするアプローチ
    * 選択する

## 最初のテストを記述

* test/poller_test.js
    * インターフェイスに対して期待する最初のことは、存在すること
    * 無名クロージャを使わなければならない
        * グローバル名前空間にショートカットがリークするのを避けるため

```javascript
// tddjs.ajax.pollerがオブジェクトだということを確かめる
(function () {
    var ajax = tddjs.ajax;

    TestCase("PollerTest",{
        "test should be object": function () {
            assertObject(ajax.poller);
        }
    });
}());
```

## 初期セットアップ

* src/poller.js
    * セットアップ: 無名クロージャ、名前空間のローカルな別名

```javascript
//tddjs.ajax.pollerを定義する
(function () {
    var ajax = tddjs.namespace("ajax");

    ajax.poller = {};
}());
```

## テストの追加

* オブジェクトは、`start()`を提供しなければならない
    * ポーリングを開始可能にするため

```javascript
"test should define a start method":
function () {
  assertFunction(ajax.poller.start);
},
```

## テストの追加

* 以下のテストは、urlプロパティがセットされていなければメソッドに例外を投げさせるように規定している
    * 要求を送るためには、ポーリングするURLが必要であるため

```javascript
//URLが指定されていなければstartが例外を投げることを確かめる
"test start should throw exception for missing URL":
function () {
    var poller = Object.create(ajax.poller);

    assertException(function () {
        poller.start();
    }, "TypeError)";
}
```

## 最初の実行

* `Object.create()`がないというエラーが出る

## テストに規定の追加

* test/poller_test.js
* `start()`が存在していなければならないということを規定する
* このテストは、startは関数でなければならないのにundefinedだというエラーが生成される

```javascript
//ポーラーがstart()を定義していることを確かめる
"test should define a start method":
function () {
    assertFunction(ajax.poller.start);
}
```

## start()を追加する

* 新しく追加したテストは`start()`を追加するだけで合格するようになる

```diff
 //start()を追加する
 (function () {
     var ajax = tddjs.namespace("ajax");
+    function start() {
+    }

+     ajax.poller = {
+         start: start
      };
  }());
```

## 修正後の実行

* 前のテストは依然として合格する
* テストをもう一度実行すると、存在テストは合格するが、例外を期待する最初のテストは不合格になる

## URLがなければ例外を投げるようにする

```javascript
  function start() {
*     if (!this.url) {
*         throw new TypeError("Must specify URL to poll");
*     }
  }
```

## ポーラーが依存する全ファイルをスタブ化

* ajax.requestとajax.createのどちらをスタブにすべきかを選択可能
* 今回はajax.requestをスタブ（またモック)にする
    * まずポーラーを開発する
    * 完成したらスタブ化した呼び出しを要求インターフェイスのテストの出発点として活用する

