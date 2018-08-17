# 最初の要求

## テストの追加

* XMLHttpRequestの`open()`が期待されるURLを指定して呼び出されたことをアサートする
    * `start()`がポーリングをスタートさせることを規定するため

```javascript
// ポーラーが要求を発行していることを確かめる
setUp: function () {
    this.ajaxCreate = ajax.create;
    this.xhr = Object.create(fakeXMLHttpRequest);
    ajax.create = stubFn(this.xhr); //ajax.createをスタブ化
},

tearDown: function () {
    ajax.create = this.ajaxCreate;
},

/* ... */

"test start should make XHR request with URL": function () {
    var poller = Object.create(ajax.poller);
    poller.url = "/url";

    poller.start();

    assert(this.xhr.open.called);
    assertEquals(poller.url, this.xhrl.open.args[1]);
}
```

## start()の実装は単純にする

```javascript
// 要求を発行する
function start() {
    if (!this.url) {
        throw new TypeError("Must provide URL property");
    }

    ajax.request(this.url);
}
```

* テストがajax.requestを使うことを指定しないことに注意
    * そのため、どのような方法で要求を発行しても構わない
        * 但し、ajax.createが提供してくるトランスポートを使っているうちに限る
* 例: 要求インターフェイスのリファクタリングは、ポーラーテストに手を触れずに進める

## テスト実施

* すべて合格する
    * しかし、テストは本来のあるべき姿ではない
    * トランスポートの`open()`が呼び出されたことがわかっていても、必ずしも要求が送られたとは限らない

## send()も呼び出されたことをチェックする

* アサーションを追加したほうがよい

```javascript
//要求は送られているはず
"test start should make XHR request with URL": function () {
    var poller = Object.create(ajax.poller);
    poller.url = "/url";

    poller.start();

    var expectedArgs = ["GET", poller.url, true];
    var actualArgs = [].slice.call(this.xhr.open.args);
    assert(this.xhr.open.called);
    assertEquals(expectedArgs, actualArgs);
    assert(this.xhr.send.called);
}
```

## complete コールバック

### 要求を定期的に発行する

* test/request_test.js
* 前の要求の処理が完了したら、遅延要求を発行する
* そのため、成功コールバックと失敗コールバックをラップしなければならない

### 3つの新しいテストを追加

* completeコールバック関数を追加
    * 要求の処理が完了したときに処理の成否にかかわらず呼び出される
* 3つの新しいテストを追加

```javascript
// completeコールバックを規定する
function forceStatusAndReadyState (xhr, status, rs) {
    var success = stubFn();
    var failure = stubFn();
    var complete = stubFn();

    ajax.get("/url", {
        success: success,
        failure: failure,
        complete: complete
    });

    xhr.complete(status, re);

    return{
        success: success.called,
        failure: failure.called,
        complete: complete.called
    };
}

TestCase("ReadyStateHandlerTest", {
    /* ... */

    //completeコールバックが成功/失敗/ローカル要求のために呼び出されていることを確かめる
    "test should call complete handler for status 200":
        /* ... */
    "test should call complete handler for status 400":
        /* ... */
    "test should call complete handler for status 0":
        /* ... */
});
```

### 実施

* 3つのテストは予想通りにすべて不合格
    * completeコールバックはどこからも呼び出されていないため

### 呼び出しは簡単に追加

```javascript
//completeコールバックを呼び出す
function requestComplete(options){
    var transport = options.transport;

    if(isSuccess(transport)){
        if(typeof options.success == "function"){
            options.success(transport);
        }
    } else {
        if(typeof options.failure == "function"){
            options.failure(transport);
        }
    }

    if(typeof options.complete == "function"){
        options.complete(transport);
    }
}
```

* 要求の処理が完了したとき、ポーラーは次の要求をスケジューリングしなければならない
* あらかじめスケジューリングには、タイマーを使う
* 新しい要求は、スケジューリングを行った同じコールバックを最終的に呼び出す
    * また次の要求がスケジューリングされ、setIntervalを使わなくても継続的にポーリングが続く
* しかし、この機能を実装する前に、タイマーのテスト方法を理解する必要がある

