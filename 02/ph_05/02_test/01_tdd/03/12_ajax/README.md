# ブラウザ間の違いの吸収：Ajax

## ゴール

* XMLHttpRequestのより深い知識を身に付ける
    * APIを実装する 
    * `Ajax呼び出し`の内部動作に触れる

## 概要

* XMLHttpRequestオブジェクトを使用する
    * POST要求によってバックエンドサーバーのデータを更新する
    * GET要求によって再ロードせずにページを部分的に更新する

## Requestインターフェイスのテスト駆動開発

### 開発戦略

* 最小のアサーションからボトムアップで組み立て
    * `ブラウザからXMLHttpRequestオブジェクトを取り出し`からスタート
* 単体テスト自体からはサーバーサイド要求を発行せず
* ブラウザ内のHTMLファイルからスクリプトを実行する

### 目標

* テスト内ではXMLHttpRequestを使わずにXMLHttpRequestラッパーを書く
    * 周囲から切り離し、外部からの依存を取り除く
    * スタブを多用
        * テスト中のシステムを本当に周囲から切り離すことを可能にする

## Requestインターフェイスの実装

### TODO

* XMLHttpRequestオブジェクトを作る
* `open()`を呼び出す
    * HTTP動詞、URL、要求が非同期かどうかを示すブール値を引数とする
    * ブール値: trueなら非同期とする
* オブジェクトの`onreadystatechange`ハンドラを設定する
    * 要求の処理が終わったタイミングを知るために、`readyState`プロパティを必要とする
* 必要ならデータを渡して`send()`を呼び出す

## Ajax APIの使い方

* tddjs.ajax.getは機能すると考えてよい程度になった
* 何もないところから小さなイテレーションをくり返し、ステップバイステップでtddjs.ajax.getを作ってきた
* そして基本的な道筋も見てきた
* 実際の世界でも本当に動作することを確かめる

### 統合テスト

* APIを使うためには、テストをホスティングするHTMLページが必要
* テストページは、ほかのHTMLページのために簡単な要求を送り、結果をDOMに追加する
* テストページはテストスクリプト、successful_get_test.jsを必要とする
* テストページとなるテスト用のHTML文書
    * [integration/request_test.html](integration/request_test.html)
* 統合テストスクリプト
* [integration/successful_get_test.js](integration/successful_get_test.js)
* テストスクリプトのlog関数からもわかるように、このテストは古いブラウザでも実行するつもりでいる
* 要求されている非同期にロードされるHTMLの断片は以下
    * [integration/fragment.html](integration/fragment.html)

### テストの結果

* GET要求に要求本体が含まれていない場合には、単純にnullを渡せばよい
* このテストはGetRequestTestテストケースに含まれる

```javascript
"test should pass null as argument to send": function () {
    ajax.get("/url");
    
    assertNull(this.xhr.send.args[0]); //sendが引数でつきで呼び出されることをアサートする
}
```

* テストは不合格になるので、sendに直接nullを渡すようにajax.getを書き換える 

```javascript
function get(url, options) {
    /* ... */
    transport.send(null); //sendにnullを渡す
}
```

* これでテストは緑に戻り、結合テストはFirefoxでもスムースに実行されるようになる
    * 他のブラウザでもうまく動作する
    * たとえば、Internet Explorer5以上でも、テストは成功する

### この先のトラブル

* このコードには、もう１つ問題がある
    * InternetExplorerではメモリリークを起こす
    * XMLHttpRequestオブジェクトとそのonreadystatechangeプロパティに代入された関数とが循環参照を引き起こすため
* 調べ方
    * 1000回の要求を送る別のテストページを作る
    * そしてWindowsのタスクマネージャでInternet Explorerのメモリ使用量を監視する
    * * 使用量はあっという間に上がり、かつページを離れても、メモリ使用量が下がらない
* 解決方法
    * 要求の処理が終わったら、onreadystatechangeハンドラを取り除く
    * スコープ内に要求オブジェクトを含んでいない関数をonreadystatechangeに代入する
        * `クリーン`なスコープチェーンを持っていることで知られるtddjs.noop関数を作ればよい
            * テストでも、実装外の関数は手軽に使える
        * 循環環境が切れていることをアサートする

