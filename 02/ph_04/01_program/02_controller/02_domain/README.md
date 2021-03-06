# DomainModelパターン

## 概要

ビジネスロジックをエンティティに持たせる

* カプセル化をすることで、DBのテーブルの変更やビジネスロジックの変更を隠蔽
    * エンティティをカプセル化とポリモーフィズムを実現可能
        * 概念モデルから抽出されたエンティティに自然な形でビジネスロジックを配置できる
* DomainModelでは、エンティティ間に強い依存関係が発生する
* エンティティにシステムの重要な情報が集中するので、`システムの変更要件がエンティティに局所化`される
    * DomainModelにビジネスロジックを追加していくと、DomainModelが巨大化する
        * 他のDomainModelの呼び出しが多くなり、かえって複雑になることがある
* Domainとは、`システムが関心のある対象の領域`という意味

## Strategyパターンを利用する

* システムの変更要件がエンティティに局所化ためエンティティが複雑になってしまう可能性がある
* デザインパターンなどを取り入れて、DomainModelの構造をシンプルにしながら、処理を追加するようにする
* 適宜、`Strategyパターン`などを使ってビジネスロジックを別のクラスに切り出すと良い
    * トランザクション管理は、エンティティに付与するか、`Facadeクラス`を用意する