### タイマーをテストする

* テスト内でタイマー関数をスタブにする
    * windowオブジェクトのsetTimeoutプロパティをスタブ化する
* 通常のスタブアプローチでは、タイマーをスタブに置き換え、スタブが想定通りに使われたことをアサートする
    * スタブを使えばテストが短くなるが、クロックを使えばテストから得られる情報が増える
    * ここではクロックを使ってポーラーをテストし、違いを学ぶ
* jsUnitMockTimeout.jsをインストール
* ダウンロードしたファイルをプロジェクトのlibディレクトリにコピー

```javascript
//setTimeoutをスタブ化する
(function () {
    TestCase("ExampleTestCase",{
        setUp: function(){
            this.setTimeout = window.setTimeout; //一度の実行のためには、setTimeoutを使う
        },

        tearDown: function(){
            window.setTimeout = this.setTimeout;
        },

        "test timer example":function(){
            window.setTimeout = stubFn(); //windowオブジェクトのsetTimeoutプロパティをスタブ化
            // Setup test

            assert(window.setTimeout.called);
        }
    });
}());
```

### ポーラーが新しい要求をスケジューリングすることをテストする

#### 事前準備

* URLを指定したポーラーを作る
* ポーラーを起動する
* 最初の要求が完了するところをシミュレートする
* `send()`を再びスタブに置き換える
* 指定したミリ秒だけ時間を先に進める
* `send()`が二度目に呼び出されたことをアサートする
    * 時間を先に進めているときに呼び出しは発生しているはず 
* 要求の処理を完了させるために、fakeXMLHttpRequestにさらにヘルパーメソッドを追加する

```javascript
//要求の処理を完了させるヘルパーメソッドを追加する
var fakeXMLHttpRequest = {
    /* ... */

    complete: function(){ //HTTPステータスコードを200にしてレディ状態4でonreadystatechangeハンドラを呼び出す
        this.status = 200;
        this.readyStateChange(4);
    }
};
```

#### 要件に従うテストを追加

```javascript
//要求の処理が完了したときに新しい要求がスケジューリングされることを確かめる
"test should schedule new request when complete":
function () {
    var poller = Object.create(ajax.poller);
    poller.url = "/url";

    poller.start();
    this.xhr.complete();
    this.xhr.send = stubFn();
    Clock.tick(1000);

    assert(this.xhr.send.called); //成功するためには、ポーラーは最初の要求の処理が終わったら非同期に新しい要求を発行しなければならない
}
```

* ポーラーが使っている`ajax.request()`は、要求ごとに新しい`XMLHttpRequest`オブジェクトを作る
* ajax.createスタブは要求ごとに一度ずつ呼び出される
    * いつも1つのテストの中の同じインスタンスを返す
* そのためフェイクインスタンスの`send()`を再定義するだけで十分

#### 非同期に新しい要求を発行する

* completeコールバックのなかで新しい要求をスケジューリングする必要がある

```diff
//新しい要求をスケジューリングする
  function start() {
      if (!this.url) {
          throw new TypeError("Must specify URL to poll");
      }

+     var poller = this;

-     ajax.request(this.url);
+     ajax.request(this.url,{
+         complete: function () {
+             setTimeout(function () {
+                 poller.start();
+             },
+         }
+     });
  }
```

### リファクタリング

* すべてのテストがポーラーオブジェクトを必要とし、ポーラーの作成のために複数行が必要なことがわかっている
+ オブジェクトのセットアップコードを`setUp()`に移す 

```diff
//ポーラーセットアップコードを移す
  setUp: function () {
      /* ... */
*     this.poller = Object.create(ajax.poller);
+     this.poller.url = "/url";
  }
```

* 1000ミリ秒ちょうどまで待つテストに変更する
* すでにsetTimeoutを正しく実装しているので、このテストはすぐに合格する

```diff
//ディレイを1000ミリ秒ちょうどにする
"test should not make new request util 1000ms passed":
  function () {
-     var poller = Object.create(ajax.poller);
-     poller.url = "/url";

      this.poller.start();
      this.xhr.complete();
      this.xhr.send = stubFn();

-     Clock.tick(1000);            
+     Clock.tick(999);

      assertFalse(this.xhr.send.called);
}
```