```javascript
"test should reset onreadystatechange when complete": function () {
    this.xhr.readyState = 4;
    ajax.get("/url");
    
    this.xhr.onreadystatechange();
    
    assertSame(tddjs.noop, this.xhr.onreadystatechange); //循環環境が切れていることをアサートする
}
```

* 予想通りに、このテストは不合格になる
* 循環参照を破るように実装の修正をする

```javascript
tddjs.noop = function () {};

    (function () {
    /* ... */
    function get(url, options) {
        /* ... */
        
        transport.onreadystatechange = function () {
            if (transport.readyState == 4) {
                requestComplete(transport, options);
                transport.onreadystatechange = tddjs.noop;
            }
        };
        
        transport.send(null);
    };
    
    /* ... */
}());
```

* この2行を追加すれば、テストは再び合格する
* Internet Explorerで大量要求テストを再実行すると、メモリリークが起きなくなったことが確かめられる

### ローカル要求

* 現在の実装が抱える最後の問題点は、ローカル要求を発行できないこと
    * ローカル要求を発行してもエラーは起きないが、「何も起きない」
    * ローカルファイルシステムにはHTTPステータスコードという概念がないため
    * そのため、readyStateが4のときのステータスコードが0になってしまう
* 現在の実装はステータスコード200だけを受け入れているが、これではいずれにしても不十分
* 以下のチェックを追加し、ローカル要求をサポートする
    * スクリプトがローカルに実行されているかどうか
    * そしてステータスコードがセットされていないかどうか

```javascript
//ローカル要求でも成功ハンドラが呼び出されるようにする
"test should call success handler for local requests": function () {
    this.xhr.readyState = 4;
    this.xhr.status = 0;
    var success = stubFn();
    tddjs.isLocal = stubFn(true);
    
    ajax.get("file.html",{ success: success });
    this.xhr.onreadystatechange();
    
    assert(success.called);
}
```

* このテストの前提
    * tddjs.isLocalというヘルパーメソッドでスクリプトがローカルに実行されているかどうかをチェックすること
* setUpで参照を保存し、tearDownで復元可能になっている
    * tddjs.isLocalとしてはスタブを使っているため
* テストを合格させるためには、以下の修正が必要
    * 要求がローカルファイルに対するもので、ステータスコードがセットされていない場合には、成功コールバックを呼び出す
* 以下は更新後のレディ状態変更ハンドラ

```javascript
//ローカル要求を成功させられるようにする
function requestComplete(transport, options) {
    var status = transport.status;
    
    if(status == 200 || (tddjs.isLocal() && !status)){
        if(typeof options.success == "function"){
            options.success(transport);
        }
    }
}
```

* これでテストに合格するようになる
* ブラウザでも使えるようにするには以下を実装する
    * スクリプトがローカルに実行されているかどうかを判定するヘルパーメソッド

```javascript
//現在のURLをチェックして、要求がローカルかどうかを判断する
tddjs.isLocal = (function () {
    function isLocal() {
        return !!(window.location && 
        window.location.protocol.indexOf("file:") === 0);
    }
    
    return isLocal;
}());
```

* このヘルパーメソッドを追加して統合テストをローカルに再実行すると、HTMLの断片をロードするようになる

### ステータスのテスト

* `readyState`と`status`の異なる組合せをチェックするテストは、類似する
* まだほかの2xxステータスコードも、すべてのエラーコードもテストしていない
* fakeXMLHttpRequestオブジェクトにレディ状態の変更をフェイクするメソッドを追加する
    * 重複を取り除くため
* 以下はレディ状態を変更してonreadystatechangeハンドラを呼び出すメソッドを追加

```javascript
var fakeXMLHttpRequest = { //フェイク要求にメソッドを追加する
    open: stubFn(),
    send: stubFn(),
    
    readyStateChange: function (readyState) {
        this.readyState = readyState;
        this.onreadystatechange();
    }
};
```

