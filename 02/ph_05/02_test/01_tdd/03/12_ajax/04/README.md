# 自動的なスタブ化

* スタブ関数作成ヘルパーを抽出する
    * lib/stub.js

```javascript
function stubFn() {
    var fn = function () {
        fn.called = true;
    };
    
    fn.called = false;
    
    return fn;
}
```

* スタブヘルパーを使ってコードを書き直す

```javascript
"test should obtain an XMLHttpRequest object": function () {
    ajax.create = stubFn();
    
    ajax.get("/url");
    
    assert(ajax.create.called);
}
```

* これでajax.getがXMLHttpRequestを手に入れるのははっきりする
* ajax.getがまずすべきことは、`XMLHttpRequest`の`open()`を呼び出すこと
    * スタブ作成ヘルパーは、オブジェクトを返せなければならない
* 更新後のスタブ作成ヘルパーとopenが正しい引数で呼び出されることを確かめる新しいテストを作成する
    * `open()`が正しく使われていることをテストする

```javascript
function stubFn(returnValue){
    var fn = function(){
        fn.called = true;
        return returnValue;
        };
        
        fn.called = false;
        
        return fn;
    }
    
TestCase("GetRequestTest",{
    /* ... */
        
    "test should call open with method, url, async flag": function () {
        var actual;
        
        ajax.create = stubFn({
            open: function () {
                actual = arguments;
            }
        });
        
        var url = "/url";
        ajax.get(url);
        
        assertEquals(["GET", url, true], actual);
    }
});
```

* 現在の実装は`open()`を呼び出していない
* actualは未定義になっているので、このテストは不合格になる
* openを呼び出すような実装を書く

```javascript
function get(url) {
    /* ... */
    transport.open("GET", url, true);
}
```

* テストを実行すると、新しいテストは合格するが、もとのテストは不合格になる
    * もとのテストが不合格になる原因
        * スタブがオブジェクトを返さず、本番コードがundefined.openを呼び出そうとするため
    * 新しいテストが不合格になる原因
        * stubFn関数を使ってスタブを作っているが、引数のチェックのためにopenのスタブメソッドを手作業で作っている
        * この問題を解決するには、stubFnを改良する
        * テスト間でニセのXMLHttpRequestオブジェクトを共有する

## スタブを改良する

* 手作業で書いたスタブの`open()`を取り除く
    * 受け付けた引数を記録し、テスト内のチェックコードからアクセス可能にしている
    * [lib/stub.js](../lib/stub.js)
    * このように改良したstubFnを使うと、第2のテストはクリーンになる

```javascript
"test should call open with method, url, async flag": function () {
    var openStub = stubFn();
    ajax.create = stubFn({ open: openStub});
    var url = "/url";
    ajax.get(url);
    
    assertEquals(["GET", url, true], openStub.args);
},

"test should obtain an XMLHttpRequest object": function () {
    ajax.get("/url");
    
    assert(ajax.create.called);
},

"test should open with method, url, async flag": function () {
    var url = "/url";
    ajax.get(url);
    
    assertEquals(["GET", url, true], this.xhr.open.args);
}
```

* テストを再実行すると、すべて合格することを確かめられる
* さらに、fakeXMLHttpRequestオブジェクトにスタブを追加する
    * ajax.getのテストが大幅に単純になる