### 設定可能なインターバル

#### ポーリングのインターバルを設定可能にする

* ポーラーインターフェイスはインターバル情報を下記のように受け付ける
    * `最初の要求の処理完了から350ミリ秒後に新しい要求が発行される`の1つのふるまいをテスト

```javascript
//要求のインターバルが設定できることを確かめる
TestCase("PollerTest",{
    /* ... */

    tearDown: function(){
        ajax.create = this.ajaxCreate;
        Clock.reset(); //Clock.reset呼び出しを追加し、テストが相互干渉しないようにしている
    },

    /* ... */

    "test should configure request interval":
        function(){
            this.poller.interval = 350;
            this.poller.start();
            this.xhr.complete();
            this.xhr.send = stubFn();

            Clock.tick(349); //349ミリ秒までやり過ごし
            assertFalse(this.xhr.send.called); //新しい要求が発行されていないことをアサートしてから

            Clock.tick(1); //最後の1ミリ秒を進め、
            assert(this.xhr.send.called); //要求が発行されたことをアサート
        }
});
```

## ソース修正

* テストが規定しているふるまい
    * 数値が指定されている場合はpoller.intervalを設定
    * そうでなければデフォルトの1000ミリ秒を使う
* もう一度テストを実行すると成功する

```diff
//インターバルを設定可能にする
  function start() {
      /* ... */
+     var interval = 1000;

      if (typeof this.interval == "number") {
          interval = this.interval;
      }

      ajax.request(this.url, {
          complete: function () {
              setTimeout(function () {
                  poller.start();
-             },
+             },interval);
          }
      });
  }
```

### ヘッダーとコールバックを設定可能にする

* オブジェクトのユーザーが要求ヘッダーを設定
* コールバックを追加可能にしなければ、ポーラーは完成とは言えない
* 以下のテストは、fakeXMLHttpRequestに渡されたヘッダーを検査する
* このテストは、2つのニセのヘッダーを設定
    * それらがトランスポートに設定されていることを単純にアサートする
    
```javascript
"test should pass headers to request": function () {
    this.poller.headers = {
        "Header-One":"1",
        "Header-Two":"2"
    };

    this.poller.start();

    var actual = this.xhr.headers;
    var expected = this.poller.headers;
    assertEquals(expected["Header-One"],
        actual["Header-One"]);
    assertEquals(expected["Header-Two"],
        actual["Header-Two"]);
}
```

## ソース修正

* 次は、すべてのコールバックも一緒に渡されるようにしたい
* まず成功コールバックから

```javascript
//ヘッダーを渡す
function start() {
    /* ... */
    ajax.request(this.url, {
        complete: function () {
            setTimeout(function () {
                poller.start();
            },interval);
        },

        headers: poller.headers
    });
}
```

## テストの追加

* コールバックが渡されたかどうかをテストする
    * 先ほどfakeXMLHttpRequestオブジェクトに追加した`complete()`が使える
* completeは要求の処理成功をシミュレートしており、成功コールバックを呼び出すはずである

```javascript
//成功コールバックが呼び出されるはず
"test should pass success callback": function() {
    this.poller.success = stubFn();
    
    this.poller.start();
    this.xhr.complete();
    
    assert(this.poller.success.called);
}
```

* このテストが規定している内容は、ヘッダーを渡したときと同じような1行を追加するだけで実装可能

```javascript
//成功コールバックを渡す
ajax.request(this.url, {
    /* ... */
    
    headers: poller.headers,
    success: poller.success
});
```

* 失敗コールバックを同様にチェックする
    * `fakeXMLHttpRequest`オブジェクトを拡張が必須
* 具体的には、すでに実装されている要求成功だけでなく、要求失敗もシミュレート可能にする必要がある
* 以下に示すように、completeがオプションのHTTPステータスコード引数を受け付けられるようにする

```javascript
//任意のステータスで要求の処理を完了可能にする
complete: function (status) {
this.status = status || 200;
this.readyStateChange(4);
}
```

