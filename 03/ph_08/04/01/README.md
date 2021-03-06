## 1-1 セキュリティ対策の責任は誰にあるのか

* システムのセキュリティレベルは鎖のようなものであって、一番弱い部分がそのシステムのセキュリティレベル
* 情報漏えいの原因はSQLインジェクションの対策漏れである
* Webアプリケーションのセキュリティ対策については、発注者からの明確な要請がなくとも、専門家である開発者側が積極的に検討・提言しなければならない

### Webアプリケーションのセキュリティ要件を定義する

* 発注者
    * 運用するシステムが依拠する業界基準・ルールを理解する
    * 同一業界でのセキュリティ事故事例などを調べる
    * 仕様変更などの手続きについては、開発会社とあらかじめ合意しておく
* 受注者
    * 顧客からの明確な要件提示がなくともセキュリティ対策を非機能要件として提示する
    * 脆弱性に起因する品質問題は自社および顧客企業への経営ダメージが大きいことを理解する

#### ■安全なウェブサイトの作り方(IPA)

* 届出件数の多かった脆弱性や攻撃による影響度が大きい脆弱性を取り上げ、開発者や運営側が適切なセキュリティを考慮したWebサイトを作成するための資料
* 別冊としてSQLインジェクションについての解説と対策をまとめた安全なSQLの呼び出し方

#### ■Webシステム/Webアプリケーションセキュリティ要件書 OWASP Edition(OWASP)

* OWASP（The Open Web Application Security Project）は、信頼できるアプリケーションの開発・購入・運用の推進を目的として設立されたオープンなコミュニティ

#### ■情報システム・モデル取引・契約書（経済産業省）

* 契約事項の明確化やユーザー・ベンダー間の取引関係などの可視化を目的とした、情報サービスのシステム取引にかかわるユーザー・ベンダー間のモデル取引および契約書

## 1-2 なぜ安全でないWebシステムができるのか

* 設計者、開発者にセキュリティ対策に関する知識が乏しい
* Webアプリケーションの脆弱性を突いた攻撃手法は、巧妙化・複雑化してきている

### スケジュールが短く余裕がない

* そもそもスケジュールが短く、工数も少ないので余裕がない
* 設計や実装のレビューが十分にできていない(スケジュールの問題と、レビュアのスキルの問題)
* セキュリティに関するテストが十分に実施されていない(正常系のテストが優先)
* コーディング規約がなく、個人任せになっている(レベルがバラバラ)

## 品質管理の三つの考え方

* 近代的な品質管理の考え方には、以下の三つの要素
    * 「品質は検査で保証するものではなく、設計段階から作りこんでいくもの」(Quality is planned in,not inspected in)。
    * 「プロダクト(製品)の品質は、母体組織の品質に依存する」
    * 「プロダクト(製品)の品質は（母体組織の品質に依存するのであれば）、経営課題であり、マネジメントが積極的にコミットしなければならない（現場任せにしてはならない）」

### フェーズごとの検討

* 要件定義
    * 認証
    * 認可(アクセス制御)
    * 暗号化方針
* 設計
    * セッション管理
    * HTTPSの利用
    * CSRF対策
* 開発
    * SQLインジェクション対策
        * webアプリケーションの入力画面に開発者が予期していない文字列を入力すると、SQLコマンドをDBに発行できてしまうSQLアプリケーションの脆弱性のこと。
        * 対策としてはバインド機構を用いるか、文字列のエスケープ処理を施すなどの方法がある。
    * OSコマンドインジェクション対策
    * クロスサイトスクリプティング対策
        * 悪意のあるスクリプト(通常はWebブラウザー上で動作するJS)がユーザーのWebブラウザー上で動作してしまう脆弱性。
            * 攻撃者が外部に用意したサイトに、悪意のあるスクリプトをパラメータとして含むリンクを用意し、そのリンクを被害者が送信することによって起こる。
            * 主たる原因は、WebブラウザーへのHTML出力の際に、HTMLの特殊文字を適切に変換(HTMLエンコード)していないこと。
            * 外部からの入力パラメータだけでなく、WebアプリケーションからHTMLを出力する際には、テキストとして出力したい値部分についてはHTMLエンコーディングを行う必要がある。
* テスト
    * セキュリティに関するテストを実施する

### 1-4 ライブラリやコンポーネントを狙った攻撃

* 利用しているライブラリやフレームワークに関する情報を把握し、管理する
* 利用しているライブラリやフレームワークにアップデートがないか情報収集する
* 定期的なパッチマネジメントを計画する(脆弱性に関するパッチでき汪は迅速に対応する)
* パッチ適応による影響範囲を特定し、十分にテストしてから適応する

### 対策の第一歩は情報の整理から

* 対策としては、まず自社のWebアプリケーションで利用しているライブラリやフレームワークの情報を整理する
    * どのようなライブラリやフレームワークを使用しているか
    * 提供しているベンダーはどこか
    * 利用しているバージョンは何か
    * どこからダウンロード(提供)されたものを利用しているか
    * インストール方法

## 第1章のまとめ

### セキュリティ対策の原因は誰にあるのか

* Webアプリケーションのセキュリティ対策は、発注者からの明確な要請がなくとも、受注者側(開発会社)からの積極的な検討、提言が求められている
* 発注者側も、セキュリティ対策について積極的に開発会社側と協議する責務がある
* 要件定義・基本設計フェーズでは、非機能要件としてのセキュリティ対策は後回しにされがち。自社にガイドラインが無ければ、IPAやOWASPのガイドラインを活用する

### なぜ安全でないWebシステムができるのか

* 品質は検査で保証するものでなく、設計段階から作りこんでいくもの。テストフェーズのセキュリティ検査だけに頼らず、上流工程からセキュリティ品質を作りこんでいく
* 「プロダクトの品質は、母体組織の品質に依存する」。開発会社は、現場任せにせず、組織を挙げてプロセスの改善や技術者の教育に取り組む必要がある

### Webアプリケーションの脆弱性を突いた攻撃の傾向

* IPAへの届け出では、「SQLインジェクション」「クロスサイトスクリプティング」が全体の7割を占める。「対策漏れ」が起きてしまう理由としては、「開発者の知識不足、理解不足」「ケアレスミス」「テスト（レビュー）漏れ」が考えられる
* Webアプリケーションの脆弱性が原因のインシデントでは、復旧に時間がかかる
* 過去に一度被害を受けたWebサイトは、改修後も継続して攻撃にさらされる。最初から安全に設計・開発する必要がある

### ライブラリやコンポーネントを狙った攻撃

* Webアプリケーションは多数のフレームワークやライブラリで構成されている。オープンソースのフレームワークやライブラリに脆弱性が見つかった場合は、無差別に攻撃される可能性がある
* 利用するライブラリやフレームワークを最新の状態に維持していくためには、「利用しているライブラリの把握」「脆弱性情報の収集」「パッチマネジメントの計画(迅速な適応)」を運用計画として検討しておく
* 本番環境へのパッチ適用までに時間がかかる場合には、IDSやWAFが攻撃の緩和に有効