# システムレベルのユースケース

* `システム`のシステムの利害関係者に対しての振る舞いを表現したもの
    * 利害関係者: ユーザー(アクターと呼ぶ)
        * システムの利用者だけでなく、外部システムなども含む
    * `振る舞い`: システムの動的な側面
        * `システムの挙動`
    * 利害関係者とシステム間でどのようなやり取りが行われていくかを順序に沿ったシナリオで表現
    * 細かい視点で書かれる
* `人`がどのように`コンピュータ`を使用するか、を表現したもの
* システムの動的な振る舞いを表す
* 様々な概念が登場する
    * 会員、注文、配送、返品etc
    * これらの概念の関連は、システムユースケースでは触れない
* ユーザー(アクター)がシステムを使って何らかの目的を達成する単位が1つのユースケース
    * このユースケースは、仕事が完了する単位にもなる
    * 目的を達成する単位: 1人の人間が中断なしに行える仕事
        * その仕事が終わったらコーヒーブレイクできるくらい
        * それが終わるとひと息入れられる仕事の単位
        * 目安は30分以内くらい
* シナリオ完了＝1つのユーザー目的の達成 

## 記述事項

システムユースケースは**システムの要件**を記述する

* 作成者
* 作成日
* ユースケース名(必須)
* 主アクター(必須)
* 事前条件
    * ユースケースが始まる前に真であると保証されていることを記述
* トリガー
    * ユースケースを実行するイベントを記述
        * 主シナリオに含まれないこともあれば、主シナリオの最初のステップになることもある
* 主シナリオ(必須)
    * シナリオは文章ごとにステップが分ける
    * 順番に数字が振られ、主アクターとシステムが、処理を行う
* 拡張シナリオ(必須)
    * シナリオは、途中で失敗することがある
        * 拡張シナリオには、この決済に失敗した場合などを書く
* 事後条件
    * ユースケースの結果として満たされていることを記述
        * 最低保証と成功時保証がある
* ビジネスルール
    * ユースケースを捕捉するものとして記述する
        * 企業毎の業務ルールなど
            * 企業がその業務を遂行するには、従わなければならないルールがある

[サンプル](system_use_case.xlsx)

## 管理

* 抽出したビジネスルールは、ビジネスルール一覧を作成して管理
* 抽出したユースケースは、ユースケース一覧を作成して管理

## TODO

* コンピュータを含めた実効単位業務関連図(＝行動シナリオ)を、各ユースケース(＝システムレベルのユースケース)に分解

## 概要
 
* [システムユースケースの抽出方法](01)
* [システムユースケースの抽出](02)

* 画面遷移や具体的なシステムの実現方法はユースケースでは言及しない
    * 要件定義の領域であるため