* 200をデフォルトステータスとして残しておくと、機能を拡張可能
    * 今までのテストをアップデートしたり壊す必要がない
* 失敗コールバックが渡されることを必要とする同様のテスト

```javascript
//テスト - 失敗コールバックが呼び出されるはず
"test should pass failure callback":function(){
    this.poller.failure = stubFn();
    
    this.poller.start();
    this.xhr.complete(400);
    
    assert(this.poller.failure.called);
}
```

## ソース修正

* 失敗コールバックを渡す実装を書く

```javascript
//実装は - 失敗コールバック
ajax.request(this.url, {
    /* ... */
    
    headers: poller.headers,
    success: poller.success,
    failure: poller.failure
});
```

* 最後に、completeコールバックがクライアントからも使えることをチェックしておかなければならない
* 要求の処理が完了したときにcompleteが呼び出されることのテストは、今までの2つのテストと同じ
* しかし、実装は今までのものとは少し異なる

```javascript
//completeコールバックがあれば呼び出す
ajax.request(this.url, {
    complete: function () {
        setTimeout(function () {
            poller.start();
        }, interval);

        if(typeof poller.complete == "function"){
            poller.complete();
        }
    },

    /* ... */
});
```

## 1行コード

* この時点で、ポーラーインターフェイスは使える状態になっている
    * 足りない機能で目立つものは、要求のタイムアウトと`stop()`がないこと
    * その一因は`ajax.request`の実装にタイムアウトとabortがないこと

### 1行インターフェイスを追加する

* `ajax.request`、`ajax.get`、`ajax.post`を受け入れるための1行インターフェイスを追加する
* このインターフェイスは、ajax.pollerオブジェクトを使う
    * つまり、そのふるまいはほとんどポーラーのスタブ実装で規定可能
* 最初のテストの要件
    * ajax.pollerを継承するオブジェクトがObject.createで作成されること
    * 作成時に`start()`が呼び出されること
* このテストケースは、いくつかのメソッドをスタブに置き換える
* 最後に復元するという通常のセットアップ処理を行う
* 新しいオブジェクトが作成され、その`start()`が呼び出されたことを確かめる

```javascript
//start()が呼び出されるはず
TestCase("PollTest",{
    setUp: function () {
        this.request = ajax.request;
        this.create = Object.create;
        ajax.request = stubFn();
    },

    tearDown: function () {
        ajax.request = this.request;
        Object.create = this.create;
    },

    "test should call start on poller object": function () {
        var poller = { start: stubFn() };
        Object.create = stubFn(poller);

        ajax.poll("/url");

        assert(poller.start.called);
    }
});
```

## ソース修正

```javascript
//ポーラーを作って起動する
function poll(url, option) {
    var poller = Object.create(ajax.poller);
    poller.start();
}

ajax.poll = poll;
```

## テストの追加

* 次に、以下は、ポーラーのurlプロパティが設定されていることを確かめる
* このテストのためには、ポーラーオブジェクトの参照が必要
* 参照を返すメソッドが必要だということになる 

```javascript
// urlプロパティが設定されていることを確かめる
"test should set url property on poller object": function(){
    var poller = ajax.poll("/url");
    
    assertSame("/url", poller.url);
}
```

## ソースの修正

* このテストに対応する実装には、2行のコードを追加しなければならない 

```javascript
//URLを設定する
function poll(url, options) {
    var poller = Object.create(ajax.poller);
    poller.url = url;
    poller.start();

    return poller;
}
```

* 残されたテスト
    * 単純にポーラーのヘッダー、コールバック、インターバルが適切に設定されていることをチェックする
* 以下は、ajax.pollの最終バージョン

```javascript
//ajax.pollの最終バージョン
function poll(url, options) {
    var poller = Object.create(ajax.poller);
    poller.url = url;
    options = options || {};
    poller.headers = options.headers;
    poller.success = options.success;
    poller.failure = options.failure;
    poller.complete = options.complete;
    poller.interval = options.interval;
    poller.start();

    return poller;
}

ajax.poll = poll;
```