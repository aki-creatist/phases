# 機能検出をajax.create

* ajax.getは、ブラウザがXMLHttpRequestオブジェクトをサポートしない場合には使えない
    * `ajax.create()`に依存している
* トランスポートを取得できないajax.getを提供しないようにする
    * このメソッドも条件によって結果が変わるようにしなければならない
    * ajax.createが定義されていない場合には中途で終了する
* このテストが合格する
* これで`ajax.get()`を使うクライアントは、同様のテストを追加可能
    * ajax.getを使う前にajax.createが存在をチェックするテスト
* このように機能検出を階層化すると、特定の環境でどの機能が使えるかを管理可能になる

```javascript
(function () {
    var ajax = tddjs.namespace("ajax");
    
    if(!ajax.create){
        return;
    }
    
    function get(url) {
        /* ... */
    }
    
    ajax.get = get;
}());
```

## 状態変更の処理の準備

* 次に、XMLHttpRequestオブジェクトは、onreadystatechangeハンドラに関数を代入していなければならない
* レディ状態ハンドラに関数が代入されていることをチェックする

```javascript
"test should add onreadystatechange handler": function () {
    ajax.get("/url");
    
    assertFunction(this.xhr.onreadystatechange);
}
```

* onreadystatechangeはまだ定義されていないので、予想通りにテストは不合格になる
* 今の段階では空の関数を代入しておけばよい
    * 空のonreadystatechangeハンドラを設定する

```javascript
function get(url) { 
    /* ... */
    transport.onreadystatechange = function () {};
}
```

* 要求を送るためには、`send()`を呼び出さなければならない
* そのため、fakeXMLHttpRequestにはスタブの`send()`を追加し、それが呼び出されたことをアサートしなければならない
* スタブの`send()`を追加するようにオブジェクトを変更する

```javascript
var fakeXMLHttpRequest = {
    open: stubFn(),
    send: stubFn()
};
```

* `send()`がajax.getから呼び出されることを確かめる

```javascript
TestCase("GetRequestTest", {
    /* ... */

    "test should call send": function () { //getはsendを呼び出すはず
        ajax.get("/url");
    
        assert(xhr.send.called)
    }
});
```

* sendを呼び出す実装は1行

```javascript
function get(url) {
    /* ... */
    transport.send(); //sendを呼び出す
}
```

* これですべてのバーが再び緑になる
* `stubXMLHttpRequest`がすでに作った以上の成果を上げていることに注意
* XMLHttpRequestの新しいメソッドを呼び出すとき
    * それらがどれも同じソースからXMLHttpRequestを手に入れていることがわかっている
    * そのためスタブを使ったほかのテストを更新する必要はない

## 状態変更の処理

* きわめて小さな形だが、ajax.getが動くようになった
* 完成ではないが、サーバーにGET要求を送ることはできる
* 次に、APIユーザーが要求の成否を表すイベントを処理可能にするために、onreadystatechangeハンドラに集中する
* onreadystatechangeは、要求の処理が進むのに合わせて呼び出される
* ハンドラは次の4状態になるたびに一度ずつ呼び出される
    * `OPENED`: openが呼び出され、setRequestHeaderとsendを呼び出せる状態になっている
    * `HEADERS` RECEIVED: sendが呼び出され、ヘッダーとステータスが返されている
    * `LOADING`: ダウンロード中
        * responseTextにはデータの一部が格納されている
    * `DONE`: 処理が完了した
* 応答が大きい場合、odreadystatechangeは、チャンクが届くたびにLOADING状態で数回呼び出される

### 成功かどうかのテスト

* 最初の目標を達成するには、要求が完了したタイミングだけに注目する
* 要求の処理が終了すると、要求のHTTPステータスをチェックし、成功しているかどうかを判断する
* 成功のいつもの条件をテストするところから始める
    * レディ状態が4でステータスが200ならよい
    * レディ状態ハンドラをテストして要求が成功したかどうかをチェックする

