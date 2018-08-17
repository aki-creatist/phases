# Struts設定ファイル

* 1.Struts設定ファイルとは
* 2.主な要素について
    * (1)概要
    * (2)global-exceptions要素
    * (3)global-forwards要素
    * (4)action-mappings要素

## Struts設定ファイル

### 1.Struts設定ファイルとは

* Struts設定ファイルは、Strutsを利用したアプリケーションの動作を決定する非常に重要なファイル
    * Struts設定ファイル: 以下のタイミングに読み込まれる
        * ActionServletが初期化されるタイミング
        * ActionServletからRequestProcessorが起動されるタイミング
    * その設定内容に応じてモジュールの準備が整えられる
* Struts設定ファイルの配置場所は、web.xml に記述する一般的には、/WEB-INF/ディレクトリに配置
    * その名称をstruts-config.xmlとする
* また、Struts設定ファイルに設定できる情報は、およそ以下のとおり
    * URLと起動するActionの関連情報
    * Action実行後に使用されるリソースの情報
    * ActionFormの情報
    * メッセージリソースの情報
* Struts設定ファイルはXML形式まずはその構造について確認していく
* 次のStruts設定ファイルの例を見る

struts-config.xmlの例

```text
<?xml version="1.0" encoding="Shift_JIS" ?>
<!DOCTYPE struts-config PUBLIC
    "-//Apache Software Foundation//DTD Struts Configuration 1.2//EN"
    "http://struts.apache.org/dtds/struts-config_1_2.dtd">

<struts-config>
    <action-mappings >
        <action path="/sample01/sample" type="sample01.SampleAction">
            <forward name="success" path="/jsp/sample.jsp" />
        </action>
    </action-mappings>
</struts-config>
```

* Struts設定ファイルはXML形式
    * XML宣言を最初に記述する
    * 続けてDOCTYPE宣言を記述する
    * DOCTYPE宣言では、この設定ファイルのDTDを指定している
    * 実際にこのURLから得られるDTDを確認して設定方法を知ることも可能
    * Strutsのライブラリの中にも含まれているので、そちらを参考にすることも可能
* Struts設定ファイルのルート要素は、struts-config要素
    * この中にモジュールの動作を制御するための、さまざまな設定を行う

### 2.主な要素について

Struts設定ファイルのルート要素struts-configに記述する主要な要素は以下の通り

* form-beans要素
* global-exceptions要素
* global-forwards要素
* action-mappings要素
* controller要素
* message-resources要素
* plagu-in要素


### (1)概要

* アプリケーションで使用するActionFormに関する情報を記述する
* この要素に重要な属性はない
* form-bean要素を子要素として持つ
* form-bean要素は、このstrutsアプリケーションで使用する
* ActionFormのクラス名とインスタンス名を関連付ける重要な要素

#### form-barn要素の属性

| 属性名 | 必須 | 説明 |
|:----|:----|:----|
| name | ◯ | ActionFromのインスタンスを識別するための名前を指定する |
| type | ◯ | ActionFormのくらすめいを完全限定名で指定する |

* form-bean要素
    * form-property要素を子要素として持つ場合がある
    * これは、以下の場合に必要となるもの
        * DynaActionFormと呼ばれるActionFormかそのサブクラスを使用した場合
    * form-property要素の属性を以下に示す

| 属性名 | 必須 | 説明 |
|:----|:----|:----|
| initial |  | この要素で指定するプロパティの初期値を指定する |
| name | ◯ | この要素で指定するプロパティの名称を指定する |
| size |  | このプロパティが配列の場合、この属性の値の長さで配列を初期化する |
| type | ◯ | この要素で指定するプロパティの方を指定する |

#### form-beans要素の記述例

```text
<form-beans>
    <form-bean name="sampleForm" type="sample.SampleForm"/>
    <form-bean name="dynaForm" type="org.apache.struts.action.DynaActionForm">
        <form-property name="id" type="java.lang.String" />
    </form-bean>
</form-beans>
```

### (2)global-exceptions要素

* global-exceptions要素では、Actionにより例外がスローされたときの振る舞いについての設定を行う
* global-exceptions要素は、exception要素を子要素として持つ
* 詳細な設定はexception要素で行う

#### exception要素の属性

| 属性名 | 必須 | 説明 |
|:----|:----|:----|
| path |  | 例外発生時のフォワード先リソースを、コンテキストル一卜からの相対パスで指定する |
| key | ◯ | 例外発生時にエラーメッセージを検索するキーの値を指定する対応する値がメッセージリソースに存在する必要がある |
| type | ◯ | ハンドリングする例外クラスの完全限定名を指定する |
| handler |  | 例外ハンドラクラスの完全限定名を指定する |

```text
<global-exceptions><exception type="java.io.IOException" key="error.io" path="/WEB-INF/jsp/ioError.jsp" />
</global-exceptions>
```

### (3)global-forwards要素

* グローバロフォワードに関する情報を設定するすべてのActionから使用される
* ActionForwardをこの要素で設定するforward要素をこ要素として持つ

| 属性名 | 必須 | 説明 |
|:----|:----|:----|
| modeule |  | フォワードするモジュール名を指定するモジュール名はスラッシュから始まる |
| name | ◯ | Actionforwardを識別するための名前 |
| path | ◯ | フォワードするJSPなどのリソースをコンテキストルートからの相対パスで指定する |
| redirect |  | リダイレクト化フォワードかを設定するtrueならリダイレクト、falseならフォワードfalseが初期値 |

global-forwards要素の使用例

```text
<global-forwards>
    <forward name="success" path="/WEB-INF/jsp/success.jsp"/>
    <forward name="fail" path="/WEB-INF/jsp/fail.jsp"/>
</global-forwards>
```

### (4)action-mappings要素

* この要素で設定された内容に基づき、ActionMappingが生成される
* action-mappings要素には特に重要な属性はない
* 主な設定はこ要素であるaction要素で指定する

#### action要素の属性

| 属性名 | 必須 | 説明 |
|:----|:----|:----|
| path | ◯ | Actionを起動するURIを指定する戦闘は/(スラッシュ)から始まる |
| type | ※ | RequestProcessorより呼び出されるActionの完全限定名を指定する |
| forward | ※ | Action以外のリソースをコンテキストルートから相対パスで指定するActionを経由せずに、他のリソースへフォワードする時に使用する |
| include | ※ | Action以外のリソースをコンテキストルートから相対パスで指定するActionを経由せずに、他のリソースをインクルードする時に使用する |
| parameter |  | Actionに追加情報を渡す時に指定する |
| roles |  | このActionへのアクセスを許可されたセキュリティロール名のカンマ区切りのリストを指定する |
| name |  | 使用するActionFormのインスタンス名を指定する対応するform-bean要素のname属性の値と一致させる |
| attribute |  | name属性で指定したActionFormをスコープに登録する際の名前を指定するデフォル卜はname属性の値 |
| scope |  | name属性で指定したActionFormをどのスコープで登録するのかをrequest、sessionのいずれかで指定する |
| validate |  | name属性で指定したActionFormにおいて、validate()による検証を行うかどうかを指定するtrueとしたとき、validate()が呼び出されるデフォルトはfalse |
| input |  | validate属性がtrueの場合に、validate()が返すActionErrorsのサイズが0でないとき（検証が失敗したとき）に表示されるページを指定する |
| unknown |  | このActionをデフォル卜のActionとする際にtrueを指定するいずれのActionにも関連付けられていないリクエストがあった場合に、このunknown属性にtrueを指定しているActionが実行される1つのモジュール中、unknown属性にtrueを指定できるActionは1つだけ |
