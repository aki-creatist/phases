# TDDとDOM操作：チャットクライアント

## 概要

* チャットバックエンドのためのクライアントを実装する
    * テスト駆動開発をDOM操作やイベント処理に応用する
* DOMはAPIなので、他のAPIと違いはない
    * その為、単一責任の原則に従い、コンポーネントの疎結合を維持する
    * DOMはホストオブジェクトから構成されている

## クライアントのプラン

### 課題

* チャットGUIを作る
* [概要](00)
* [テストケースのセットアップ](01)
* [クラスを追加する](02)
* [イベントリスナーを追加する](03)
* [サブミットイベントの処理](04)
* [機能テスト](05)
* [Node.jsとともにクライアントを使う](06)
* [コントローラとメソッドを定義する](07)
* [ビューを設定する](08)
* [メッセージを追加する](09)
* [同じユーザーからの反復メッセージを抑える](10)
* [機能テストと動作確認](11)
* [メッセージフォーム](12)

## メッセージリスト

* メッセージリストは、定義リストとして表示される
* 各メッセージは、ユーザーを消すdt要素とメッセージを示すdd要素として表現
* コントローラは、モデルの`message`チャネルを観察してメッセージを受け取る
* DOM要素を作ってそれをビューに注入する
* ユーザーフォームコントローラと同様に、ビューの設定時に`js-chat`というクラス名を追加する 

## 最終的なチャットクライアント

* すべてのコントローラが完成
* チャットクライアントを組み立てて動作確認
* HTML文書にメッセージフォームを追加する 

```bash
vim index.html
```

```html
<!-- ... -->
<dl id="messages"></dl>
<form id="messageForm">
<fieldset>
  <input type="text" name="message" id="message"
         autoconmplete="off">
</fieldset>
</form>
<!-- ... -->
```

* `form_controller.js`をコピー
* 更新した`user_form_controller.js`をコピー
* `message_form_controller.js`をコピー
* index.htmlにこれらを取り込むためのscript要素を追加する
* ブートストラップスクリプトを追加する 

```javascript
//最終的なブートストラップスクリプト
/* ... */
userController.observe("user", function(user) {
    /* ... */

    var mForm = document.getElementById("messageForm");
    var messageFormController =
        Object.create(c.messageFormController);
    messageFormController.setModel(model);
    messageFormController.setView(mForm);

    model.connect();
});
```

* ブラウザにクライアントをロードする
* サーバー、クライアントともJSを使ってチャットシステムのクライアントが表示される
* メッセージのポストがうまくいかない場合
    * `messageFormController`の`handleSubmit()`でデフォルトイベントアクションを定義する
        * `messageFormController`を完成する 

## 最後の仕上げ

* 動作確認
    * ブラウザをもう1つ起動する
    * 複数タブで起動するetc
* 現在はクッキー不使用
    * 同じブラウザの異なるタブから２つのセッションを実行可能 

### アプリケーションのスタイル

* クライアントはいずれスクロールするようにする
* メッセージは枠の外に追加されていく
* スタイルシートでは、スクロールはメッセージを表示する定義リストに移る
* 高さに制限を設ける
    * メッセージフォームの表示が消えないようにするため
    * [public/css/chapp.css](public/css/chapp.css)
    
```bash
vim css/chapp.css
```

### スクロールの修正

* メッセージリストコントローラにちょっとした改良
    * 定義リストがいつも一番下までスクロールするようにする 
    * ユーザーは新しく入ってきたメッセージにより興味を感じるため
* scrollTopプロパティにリストの最大値を設定する
    * リストを一番下までスクロール可能
    * この値の正確な調査は不要
    * 最大値以上の値を設定すれば、ブラウザが可能な限りまで要素をスクロールする
    * 要素のscrollHeightの使用が適切
* scrollHeightの値は、要素の内容の高さ全体
* 明らかにscrollTopの最大値よりもいつも大きい

## テストの追加

* このテストは、実際の要素ではなくスタブの要素を使用
* このようなテストでは、入力と出力を完全にコントロールできなければならない
    * 正しい動作を確かめるため
* 要素のscrollTopプロパティセッターをスタブにすることはできない
* scrollTopの値が正しく設定されていることを簡単に調べることもできない
* scrollTopの値は表示された高さによって左右される
* オーバーフロー時に要素をスクロールさせるためには最初からスタイルを追加しなければならない