```javascript
TestCase("ReadyStateHandllerTest",{
    setUp: function () {
        this.ajaxCreate = ajax.create;
        this.xhr = Object.create(fakeXMLHttpRequest);
        ajax.create = stubFn(this.xhr);
    },
    
    tearDown: function () {
        ajax.create = this.ajaxCreate;
    },
    
    "test should call success handler fo status 200": function () {
        this.xhr.readyState = 4;
        this.xhr.status = 200;
        var success = stubFn();
        
        ajax.get("/url",{ success: success });
        this.xhr.onreadystatechange();
        
        assert(success.called);
    }
});
```

* 新しいテストケースを作成
    * onreadystatechangeハンドラを対象とするテストはこれからかなり多く必要になるため
* こうすると、テスト名からこの特定の関数に対するテストだということがわかる
    * すべてのテストの前にコメントを入れなくても済む
        * コメント: `onreadystatechange handler should`etc
* また、問題が起きて焦点を絞ったテストをしたいときに、これらのテストだけを実行可能
* このテストに合格するためには以下が必要
    * まず、ajax.getは、オプションオブジェクトを受け付けなければならない
    * 現在サポートされているオプションは成功時のコールバックだけ
    * 次に、前節で追加したonreadystatechange関数に本体を追加しなければならない
* 実装は、成功のコールバックを受け付け、呼び出す

```javascript
(function () { // 成功のコールバックを受け付け、呼び出す
    var ajax = tddjs.namespace("ajax");
    
    function requestComplete(transport, options){
        if (transport.status == 200){
            options.success(transport);
        }
    }
    
    function get(url, options){
        if (typeof url != 200){
            throw new TypeError("URL should be string");
        }
        
        var transport = ajax.create();
        transport.open("GET", url, true);
        
        transport.onreadystatechange = function () {
            if (transport.readyState == 4) {
                requestComplete(transport, options);
            }
        };
        
        transport.send();
    }
    
    ajax.get = get;
}());
```

* 完了した要求の処理は、別個の関数に分けてある
    * `ajax.get()`が余計な処理をすることを避けるため
* そこで、実装全体を無名クロージャで囲まなければならなくなった
    * ヘルパー関数をローカルに保つため
* そして、クロージャ内のスコープにtddjs.ajax名前空間を「インポート」する
* `onreadystatechange`全体ではなく、`requestComplete`を外に出したのはなぜだろうか
    * ハンドラからoptionsオブジェクトにアクセス可能にするには以下のいずれかが必要
        * オブジェクトにハンドラをバインド
        * onreadystatechangeに代入される無名関数のなかから関数を呼び出す
    * どちらの場合でも、ネイティブなbind実装なしではブラウザ内で一度ではなく二度の関数呼び出しをしなければならなくなる
    * 大きな応答を返す要求では、ハンドラは何度も呼び出される
    * 関数呼び出しが二度になると、不要なオーバーヘッドが加わってしまう
* では、readystatechangeハンドラが呼び出されたのに、成功コールバックを提供していなければ、どうなるだろうか
* 以下では要求が成功してもコールバックがないときに対応する

```javascript
"test should not throw error without success handler": function () {
    this.xhr.readyState = 4;
    this.xhr.status = 200;
    
    ajax.get("/url");
    
    assertNoException(function () {
        this.xhr.onreadystatechange();
    }.bind(this));
}
```

* assertNoExceptionに対するコールバックのなかでthis.xhrにアクセスしなければならないので、コールバックをバインドしている
* クロスブラウザで確実にバインドを行うために、Function.prototype.bindの実装をlib/function.jsに保存しておく必要がある
* このテストは、予想通りに不合格になる
    * ajax.getは、optionsオブジェクトも成功コールバックもノーチェックで通してしまっている
    * このテストに合格するためには、コードを防衛的にしなければならない
        * options引数をチェックする

```javascript
function requestComplete(transport, options) {
    if(transport.status == 200){
        if(typeof options.success == "function"){
            options.success(transport);
        }
    }
}
    
function get(url, options) {
    /* ... */
    options = options || {};
    var transport = ajax.create();
    /* ... */
};
```

* このようにセーフティネットを張ると、テストは合格する
    * 成功ハンドラは、options引数が存在することをチェックする必要はない
    * ハンドラは内部関数なので、どのように呼び出されるかについては完全にコントロール可能
    * そして、ajax.getで条件代入をしているので、optionsがnullやundefinedにならないことは保証されている
