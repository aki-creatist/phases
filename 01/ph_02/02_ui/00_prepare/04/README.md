# 画面項目パターン

* 画面に配置する項目の形式を検討


## 項目には、表示項目と入力項目がある

* 入力項目
    * 入力項目の入力された値の妥当性のチェックは、ここで検討しない
    * 入力項目の画面上の形式について検討
        * `電話番号を三つの入力項目とするのか、１つの入力項目とするのか`
        * `都道府県をリストボックスで選択させるのか、直接入力させるのか`etc

### 項目

* 電話番号
    * 入力
        * 市外局番、局番、番号の３つの入力項目とする
    * 表示
        * 市外局番、局番、番号を半角ハイフンで区切って表示する
* 都道府県
    * 入力
        * リストボックスで表示・選択する
    * 表示
        * テキストで表示する
* 住所
    * 入力
        * 市区町村、町名番地、アパート・マンション名の３つの入力項目とする
    * 表示
        * 市区町村、町名番地、アパート・マンション名を半角スペースで区切って表示する
