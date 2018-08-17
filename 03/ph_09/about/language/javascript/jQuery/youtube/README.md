# API

## 概要

### APIの利用の価値

* ネット上のサービスを、自分のアプリの一部のように利用可能
* APIでは、XMLやJSONで情報を返す

#### XML(eXtensible Markup Language)

* 決められたタグを持たないHTMLのようなもの
    * データの提供者が自分の好きにタグを設定可能
        * 今度は閲覧のための余計な情報も含まれない
        * タグの名前がそのままデータの意味を表せる

### 問い合わせ成功時

* Web APIでは代わりにXML形式で返される

### 要素の意味の把握のツリー図

```text
<fead> 結果全体
  └── <openSearch:totalResult>  検索結果の総件数
      <openSearch:startIndex>   検索結果の取得開始位置
      <openSearch:itemsPerPage> ページあたりの件数
      <entory>                  個々の動画情報
         ├── <title> タイトル
         ├── <link>  リンク情報
         │    ├── @href リンク先
         │    └── @type データの形式
         └── <media:group> メディア情報
```

* XML形式のデータをそのまま人間には見ずらい
    * 実際にはJavaScriptやPHPなどのアプリケーションで読み込んで、処理を行う
    * 今回作成する例
        * PHP経由で取得したXMLをさらにJavaScript(jQuery)で受け取る
        * 検索結果をHTMLページに整形する

## APIで住所検索機能を実装

* サーバーからXML形式のデータを取得し、処理するには`$.get()`を利用

### loadより汎用的な非同期通信を行う $.get()

* `load()`
    * サーバー側から受け取ったデータをjQuery(JavaScript)側で加工したい
    * シンプルなコードで利用できるが、応用が利かない
* `$.get/done()`
    * サーバー側から受け取ったデータをjQuery(JavaScript)側で加工したい
    * 応用が効く
* `$.get`
    * サーバーからデータを受信する
* `done`
    * 受信したデータを手元で処理する
    
```javascript
$.get(
    '読み込むデータのURL'
    [, 読み込み先に送信するデータ]
)
.done(function(data){
    通信に成功した場合の処理
})
```

#### これまでのメソッドと$.getの差異

* これまで
    * $(セレクター).〜
        * 何らかの要素セットを対象に処理を行う
* `$.get`
    * $.〜
        * 何らかの要素セットを対象に処理を行うわけではない
            * 最初に$()関数で要素セットを用意しておく必要がない

```js
$('#result').load('html.html');
```

* 以下のような書き換えも可能

```js
$.get(html.html')
.done(function(data){
    $('#result').html(data);    //処理結果を<div id="result">に反映
});
```

## APIのアクセス

### ソースの確認

* 通信に成功した場合の処理を書いたコールバック関数が長い
    * そのため、まずはコールバック関数を除いた部分を確認

指定しているvideo.phpは以下
  
* video.php
    * クエリ情報(?keywd=jQuery&page=1)の検索キーワード(keywd)とページ番号(page)を受ける
    * APIから必要な結果を取得するPHPスクリプト
* 値のセット(4~5行目)
    * { パラメータ名:値, ... } の形式のような形式をハッシュと呼ぶ
        * ここではページ番号(page)は固定で１
        * 検索キーワード(keywd)にはテキストボックスkeywdの値をセット

これで、video.phpに`$.get()`でアクセス可能
    
```js
$.get(
  '../video.php',        // 通信先のURL
  {        // ↓通信先に渡すデータ
    keywd: $('#keywd').val(),
    page: 1 
  }
)    
.done(function(data) {        // コールバック関数
    〜 省略 〜
});
```

## APIから取得した結果を処理する

* video.phpから取得したデータを処理
    * video.phpの結果はAPIから取得したXML形式のデータ
    * `done()`で表されたコールバック関数でこれを処理する

1. 結果の表示領域(<div id="result">要素)を空にする
    * 最初に表示領域をクリアしておかないと、続けて検索を行った場合に、検索結果がどんどん追加されていってしまうため
2. 結果データから<entry>要素を取り出し、その内容を順番に処理 `$('entry',data).each`
    * dataは結果データ(今回はXMLデータ)
    * `$()関数`はHTMLページから特定の要素を取り出す以外に下記のような用途がある
        * `$(セレクター,XMLデータ)`構文を使用し、XML形式のデータも処理できてしまう
    
```js
$('#result').empty();

$('entry', data).each(function() {
  $('#result').append(
    $('<a></a>')
      .attr('href', $('link[type="text/html"]', this).attr('href'))
      .append(
         $('<img>')
          .addClass('thumb')
          .attr({
            src: $('media\\:thumbnail, thumbnail', this).attr('url'),
            title: $('title', this).text()
          })
      )
  );
});
```

* `each()`の中では以下のようなタグを生成して、順番に<div id="result">に追加
    * `append()`を利用することで、階層を持ったHTMLを動的に生成できる
* `each()`の中では、thisは順番に取り出した要素(ここでは<entry>要素)を表す
    * `&('title', this)`は、`<entry>`要素配下の`<title>`要素を表す

```html
<a href="<link要素のhref属性の値>">
    <img src="<media:thumbnail要素配下のUrl要素の値>" title="<title要素の値>"/>
</a>
```

## 動画検索機能にページング処理を追加する

* 動画検索アプリケーションに対してページング機能を実装
    * 検索キーワードにヒットした最初の20件しか確認できなかった
    * ページング機能によってそれ以降のデータも自由に確認できるようにする

### 準備

* ページャ(ページングのためのリンク)を表示する`<div id="pager">`要素を追加
* ページャを中央寄せするための#pagerスタイルを追加
* ページャのここのリンクをスタイル付けするための、`.pager_link`スタイルの追加

