# 最初のテスト

* XMLHttpRequestオブジェクトが存在することを確かめるテスト
    * 使用するプロパティは、`open`、`send()`
* tddjs.ajax名前空間がないので、このテストは不合格になる
* ajax_test.js

```javascript
TestCase("AjaxCreateTest", { // XMLHttpRequestが存在することを確かめる
    "test should return XMLHttpRequest object": function () {
        var xhr = tddjs.ajax.create();
        assertNumber(xhr.readyState);
        assert(tddjs.isHostMethod(xhr, "open"));
        assert(tddjs.isHostMethod(xhr, "send"));
        //要求ヘッダーを設定するために、以下のsetRequestHeader()が必要
        assert(tddjs.isHostMethod(xhr, "setRequestHeader"));
    }
});
```

* src/ajax.jsを取り込む名前空間宣言を行う
    * 前提条件: `tddjs.namespace()`がlib/tdd.jsに含まれていること
        * [lib/tdd.js#4](../lib/tdd.js#4)

```javascript
tddjs.namespace("ajax"); //ajax名前空間を作る
```

* テストは不合格になる
* 名前空間を作っても、`create()`がないため
* createを実装するためには、背景の知識が必要

## XMLHttpRequestについての基礎知識

* XMLHttpRequestは、２通りの作成方法がある
    * 事実上の標準となっている作成方法
    * IEのActiveXObjectを使った作成方法を示したもの
    * ActiveXオブジェクトの識別子`Microsoft.XMLHTTP`は`ActiveX ProgId`と呼ばれているもの
        * Microsoft.XMLHTTPは、古いバージョンのWindowsに搭載されていたIE5.xを対象としている

```javascript
// 標準案/ほとんどのブラウザで動作
var request = new XMLHttpRequest();

// IE 5、5.5、6 (IE7でも可)
try{
    var request = new ActiveXObject("Microsoft.XMLHTTP");
} catch (e) {
    alert("ActiveX is disabled");
}
```

## tddjs.ajax.createを実装する

XMLHttpRequestオブジェクトを作る

```javascript
tddjs.namespace("ajax").create = function () {
    var options = [
        function () {
            return new ActiveXObject("Microsoft.XMLHTTP");
        },
        
        function () {
            return new XMLHttpRequest();
        }
    ];
    
    for(var i = 0, l = options.length; i < l; i++){
        try{
            return options[i]();
        } catch (e) {}
    }
    
    return null;
};
```

* テストを実行すると、緑になる
* リファクタリングで改善できる重複、その他の問題点を探す
    * コードのなかに自明な重複は含まれていない、実行時の無駄な重複がある
        * オブジェクトが作成されるたびに、適切なオブジェクトを探すtry/catchが実行されている
