## 1.プロジェクトの作成

### プロジェクトの設定

* Eclipseで新規にプロジェクトを作成
* Eclipseのファイルタブ→新規→その他→動的WEBプロジェクト
    * プロジェクト名: StrutsSample
    * ターゲット・ランタイム: Apache Tomcat v6.0

### サーバーに追加

* サーバービューの`ローカル・ホスト の Tomcat v6.0 サーバー`を右クリックで`追加および除去`を選択
* ・`StrutsSample`を選択して、追加ボタンを押下

### Strutsサポートの追加

* 作成した`StrutsSample`プロジェクトの`WebContent`を右クリックし、`新規→その他`と進む
* 開いたウィンドウから、`Amateras→Struts→Strutsサポートの追加`を選択し、`次へ`を押下
* `Webアプリケーションのルート`の値が`/StrutsSample/WebContent`であることを確認し完了ボタンを押下