### ページング機能のスクリプトを概観

* 複数の箇所でイベント処理を共有している場合
    * ダメな方法：それぞれで同じコードを記述する
    * いい方法：あらかじめonsearchという名前としてイベント処理を準備しておく
        * click、`on()`では名前でもって関連付ける
        
```js
var onsearch = function(e) {
  〜 省略 〜 
  e.preventDefault();
};

$('#search').click(onsearch);
$('#pager').on('click', '.pager_link', onsearch);
```

## ページング本体の処理を確認する

* `$(this).text()`はイベント発生元となる要素の配下のテキストを表す
    * `[検索]`ボタンであれば空
    * ページャであればページ番号が入っている
        * `$(this).text()`が空でない場合には最初の検索であるとみなす
        * 変数`page_num`に１を、そうでない場合にはリンク上のページ番号をセット

```js
var page_num = !$(this).text() ? 1 : $(this).text();
```

## Ajax通信の進捗状況やエラー情報を表示する

* Ajaxを利用
    * Ajaxによる通信中に進捗バーを表示する
    * 検索エラーが発生した場合にエラーメッセージを表示する
    
```html
<div id="prog"><img src="../images/loader.gif" alt="" /></div>
```

* ajaxStartイベント
    * 進捗バーを表示し、ajaxStopイベントで進捗バーを非表示にする
    * ( = Ajax通信中に進捗バーを表示する)
* ajaxSendイベント
    * 通信開始前に特定のパラメータ情報を追加
* ajaxErrorイベント
    * 通信に失敗した場合のエラーを表示
* ajaxCompleteイベント
    * 通信が完了した時に何かしらユーザーに追加(アニメーション処理を実行するなど)

## jQueryからAPIに直接アクセスする

### $.getJSON()を利用する

* サーバー側でプログラムを書かなくても外部のサービスにアクセス可能

### 外部サービスとスムーズに連携

* 通常のAjax通信での制限
    * Ajaxでは自分が属しているサーバー(ドメイン)以外とは、通信できない
    * 外のサービスを利用するには、いったんサーバーサイド(PHPなど)のプログラムを準備
        * これを経由して外に出る必要がある

しかし、外部のサービスがJSONPに対応している場合例外的にAjaxでも外部のサービスと通信が許可される

### JSONP

JavaScriptのオブジェクト形式(JSON)でデータをやり取りする仕組み

### APIでJSONPを利用する

* APIはJSONPに対応している
    * altパラメータにjsonと言う値を渡すだけで、JSONPのためのデータを取得可能
* まずは対象URLの結果を確認(ダウンロードしたらメモ帳などで確認する)
* JSON技術を利用したアクセスを行うには、`$.getJSON()`を利用する

```js
$.getJSON(
    '読み込むデータのURL'
    [, 読み込み先に送信するデータ]
)
.done(function(data){
    通信に成功した場合の処理
})
```

### 基本的なルール

* 検索のためのURLにクエリ情報「callback=?」を付与する
    * これによりjQueryでは外部のサービスから取得したデータを処理できるようになる
* コールバック関数はJavaScriptのオブジェクトを受け取る
* `$.get()`との違い
    * コールバック関数に渡される値(ここではdata)が、JavaScriptのオブジェクトという点
        * data.feed.entryのようにすることでfeedプロパティは以下のentryプロパティにアクセスできる
        * 検索結果の１件目の動画タイトルを取り出したいならば、`data.feed.entry[0].title.$t`のように書ける
        
### オブジェクトからサムネイルを組み立てる

* APIから取得したデータを処理
* data.feed.entryで検索結果を全て配列(オブジェクトの集合)として取得
    * 取得した配列は、`$each()`で順に処理可能

```js
$.each(data.feed.entry, function() {
  $('#result').append(
    $('<a></a>')
      .attr('href', this.link[0].href)
      .append(
         $('<img>')
          .addClass('thumb')
          .attr({
            src: this.media$group.media$thumbnail[0].url,
            title: this.title.$t
          })
      )
  );
});
```

`$.each()`は配列の内容を順に処理する

```js
$.each(配列, function(){
    ...処理内容...
}
```

* `function(){...}`の中では、thisで個々のオブジェクトにアクセスできる
    * `this.title.$t`であれば、data.feed.entryプロパティで取得した結果データの中のtitle.$tプロパティを指す
    * `this.link[0].href`、`this.media$group.media$thumbnail[0].url`
        * `[0]`がついているのは、link/media$thumbnailは複数の値を持つ配列であるため
        * ここでは、決め打ちで先頭の値を取り出している
    * オブジェクトからデータを取り出すには、特にjQueryの機能は利用しない
        * よって、`$(this)`のように囲む必要がない

# まとめ

* 一般的なWebの世界
    * サービス(コンテンツ)を提供するサーバー
    * サービスを受け取るクライアント
* Ajaxは、サーバーとの通信をJavaScriptを使って行う技術
    * Ajaxによる通信では、ドメインをまたがった要求を行うことはできない
* サーバーから取得したデータをそのままページに反映するには、`load()`を使用する
* Web APIを利用するこのはメリットがある
    * 外部で提供されているサービスをあたかも自分のアプリケーションの一部のように利用できる
* サーバーから取得したデータに対して何らかの処理を行うには、`$.get()`を使用する
* `$.getJSON()`とJSONPという技術を利用することで、ドメインをまたがった通信が行える
* Ajax通信の途中でアプリケーション独自の操作を挟むこともできる
    * ajaxStart、ajaxStop、ajaxErrorなどのAjaxイベントを利用する
