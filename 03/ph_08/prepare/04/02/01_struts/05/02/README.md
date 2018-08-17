# 設定ファイルの編集

Strutsを動かすための準備として、次の2つの設定ファイルを編集する

## 1.web.xmlの編集

web.xmlはWebアプリケーションの要素および配置情報をサーブレットコンテナに伝えまる役割を持つ重要なファイルこの中にStrutsを使用するための記述を行う

[/WebContent/WEB-INF/web.xml](web.xml)を編集する

* Strutsを利用したWebアプリケーションで使用されるサーブレットは、org.apache.struts. action.ActionServletのみ
* servlet要素では、このサーブレットを actionという名前で登録する
    * このサーブレットはStruts設定ファイルに書かれた内容に従って動作するためその設定ファイル名を初期値として設定する
    * ここではファイル名をstruts-config.xmlとし、web.xmlと同じディレクトリに配置
    * servlet-mapping要素では拡張子が`do`のURLでアクセスされた際に、ActionServletが呼び出されるように設定

## 2.struts-config.xmlの作成

* Struts設定ファイルの設定
    * このファイルはStrutsを使用したアプリケーションの設計図に該当する

[/WebContent/WEB-INF/struts-comfig.xml](struts-comfig.xml)

* `<action>`タグのpath属性に指定したURLにアクセスすると、type属性に指定したLoginActionが実行される
    * URL: `http://localhost:[ポート番号]/StrutsSample/sample01/login.do`
* 最終的には`<forward>`タグのpath属性に指定したsuccess.jspが表示されるという流れが重要

設定ファイルの編集は以上

## 3.ActionクラスとActionFormクラスの作成

* 2つのクラスを作成する前に`/src/`の直下に`sample01`というパッケージを作成
* まずはActionFormを作成する
    * 先ほど作成したパッケージの直下に`LoginForm`という名前のクラスを作成
    * ActionFormはorg.apache.struts.action.ActionFormを継承する必要がある
    * ActionFormの役割
        * リクエストパラメータの受け取りリクエストパラメータ名に対応するフィールド及び、それらに対するgetter/setterメソッドを作成すると値が自動的にフィールドにセットされる
        
[LoginForm](LoginForm.java)

* Actionを作成する
* 作成場所はActionFormと同様
* Actionの役割
    * データベースへの問い合わせなど、ビジネスロジックを呼び出すこと
    * 処理が終了した際にJSPやHTMLにフォワードを行い、HTTPレスポンスとして利用者へ応答を返し、一連の処理を完了させること
* Actionを作成する際は、org.apache.struts.action.Actionを継承する
    * このクラスでは`execute()`をオーバーライドし、このメソッドの中にリクエストパラメータに対する処理などを記述する
* 今回は、引数で渡されるActionFormを先ほど作成したLoginFormにキャストし、LoginFormにセットされたリクエストパラメータの値を取得する
* 続いて、次の画面で表示する文字列をrequestスコープに登録する最後に、フォワード先のJSPを指定するActionForwardインスタンスを返する

作成するLoginActionを次に示する

[LoginAction](LoginAction.java)

## 4.HTML、JSPの作成

* IDとパスワードを入力するindex.htmlと、入力された文字列を表示させるsuccess.jspを作成
    * index.htmlは`/WebContent/sample01/`の直下
    * success.jspは`/WebContent/WEB-INF/jsp/sample01/`の直下
* まずは、index.htmlの作成
    * idとpasswordのinput要素のname属性の値はLoginFormのプロパティと一致している必要がある
* [index.html](index.html)
* [success.jsp](success.jsp)
    * LoginActionでリクエストにセットしたmessageの値を参照している

## 5.サンプルを実行する

* 作成したアプリケーションの動作を確認
* 本来は作成したプログラムをコンパイル（ビルド）とTomcatへの配備（デプロイ）が必要
    * これらの作業はEclipseが自動的に行うため割愛する
* Tomcatを起動する（すでにTomcatが起動している場合は、再起動
* Tomcatが起動したら、Webブラウザから次のURLにアクセスし、動作を確認

`http://localhost:[ポート番号]/StrutsSample/sample01/index.html`