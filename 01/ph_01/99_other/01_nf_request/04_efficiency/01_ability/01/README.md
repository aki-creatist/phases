# ①システム化企画・要件定義時

* 業務諸元に基づくピークを認識
* マッピング
* 処理がピークを迎える瞬間の負荷を想定する
* 注目する処理
    * 業務諸元で厳しい負荷がかかりそうなところ(=データ量が多いところ)
    * 連携数が多いところ
    * ターンアラウンドタイムが厳しいところ
    * 処理が複雑なところ
* 業務の流れに沿って業務のサービスイメージを見ていく

## 業務諸元に基づくピークを認識

* `RFP`
    * クリアしなければならない性能を担保するため
    * １日の発注量は何万件etcの必須の業務諸元が記載されている

## マッピング

* 業務諸元の値がどのコンピュータ機能にマッピングされるかを検討する
    * 個々の業務の要件に関して、次に業務の流れに沿って確認
    * どの機能にどれだけの性能が要求されるのかがわかる

## 処理がピークを迎えるタイミングを絞る

* 繁忙期(ピーク)を計算の対象に選ぶ
    * 業務面から見た定期・不定期に発生するピーク
    * 業務が集中する時期を想定する
    * この際、業務量の見極めは１日単位ではない
        * その中の何時なのか
        * 短い処理なら何時何分なのか
    * 不定期には、受注時・発注前・作業着手時・納品時・返品発生時など、
    * 取引やイベントのライフサイクルに沿った処理を想定する
    * 問合わせやクレームへの対応も不定期のピークになる可能性がある

## 処理がピークを迎える瞬間の負荷を想定

* 時間当たりの必要処理量を想定する
    * トランザクションの集中する時間帯などを参考にする
* 負荷が高い状態がどれだけ続くのかということも業務諸元から明確にする

