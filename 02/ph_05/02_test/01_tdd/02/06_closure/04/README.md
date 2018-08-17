# 名前空間

* グローバルスコープに入り込まないようにするため方法の１つ
    * JSはネイティブな名前空間を持っていない

## オブジェクトを名前空間として使うには

* グローバルスコープで1個のオブジェクトを定義する
* その他の関数、オブジェクトを**そのオブジェクトのプロパテイとして**実装する

## 例: tddjs名前空間内にライトボックスオブジェクトを実装

* ライトボックスは`tddjs.ui`にまとめる
* Ajax機能は`tddjs.ajax`にまとめる

```javascript
//オブジェクトを名前空間として使う
var tddjs = {
    lightbox: { /* ... */ },
    anchorLightbox: function (anchor, options) {
        /* ... */
    }
};
```

## 名前空間を実装する

* 例として`tddjsオブジェクト.namespace関数`を実装する
    * またがって共有される再利用可能コードに名前空間を与える
* 名前空閲の各レベルをループで処理し、存在しないオブジェクトを作る独自関数を実装する

### テストの実装

* [test/namespace_test.js](test/namespace_test.js)

## 概要

* src/tdd.js
* namespaceは、グローバルtddjsオブジェクトのメソッドとして実装
    * その中の名前空間を管理する
* 関数宣言を使ってnamespaceを定義し、クロージャがローカルスコープを作ることを利用

```javascript
//実装全体をクロージャでラップし、tddjsは独自名前空間内で完全にサンドボックス化
var tddjs = (function () {    //即時実行クロージャを組み合わせ、プロパテイがグローバルオブジェクトにリークすることを確実に防ぐ
    function namespace(string) {  //namespace関数
        
        var object = this;
        var levels = string.split(".");

        for (var i = 0, l = levels.length; i < l; i++) {
            if (typeof object[levels[i]] == "undefined") {
                object[levels[i]] = {};
            }

            object = object[levels[i]];
        }
        //1. オブジェクトにobjectを返し、namespaceプロパティにそれを代入する
        return object;
    }

    return { //戻り値のオブジェクトリテラルをグローバルtddjsオブジェクトに代入
        namespace: namespace // 1から返された値をnamespaceに代入
    };
}());
```

* namespace関数は、thisから名前空間の解決を始める
    * こうすると、tddjs以外のオブジェクトの名前空間を作るときに、この関数を借りやすくなる

### 他のオブジェクト内に名前空間を作る例

* メソッドを借りて他のオブジェクトの中に名前空間を作る
* 他のオブジェクトからメソッドを呼び出すときにも変更されない

```javascript
//カスタム名前空間の作成
"test namespacing inside othew objects":
function () {
    var custom = { namespace: tddjs.namespace };
    custom.namespace("dom.event");
    
    assertObject(custom.dom.event);
    assertUndefined(tddjs.dom);
}
```

## 名前をインポートする

* JSはネイティブの名前空間を持っていない
    * つまり`import`キーワードがない
        * `import`: ローカルスコープに一連のオブジェクトをインポートする
* `ローカル変数にネストされたオブジェクトを代入する`だけでそれらを`インポート`可能
    * **クロージャにはローカルスコープがある**ため

```javascript
//ローカル変数を使って名前空間をインポートする
(function () {
    var request = tddjs.ajax.request;
    
    request(/* ... */);
    
    /* ... */
}());
```

## 名前をインポートする長所

* グローバル変数の場合とは異なり、ローカル変数の識別子は安全にミニファイ可能
    * つまり、ローカルエリアスを使うと、本番でのスクリプトサイズも削減可能

## メソッドのローカルエイリアスを作る際の注意

* メソッドがそのthisオブジェクトに依存している場合
    * ローカルインポートすると、暗黙のバインドを切ってしまう
    * `名前空間のインポート`＝**実質的にオブジェクトをクロージャ内にキャッシュ**すること
    * なので、インポートされたオブジェクトのモック、スタブを作ろ際も問題が起きる

## まとめ

* 名前空間は、グローバル名前空間を汚さずに、コードを構造化可能
* パフォーマンスは落ちるが、DOM操作などと比べれば、名前空間による影響は小さい

