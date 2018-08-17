# Webサーバ

## Webサーバの仕組み

* Webブラウザー
    * Web Brouser
    * アプリケーション・ソフトウェア
        * ネット上のWebページを閲覧する時に利用する
    * browse ＝ `ざっと見る`という意味
        * Windows標準のInternet Explorer
        * OS X標準のSafari
        * Firefox、chromeなど
* Webサーバーから送られてきたHTMLデータを解析しレンダリング
    * レンダリング ＝ 必要な画像などとともに画面上に出力

## WebサーバーとWebブラウザーの通信

### リクエストとレスポンス

1. リクエスト
2. レスポンス

* リクエスト
    * WebブラウザーはWebサーバーに処理を要求する
* レスポンス
    * WebサーバーはWebブラウザーがリクエストした処理を行い、HTMLデータなどの応答を返す

![server_01](image/server_01.png)

### HTTP

* `HTTP` というプロトコルが使われる
    * HyperText Transfer Protocol
    * HTTPの仕様はW3Cで定められている
        * W3C: World Wide Web Consorxium
* Webサーバーは通常、80番ポートを使ってWebブラウザーからの接続(リクエスト)を待ち受ける

## 広く使われているWebサーバー

* Apache
* Nginx
    * Apacheよりも少ないメモリで高速に動作する
    * アクセス負荷の高いサイトで利用される
    * リバースプロキシにも利用されている
        * リバースプロキシ ＝ 負荷分散のための仕組み
