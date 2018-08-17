# 背景

* ServletとJSPは比較的低レベルのもので、効率的にWebシステムを開発するには十分ではない
    * Servlet
        * Servlet APIはHTTPプロトコルレベルのAPI
        * HTTPリクエストやHTTPレスポンス、CookieやURLRewritingを使ったHTTPセッション管理などの機能を提供
    * JSP
        * HTMLを動的に生成するための仕組み
        * JSPもServlet APIの一部
* Strutsのようなフレームワークが登場
    * Webアプリケーションを作成するためのフレームワークの1つ
    * 以下で構成
        * サーブレット、
        * JavaBeans
        * JSP
        * メッセージリソースファイルやXMLなど