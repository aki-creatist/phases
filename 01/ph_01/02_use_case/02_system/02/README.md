# システムユースケース抽出

* ビジネスユースケースからシステムユースケースを抽出する

## 手順

* [ソフトのパンフレットを作成](01)
* [実行単位業務関連図の修正](02)
* [UMLでユースケース図を記述](03)

## 用語

* [アクター](03_actor)

ビジネスユースケースを作成する事自体は、システムレベルユースケースとは別物

## 例2

* 買い物かごを表示する画面と決済方法を入力させる画面が1つなのか、別れているのかは決めていない
    * それは別途、UIを決定する段階で考えればよい
* これにより、画面設計などの具体的な実現方法が変わっても、影響を受けない本質的な要件を表現可能

## ユースケースシナリオの各ステップの意味

* ユースケースの特徴は、自然言語の文章で書くこと
* ニュアンスの違いを柔軟に表現可能
    * 自然言語の文章で書くユースケースの柔軟さは弱点でもある

### 例1

3と5のステップが別れている

1. 会員は商品を検索する
2. システムは商品の一覧を表示する
3. 会員はほしい商品を買い物かごに入れる
4. システムは買い物かごを表示する
5. 会員は決済方法を入力する

### 例2

3と5のステップが3にまとめられている

1. 会員は商品を検索する
2. システムは商品の一覧を表示する
3. 会員はほしい商品を買い物かごに入れ、決済方法も入力する

* この連続したシナリオを書いた人は、商品を買い物かごに入れた人にすぐに注文へ進んでほしかったと考えられる
* 買い物かごにたくさん商品を入れるよりも、1つだけ購入することが多い商材を扱っている可能性がある

## TODO

* 業務フローからシステムユースケースを抽出
* 要件定義段階に渡す

## 事後作業

以下を確認する

* ある目的を実現するためのユースケースが足りているか
* あるアクターのライフサイクルからユースケースが足りているか
    * 「商品を返品する」などは忘れられがち
* すべてのトリガーに対するユースケースが洗い出せているか
* 関係者による承認を得ているか