```javascript
//メッセージリストコントローラがビューをスクロールダウンすることを確かめる
TestCase("MessageListControllerAddMessageTest", {
    /* ... */

    "test should scroll element down": function () {
        var element = {
            appendChild: stubFn(),
            scrollHeight: 1900
        };
        this.controller.setView(element);
        this.controller.addMessage({ user:"me",message:"Hey" });

        assertEquals(1900, element.scrollTop);
    }
});
```

## ソース修正

* scrollTopにscrollHeightの値を代入する 

```javascript
//新しいメッセージが追加されるたびに、メッセージリストをスクロールダウンする
function addMessage(message) {
    /* ... */

    this.view.scrollTop = this.view.scrollHeight;
}
```

## テストの追加

### テキストフィールドのクリア

* ユーザーがメッセージをポスト後のメッセージの再利用は想定しない
    * 再利用: ここでは前のメッセージの文章を利用して次のメッセージを書くこと
* メッセージフォームコントローラは、メッセージがポスト時にテキストフィールドをクリアすべき

```javascript
//メッセージフォームがメッセージをクリアしていることを確かめる
"test should clear form after publish": function () {
    var el = this.element.getElementsByTagName("input")[0];
    el.value = "NP: A vision of misery";

    this.controller.handleSubmit(this.event);

    assertEquals("", el.value);
}
```

## ソース修正

* メッセージが送られたことが確かめられてからフォームをクリアする
* メッセージを送った直後にフォームをクリアし、メッセージが届くことを祈るしかない
    * `comentClient`は、このタイミングで成功コールバックを追加可能にはなっていないため
* 修正方法は、cometClientに第3オプション引数を追加して、送信成功を待てるようにする
* 以下はメッセージフォームコントローラの新しい`handleSubmit`を示したもの 
    * メッセージフォームが、テキストフィールドを初期化した後、フォーカスも移っているとなおよい 

```javascript
//発行したあとでメッセージをクリアする
function handleSubmit(event) {
    /* ... */

    input.value = "";
}
```

## 動作確認

* メッセージフォームとコピーchappのpublicディレクトリにコピー
* メッセージリストコントローラをchappのpublicディレクトリにコピー
* ブラウザをリロード

## デプロイについての注意

* 単純にファイルをコピーしてデプロイするのでは、煩雑でエラーを起こしやすい

## ミニファイ

* 多数のスクリプトから構成するとパフォーマンス的に問題がある
* 今回15個の別個のスクリプトファイルを使ってアプリケーションを構成されている
* RubyとRubyGemsをインストールしてあればJSとCSSを結合、ミニファイするツールが使える

### Juicerの利用

* Juicerは、スクリプトをデプロイ用にパッケージングするツール

```bash
#JuicerとYUIコンプレッサをインストールする
gem install juicer
juicer install yui_compressor
```

* 以下のコマンドをNode.jsアプリケーションのルートで実行する
* クライアントサイドアプリケーション全体を格納する1個のファイルが作られる 
    * ここでは`chat.min.js`

```bash
#Juicerを使ってファイルを圧縮する

Juicer merge -s -f -o public/js/chat.min.js\
public/js/function.js \
public/js/object.js \
public/js/tdd.js \
public/js/observable.js \
public/js/form_controller.js \
public/js/user_form_controller.js \
public/js/json2.js \
public/js/url_params.js \
public/js/ajax.js \
public/js/request.js \
public/js/poller.js \
public/js/comet_client.js \
public/js/message_list_controller.js \
public/js/message_form_controller.js \
public/js/chat_client.js
```

* こうすると、チャットルームを格納する14KBのJavaScriptファイルが作られる
* gzip圧縮で提供すれば、ダウンロードサイズは約5KBに抑えられる
* Juicerは、スクリプトファイル内で宣言された依存ファイルも見つけられる
* 個々のファイルに依存ファイルのコメントを残しておく
    * 依存ファイルを含んだ完全名ファイルを作成可能になる
    * 実行コマンド: `juicer merge chat.js`

## まとめ

* MVP/パッシブビューパターンを採用
    * ビューでは再利用可能なコンポーネントを明らかになる
    * モジュール化された形でチャットクライアントを実装可能
    * モジュール間の結合は非常に疎になり、切り離してテストしやすい
