# オブジェクトの調査

* オブジェクトを定義する前に、どのオブジェクトが使えるかを調べる
* こうすると、呼び出し時のオーバーヘッドtddjs.ajax.createもない
* クライアントコードはtddjs.ajax.createの有無をチェックする
    * ブラウザがXMLHttpRequestをサポートしているかどうかのテストになる
* あらかじめサポートされているかどうかをチェックする

```javascript
(function (){
    var xhr;
    var ajax = tddjs.namespace("ajax");
    var options = [/* ... */]; // 以前と同じ
    for (var i = 0, L = options.length; i < l; i++){
        try{
            xhr = options[i]();
            ajax.create = options[i];
            break;
        } catch (e) {}
    }
}());
```

* この実装なら、try/catchはロード時に実行されるだけ
* ajax.createは、作成に成功していれば、正しい関数を直接呼び出す

## より強力な機能検出

* URLとHTTP動詞を使ってサーバーに要求を発行できるインターフェイスを作る
* 可能なら成功時、失敗時のコールバックを指定可能にするという究極の目標をコードにしてRequest APIを作る
* まず、以下のようにGET要求から始める
    * tddjs.ajax.getが定義されていることを確かめる

```javascript
TestCase("GetRequestTest", {
    "test should define get method": function () {
        assertFunction(tddjs.ajax.get);
    }
});
```

* `get()`があるかどうかをチェックすることからスタートする
* 予想されるように、メソッドがないため、このテストは不合格になる
* `src/request.js`にて、メソッドを定義

```javascript
tddjs.namespace("ajax").get = function () {};
```
## URLを要件とする

* `get()`はURLを受け付けられなければならない
    * getはURLを要件とする必要がある
    * URLが必須とされていることをテストする
        * [test/request_test.js#48](../test/request_test.js#48)
    * まだ例外を投げていないので、このメソッドはそのために不合格になる
* URLが文字列でなければ例外を投げることでテストは合格する

```javascript
tddjs.namespace("ajax").get = function (url) {
    if (typeof url != "string") {
        throw new TypeError("URL should be string");
    }
};
```

* 現時点では名前空間をいちいち指定している
    * テストを無名クロージャでラップし、変数にajax名前空間を代入する
    * これにより、ローカルスコープにajax名前空間を`インポート`可能
    * テストにajax名前空間を`インポート`する

```javascript
(function () {
    var ajax = tddjs.ajax; //テストにajax名前空間を`インポート`する
    
    TestCase("GetRequestTest",{
        "test should define get method": function (){
            assertFunction(ajax.get);
        },
        
        "test should throw error without url": function () {
            assertException(function () {
            ajax.get();
            },"TypeError");
        }
    });
}());
```

* 同じことをソースファイルにも適用可能
    * 無名クロージャによって得られるスコープを名前つき関数にも使える
    * ソースにajax名前空間を`インポート`する

```javascript
(function (){
    var ajax = tddjs.namespace("ajax");
    
    function get(url) {
        if (typeof url != "string") {
            throw new TypeError("URL should be string");
        }
    }
    
    ajax.get = get;
}());
```