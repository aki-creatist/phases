## アプリケーション

* システムの利用者にとって付加価値のある機能を提供
    * パッケージを利用することもできる
        * パッケージによっては、ミドルウェアやDBを内部に持つ
    * ゼロから開発することもできる

### アプリケーションアーキテクチャ

```text
システムコンポーネント、コンポーネント同士と環境との間の関係、およびその設計と進化を支配する原理に体現されたシステムの基本的な構造。
```

### 業務アプリケーション

* 何らかの産業に携わるユーザー企業の業務を支援するシステム
    * 流通業
        * 受発注、出荷指示、在庫管理、決済管理、商品管理など
    * 製造業
        * 生産計画、調達・材料管理、仕掛品完成品管理など
* Webアプリケーションとして開発することが多くなっている

### 業務アプリケーションの共通する部分

* 機能的に似ている部分
    * 受発注のデータ項目や処理が似ているetc
* 基本構造が似ている部分
    * `受信`
        * システムの利用者が画面から入力したり
        * 指示した内容をシステムが受け取り
    * `加工`
        * システムが入力チェック
        * 変換や加工を行う
    * `保存`
    * `応答`
        * DBやバックエンドのシステムに送信etc
        * 最終的には処理結果を返す

![flow_00](image/flow_00.png)
