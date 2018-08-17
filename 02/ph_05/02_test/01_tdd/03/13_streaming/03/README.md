# ロングポーリングサポートの実装

* 要求の間に長いタイムアウトを入れずにポーラーにロングポーリングサポートを追加する
* ロングポーリングの目的は、レイテンシを低くすること
    * そのため、少なくともタイムアウトは取り除く

## Dateのスタブ化

* この機能をテストするためには、Dateコンストラクタをフェイクしなければならない
* パフォーマンス計測と同様に、`new Date()`を使って経過時間を管理する
* テストでこれをフェイクするためには、簡単なヘルパーを使う
    * このヘルパーは1個の日付オブジェクトを受け付け、Dateコンストラクタをオーバーライドする
* 次にコンストラクタが使用の際、フェイクオブジェクトが返され、ネイティブコンストラクタが復元される

```bash
touch lib/stub.js
```

```javascript
(function (global) {
    var NativeDate = global.Date;

    global.stubDateConstructor = function (fakeDate) { //時刻をフェイクする
        global.Date = function () {
            global.Date = NativeDate;
            return fakeDate;
        };
    };
}(this));
```

## テストの追加

### スタブDateを使ってテストする

* 最後の要求が発行されてから最小限のインターバルが経過後、新しい要求がただちに送られることを確認する
* 実行に時間のかかる要求が完了したらただちに再接続されることを確かめる
* このテストは、ポーラーのインターバルを500ミリ秒に設定し、600ミリ秒かかる要求をシミュレートする
* new Dateで600ミリ秒後を表すオブジェクトを作る
* `this.xhr.complete()`でニセ要求の処理を完了する
* この時点で、新しい要求がただちに生成されなければならない
    * 前の要求が開始してからのインターバルの最短は経過しているため
* テストはそのままでは不合格になる

```javascript
TestCase("PollTest",{
    setUp: function () {
        /* ... */
        this.ajaxRequest =ajax.request;
        /+ ... */
    },

    tearDown: function () {
        ajax.request = this.request;
        /* ... */
    },

    "test should re-request immediately after long request":
        function () {
            this.poller.interval = 500;
            this.poller.start();
            var ahead = new Date().getTime() + 600
            stubDateConstructor(new Date(ahead));
            ajax.request = stbFn();

            this.xhr.complete();
            assert(ajax.request.called);
        }
});
```

## ソース修正

* 指定されたインターバルを次の要求開始までの最短インターバルとして使う
* 要求したインターバルが0でも、次の要求は決して同期的な実行をしない
    * setTimeoutを介して実行される
* この方法の利点の1つは、呼び出しスタックが深くなるのを避けられること
* 再帰的に新しい呼び出しを発行することを避けられる
    * 非同期呼び出しを使って次の要求をスケジューリングすると、現在の呼び出しはただちに制御を返してくるため
* しかし、この巧妙な部分がトラブルの原因にもなる
* このテストは新しい要求がただちにスケジューリングされることを想定しているが、そうはならならい
* キューイングされ、実行できる状態になっているタイマーを行動させる
    * テスト内でクロックに触れなければならない

```javascript
function start () {
    /* ... */
    var requestStart = new Date().getTime();

    ajax.request(this.url, {
        complete: function () {
            var elapsed = new Date().getTime() - requestStart;
            var remaning = interval -aelpsed;

            setTimeout(function () {
                poller.start();
            }, Math.max(0, remainting));
            /* ... */
        },

        /* ... */
    });
}
```

## テストの修正

* ポーラーは、ロングポーリングをサポートするようになる
    * このロングポーリングはサーバーに次の要求を送るまでの最短インターバルをオプションで指定可能
* さらに、別のオプションをサポートするように拡張することも可能
    * 前の要求の処理が完了してから次の要求を発行できるまでの時間を設定するetc
    * 要求の処理にどれだけ時間がかかったかは不問で行える
* こうするとレイテンシが上がるが、負荷の高いシステムには効果があるはず

```javascript
//準備のできているタイマーを作動させるために、クロックに触れる
"test should re-request immediately after long request":
function(){
    this.poller.interval = 500;
    this.poller.start();
    var ahead = new Date().getTime() + 600;
    syubDateConstructor(new Date(ahead));
    ajax.request = stubFn();

    this.xhr.complete();
    Clock.tick(0);

    assert(ajax.request.called);
}
```

## ソース修正

### キャッシュ問題を避ける

* ポーラーの現在の実装で問題になる可能性があるのはキャッシュ
* ポーリングは、サーバーから新しいデータをストリーミングしなければならないときに使われる
    * しかしブラウザが応答をキャッシングしていると問題が起きる
* キャッシングは、サーバーが応答ヘッダーを介して制御可能
    * しかし、サーバーの実装には手を付けられない場合がある
* ポーラーをできる限り汎用的にしておきたい
    * ここではURLにランダムな値を追加して、キャッシングが働かないようにする
* トランスポートの`open()`にキャッシュバスターつきのURLを渡すことを要求する 
    * キャッシュバスター: タイムスタンプ

```javascript
//ポーラーはURLにキャッシュバスターを追加してるはず
"test should add cache buster to URL": function(){
    var date = new Date();
    var ts = date.getTime();
    stubDateConstructor(date);
    this.poller.url = "/url";

    this.poller.start();

    assertEquals("/url?" + ts, this.xhr.open.args[1]);
}
```

## ソース修正

* 要求を発行時に、URLに記録済みのタイムスタンプを追加する
* こうすると、キャッシュバスターテストには合格する
* しかし変更されていないURLを使うことを求めている上記のテストには不合格になる
* 最初のテストのURL比較は取り除いてよい
    * このURLは専用テストでテストされているため
* 任意のURLにクエリー文字列を追加すると、URLがすでにクエリー文字列を含んでいるときに動作しなくなる

```javascript
//キャッシュバスターを追加する
function start () {
    /* ... */
    var requestStart = new Date().getTime();

    /* ... */

    ajax.request(this.url + "?" + requestStart, {
        /* ... */
    });
}
```

### 機能テスト

* ポーラーでも機能検出を使って、使えないことがわかっているインターフェイスを定義しない
    * requestインターフェイスのときと同様

```javascript
//ポーラーの機能テスト
(function () {
    if(typeof tddjs == "undefined"){
        return;
    }

    var ajax = tddjs.namespace("ajax");

    if(!ajax.request || !Object.create){
        return;
    }

    /* ... */
}());
```