# Actionサブクラス設計

* Action一覧に上がっているそれぞれのActionで行う処理を設計する

## Actionが行う処理

* セッションの作成
* セッションからのデータ取得
* ビジネスロジックの呼び出し
* セッションへのデータ設定
* 画面遷移

## Action設計書

* UMLのシーケンス図で記述
    * 文章で記述すべきものがあれば、図にメモを残す
* UMLのアクティビティ図で記述
    * シーケンス図では分岐が記述しにくいもの
* Actionクラスはスレッドセーフに作成する
    * 単純にメンバー属性を作成しなければ良い
    * Actionは、状態を持たないように作成