* このメソッドの役割
    * 引数としてステータスコードとレディ状態を受け付ける
    * successとfailureというプロパティを持つオブジェクトを返すヘルパーメソッドを抽出可能
* 2つのプロパティは、対応するコールバックが呼びだされたかどうかを示す
* 以下は、新しいヘルパー関数
    * テスト用の要求ヘルパー
    * [test/request_test.js#6](test/request_test.js#6)
    * このヘルパーは、いくつかのテストを抽出化するもの
    * 長い名前をつけて、テストの意味がはっきりするようにしている
* 以下はこのヘルパーを使ったテストコード
    * テスト内で要求ヘルパーを使う
        * [test/request_test.js#240](test/request_test.js#240)
        * [test/request_test.js#272](test/request_test.js#272)
* 大きい変更を加えるとき、私はヘルパーにわざとバグを入れて期待通りに動作しているかどうかを確かめることがよくある
    * ヘルパー内の成功ヘルパーを設定する行をコメントアウトしたら、テストが不合格になるかどうかをチェックする
    * また、trueを返すスタブをtddjs.isLocalに代入する行をコメントアウトすると、第2のテストは不合格になるはず
    * レディ状態やステータスコードを操作するのも、テストが期待通りにふるまうかどうかを試すためによい方法

#### ステータスコードのさらなるテスト

* ステータスコードをテスト
    * 200台以外のステータスコードに対しては失敗コールバックが呼び出されるようにする
        * ただし、ローカルファイルの0と304の「変更なし」を除く
* 完成したハンドラを示している 
    * 成功コールバックと失敗コールバックの呼び分け
    * [src/request.js#12](src/request.js#12)
    * [src/request.js#20](src/request.js#20)

## POST要求を発行する

* GET要求がかなり使える状態になったところでPOST要求に移る
    * GETの実装には、まだ足りない部分が多数含まれていることに注意
        * 要求ヘッダーの設定やトランスポートの`abort()`など

### ポストのためのスペースを作る

* 現在の実装は、新しいHTTP動詞を簡単にサポート可能には作られていない
* 3つのポイントで既存の実装をリファクタリングする必要がある
    * ジェネリックな`ajax.request()`を抽出する
    * HTTP動詞を設定可能にする
    * 重複を取り除くために、`ajax.get()`を解体
    * GET要求を強制するような形でajax.requestに処理を委ねる

#### ajax.requestを抽出する

* 新しいメソッドの抽出には、ajax.getをコピーアンドペーストして、名前を変えればよい 

```javascript
//ajax.getをコピーアンドペーストしてajax.requestを作る
function request(url, options) {
    // もとのajax.get関数の本体のコピー
}

ajax.request = request;
```

#### メソッドを設定可能にする

* 次は、`ajax.request()`でオプションを設定可能にする
* これは新しい機能のため、以下のようなテストが必要

```javascript
//要求メソッドは設定可能でなければならない
function setUp() {
    this.tddjsIsLocal = tddjs.isLocal;
    this.ajaxCreate = tddjs.create;
    this.xhr= Object.create(fakeXMLHttpRwquest);
    ajax.create = stubFn(this.xhr);
}
    
function tearDown() {
    tddjs.isLocal = this.tddjsIsLocal;
    ajax.create = this.ajaxCreate;
}
    
TestCase("GetRequestTest", {
    setUp: setUp,
    tearDown: tearDown,
    /* ... */
});
    
TestCase("ReadyStateHandlerTest", {
    setUp: setUp,
    tearDown: tearDown,
    /* ... */
});
    
TestCase("RequestTest", {
    setUp: setUp,
    tearDown: tearDown,
        
    "test should use specified request method": function () {
        ajax.request("/url",{method: "POST"});
        
        assertEquals("POST",this.xhr.open.args[0]);
    }
});
```

* `ajax.request()`のために新しいテストケースを追加
    * これにより、3つのテストケースが同じsetUp、`tearDown()`を使うことになる
    * これらを無名クロージャ内の関数として抽出し、テストケース全体で共有する
* テストは、`request()`が要求メソッドとしてPOSTを使っていることをアサートしている
    * この要求メソッドの選択は、たまたまのものではない
* POSTを使うと、本物もソリューションを作る必要がある
    * POSTをハードコードするともう1つのテストが不合格になってしまうため
* 以下はajax.requestが要求メソッドを設定可能にする仕組み

```javascript
//要求メソッドを設定可能にする
function request(url, options) {
    /* ... */
    transport.open(options.method || "GET", url, true);
    /* ... */
}
```

#### ajax.getを更新する

* リファクタリングを進める
    * ajax.requestは、ajax.getと同じ仕事をする
        * 違いはajax.re-questのほうが柔軟性が高いこと
    * そこで、ajax.getは、使われている要求メソッドがGETだということを確かめるのみ
        * 他の仕事はajax.requestに任せればよい
    * ajax.getを簡単にする

```javascript
function get(url, options) {
    options = tddjs.extend({], options);
    options.method = "GET";
    ajax.request(url, options);
}
```

* methodオプションを上書きしようしてしている
    * `tddjs.extend()`を使って、変更を加える前のoptionsオブジェクトのコピーを作成
    * テストを実行すると、この部分が期待通りに動くことが確かめられる
* POST要求の基礎もできあがっている
* インターフェイスを変更したので、テストにもメンテナンスが必要
    * ほとんどのテストは、ajax.getを対象としつつ、実際にはajax.requestの内部をテストしている
    * テスト内でこのような間接処理は、一般に望ましくない
* `should define get method`(`get()`を定義しなければならない)以外は、GetRequestTestからRequestTestに移せる
* 加えなければならない変更
    * get呼び出しを直接request呼び出しに書き換える
* レディ状態変更ハンドラのテストは、すでにReadyStateHandlerTestという独自のテストケースを持っている
    * ここでも、get呼び出しをrequest呼び出しに置き換える
* 置換は、forceStatusAndReadyStateヘルパーのなかでも行う
    * テストを移動し、メソッド呼び出しを書き換え、テストを再実行する

#### ajax.postを新設する

* ajax.requestができていれば、POST要求の実装は簡単
* 今回は、POSTがどのようにふるまうかについて規定した簡単なテストから始める
    * ajax.postはajax.requestに処理を委ねるはず

```javascript
TestCase("PostRequestTest", {
    setUp: function () {
        this.ajaxRequest = ajax.request;
    },
    
    tearDown: function () {
        ajax.request = this.ajaxRequest;
    },
    
    "test should call request with POST method": function () {
        ajax.request = stubFn();
    
        ajax.post("/url");
    
        assertEquals("POST", ajax.request.args[1].method);
    }
});
```

* 実装は ajax.postはmethodとしてPOSTを指定してajax.requestに処理を委ねる

```javascript
function post(url, options){
    options = tddjs.extend({}, options);
    
    options.method = "POST";
    ajax.request(url, options);
}

ajax.post = post;
```

* テストを実行すると、この実装が新しく追加された要件を解決していること確かめられる
* 次に、先に進む前に重複を探す
* `get()`と`post()`は明らかに非常によく似ている
* そこで、ヘルパーメソッドを抽出してもよい
    * しかし、関数呼び出しを1つ増やしても、2つのメソッドの2行を節約できるだけ
    * ここでは間接化のレベルを増やすだけの意味は感じられない

### データを送信する

* POST要求に何らかの意味を持たせるためには、POST要求を使ってデータを送る必要がある
* サーバーにデータを送るには、以下2つのことを行う
    * encodeURIかencodeURIComponentを使ってデータをエンコード
        * どちらを使うかは、データをどのように受信するかによって決まる
    * Content-Typeヘッダーを設定する

#### データの準備

* 文字列のエンコードは独自インターフェイスに分離する
* [src/url_params.js](src/url_params.js)
* このメソッドは、配列やその他の種類のデータをエンコードできるように拡張可能
* 機能検出を使ってないときに限り定義 
    * encodeURICom-ponent関数は、あることが保証されている関数ではないため

## テストの追加

#### ajax.requestでデータをエンコードする

* POST要求では、データをエンコードして、`send()`に引数としてエンコードされたデータを渡す
* まずデータがエンコードされていることを確かめるテストを書く

```javascript
function setUp() {
    this.tddjsUrlParams = tddjs.util.urlParams;
    /* ... */
}

function tearDown(){
    tddjs.util.urlParams = this.tddjsUrlParams;
    /* ... */
}

TestCase("RequestTest", {
    /* ... */
    
    "test should encode data": function () {
        tddjs.util.urlParams = stubFn();
        var object = { field1: "13", field2: "Lots of data!"}
        
        ajax.request("/url", {data: object, method: "POST"});
        
        assertSame(object, tddjs.util.urlParams.args[0]);
    }
});
```

* データがあればエンコードする

```javascript
function request(url, options) {
    /* ... */
    options = tddjs.extend({}, options);
    options.data = tddjs.util.urlParams(options.data)
    /* ... */
}
```

* urlParamsはdataが存在するかどうかをチェックする必要はない
    * 存在しない引数に対応可能に設計されているため
* おそらく機能テストを追加すべきだということに注意
    * エンコードインターフェイスはajaxインターフェイスから切り離されているため

#### エンコードされたデータの送信

* 次にデータを送信する
* POST要求ではデータはsendで送るようにする

```javascript
//POST要求のためにデータが送信されることを確かめる
"test should send data with send() for POST":function () {
    var object = { field1: "$13", field2: "Lots of data!"};
    var expected = tddjs.util.urlParams(object);
    
    ajax.request("/url", { data: object, method: "POST"});
    
    assertEquals(expected, this.xhr.send.args[0]);
}
```

* このテストは不合格になる
    * `send()`にnullを与えているため
* また、`tddjs.util.urlParamsが正しい値を提供するはずだ`を前提することにも注意
    * tddjs.util.urlParamsは、正しい値を提供することを確かめられる自分用のテストを持つ必要がある
* テスト内でtddjs.util.urlParamsをそのまま使う
* テストに合格させるためには、ajax.requestにデータ処理を追加する必要がある

```javascript
//データ処理の最初の試み
function request(url, options) {
    /* ... */
    options = tddjs.extend({}, options);
    options.data = tddjs.util.urlParams(options.data);
    var data = null;
    if (options.method == "POST") {
    data = options.data;
    }

    /* ... */

    transport.send(data);
};
```

* ajax.requestをクリーンアップするにはデータ処理部分を別の関数にするというリファクタリングする

```javascript
//データ処理関数を外に出す
function setData(options) {
    if (options.method == "POST"){
        options.data = tddjs.util.urlParams(options.data);
    }else{
        options.data = null;
    }
}

function request(url, options) {
    /* ... */
    options = tddjs.extend({}, options);
    setData(options);
    
    /* ... */
    
    transport.send(options.data);
};
```

#### GET要求によるデータの送信

* 要求ヘッダーの設定に移る前に、GET要求でもデータを送れるようにしておかなければならない
* GET要求では、データはURLにエンコードされる
    * データは`send()`に渡されるのではない
* 以下は、この動作を規定するテスト

```javascript
//GET要求がデータを送れることをテストする
"test should send data on URL for GET": function() {
    var url = "/url";
    var object = { field1: "$13", field2: "Lots of data!"};
    var expected = url + "?" + tddjs.util.urlParams(object);
    
    ajax.request(url, { data: object, method: "GET"});
    
    assertEquals(expected, this.xhr.open.args[1]);
}
```

* このテストを追加したら、データ処理を書き換える
    * GET、POSTのどちらでも、データをエンコードする必要がある
    * しかし、GET要求の場合、データはURLに組み込まれ、`send()`には依然としてnullを渡す

```javascript
//GET要求にデータを追加する
function setData(options) {
    if (options.data){
        options.data = tddjs.util.urlParams(options.data);
        
        if(options.method == "GET"){
            options.url += "?" + options.data;
            options.data = null;
        }
    } else {
        options.data = null;
    }
}
    
function request(url, options) {
    /* ... */
    options = tddjs.extend({}, options);
    options.url = url;
    setData(options);
    /* ... */
    
    transport.open(options.method || "GET", options.url, true);
    /* ... */
    transport.send(options.data);
};
```

* データ処理には、URLをoptionsオブジェクトに追加し、以前と同様にoptionsオブジェクトをsetDataに渡している
    * データを組み込んでURLを書き換える処理が含まれる場合があるため
* URLにすでにクエリー文字列が含まれている場合には、失敗してしまう

### 要求ヘッダーを設定する

* データを渡すために必須の最後の処理は、要求ヘッダーの設定
    * ヘッダーは、`setRequestHea-der(name, value)`で設定可能
    * テストするためには、ヘッダーを記録できるようにfakeXMLHttpRequestに修正を加える
        * テストからヘッダーを参照可能にする
* 以下は、この目的のために使えるオブジェクトのアップデート版
    * フェイクの`setRequestHeader()`を追加する
    * [lib/fake_xhr.js#7](lib/fake_xhr.js#7)

## ソース修正

### Request APIを見直す

* 要求ヘッダー処理実装後のajax.request
    * `tddjs.ajax,request`の「最終」バージョン
        * [src/request.js](src/request.js)
    * optionsオブジェクトを受け付けるヘルパーがいくつか見つかる
        * このオブジェクトは、実際には要求の状態を表現するもの
        * この時点ではrequestという名前であってもよい
    * ヘルパーは要求オブジェクトのヘルパーメソッドになる

### 要求APIの発展方向の1つ

* ajax.getとajax.postの実装する
* `request.create`は、唯一の引数としてトランスポートを取る
    * つまり、request.createにトランスポートを取得させない
    * 最大の依存対象であるトランスポートを与えるようにしている
* さらに、このメソッドは、設定すれば要求として送れる要求オブジェクトを返すようになる
    * こうすると、基本APIはラップしているXMLHttpRequestオブジェクトに近づいてくる
    * それでもデフォルトヘッダーの設定、データの前処理、ブラウザ間の不一致への対処といったロジックを含んだものになる
        * そのようなオブジェクトは、JSONRequestオブジェクトなど、もっと特化した要求に拡張することも簡単
        * そのようなオブジェクトは、たとえばパースしたJSONをコールバックに渡すなどの方法で、応答も前処理可能
* コードカバレッジはほとんど100%に近いが、テストのなかにはいくつかの穴が残っている
    * テストを増やさなければならないケース
        * メソッドが誤った引数を受け取った場合
        * その他の境界条件が必要になった場合

```javascript
(function () {
    /* ... */
    
    function setRequestOptions(request, options) {
        options = tddjs.extend({}, options);
        request.success = options.success;
        request.failure = options.failure;
        request.headers(options.headers || {});
        request.data(options.data);
    }
    
    function get(url, options) {
        var request = ajax.request.create(ajax.create());
        setRequestOptions(request, options);
        request.method("GET");
        
        request.send(url);
    };
    
    ajax.get = get;
    
    function post(url, options){
        var request = ajax.request.create(ajax.create());
        setRequestOptions(request, options);
        request.method("POST");
        
        request.send(url);
    }
    
    ajax.post = post;
}());
```

## まとめ

* APIを開発するためのエンジンとしてテストを活用
    * このAPIは、以下に対処している
        * オブジェクトの作成方法の違い
        * メモリリーク
        * バグのある`send()`などのクロスブラウザの問題点
* バグが見つかるたびに、APIがその問題を適切に処理可能
* スタブの利用
    * スタブ関数、オブジェクトが手作業で簡単に作れる
        * すぐにそのようなことをするとコードの重複が増えすぎる
    * そこで、スタブを助ける簡単な関数を書く
* tddjs.ajax.requestと関連コードを書く過程で、本番コードとテストの両方をリファクタリング
    * コードは問題点をよりよく理解できた後に、いつでも改良可能

