# 機能テスト

## 前提条件

* ユーザーフォームコントローラは、うまくいったときに通る道を十分整備できている
* 適切な機能テストを追加するためには、依存コードとして本物のイベント実装が必要

## 概要

* コントローラをサポートできるかどうかを判定するための機能テストを追加する
* コントローラが、定義時にイベント実装を必要とする

## ソース実装

* 機能テストを含むコントローラ
    * イベントユーティリティをtdd.jsに保存しなければ、テストに合格しない

```bash
touch lib/event.js
```

```javascript
//userFormControllerの機能テスト
(function () {
    if (typeof tddjs == "undefined" ||
        typeof document == "undefined") {
        return;
    }

    var dom = tddjs.dom;
    var util = tddjs.util;
    var chat = tddjs.namespace("chat");

    if (!dom || !dom.addEventHandler || !util ||
        !util.observable || !Object.create ||
        !document.getElementsByTagName ||
        !Function.prototype.bind) {
        return;
    }

    /* ... */
}());
```

* addEventHandlerの参照を保存してからスタブに置き換える
* テストスイート全体を上書きしていることになる
    * tearDownでもとのハンドラを復元するわけではないため
* しかし、この場合はそれが問題になることはない
    * どのテストも実際のDOMイベントハンドラを登録するわけではないため
* コントローラは、依存コードにアクセスできなければ定義されない