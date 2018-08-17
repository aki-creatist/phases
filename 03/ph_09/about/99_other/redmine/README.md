# Redmine

## コンテナ起動

```bash
docker-compose up -d
```

## 設定

* 以下にアクセス
    * http://localhost:4444
        * 初期ログインデータ
            * `ID' admin
            * `PW` admin
### パスワードの変更

* 適当なものに変更
    * `ID` admin
    * `PW` adminadmin

### パラメータの設定

* `管理` に移動
    * `/admin`
* `新しいステータス` に移動
    * `/issue_statuses/new`
        * 新規
        * 処理中
        * 処理済
* `新しいトラッカー`
    * `/trackers/new`
        * タスク
* `ワークフロー`
    * `/workflows/edit`
* `設定`
    * `settings?tab=general`
        * テキスト書式
            * `Markdown`

## DB Back UP

```bash
docker exec -it redmine_db_1 bash
mysqldump -u root -ppassword -h localhost -t redmine > /var/backups/database.sql
```

## チケット起票のフロー

『新しいチケット』メニューから作成する

### チケットの粒度

参画しているプロジェクト、または自身の定める粒度で分ける

* 環境による分類
    * Develop/Test/Staging/Production
* トラッカーによる分類
    * インブラ構築依頼/環境の設定依頼/タスク
* etc...

### チケットを分ける

* Test/インフラ構築依頼
* Test/環境設定依頼
* Staging/インフラ構築依頼
* Staging/環境設定依頼

### 1.トラッカーの指定

依頼内容に合わせて選択をする
トラッカーを作成する場合、大まかな分類、かつ少数でよい

### 2.共通項目の指定

入力必須項目を入力

* 担当者
* 優先度

### 3.(トラッカー特有項目の入力)

各トラッカー特有の入力項目がある場合には入力をする

### 4.起票

以下の点を再度確認し、起票する

* ステータスが新規(Created)
* 担当者(Assignee)が依頼先を向いている
* 進捗率(% Done)が`0`
* 必要な情報が明記されている

## チケット運用フロー

### 1.起票完了から着手するまで

起票されたチケットを担当する人が着手する際、『`処理中 (In Progress)`』に変更

チームで受け取った場合、担当者が決まった時点で進捗率を`20%`に変更

### 2.着手から作業完了するまで

* 依頼者
    * 作業の詳細をコメントに記載
    * 作業が完了したら担当者を起票者に戻し、ステータスを`処理済み(Solved)`に変更
    * 調整や追加のヒアリングがあるなどする場合、質問したい相手に担当者を変更
    * 進捗率を`80%`に変更する
* 被依頼者
    * `処理済み`かつ、担当者が自らを向いたチケットが戻ってくるのを待つ
    * 質問が返ってきた場合には応答し、担当者を作業者に向け直す
    * 結果に問題がなければ進捗率を`100%`に変更し、ステータスを`完了`にする
    * 結果に問題があれば進捗率を`60%`に変更し、担当者を作業者に戻す

## チケット項目の概要

### 題名(Subject)

依頼内容が判別可能にする(プレフィックスを付けるなど工夫する)

### 説明(Status)

* 新規 (Created)：未着手の状態
* 処理中 (In Progress)：進行中の状態
* 処理済み (Solved)：作業が完了し、チェックを待っている状態
* 保留 (Pending)：保留されている状態
* 完了 (Done)：クローズされた状態

### 担当者 (Assignee)

起票時点では自身ではなく担当を以来する相手に向ける

### 優先度

* 緊急 (Urgent)：本番環境での障害など、緊急に対応しなければ損害となるもの
* 高い (High)：リリース直前の変更などスケジュールに影響を及ぼすもの
* 通常 (Normal)：通常の対応でよいもの
* 低い (Low)：対応が遅くなっても構わないもの

### 進捗率 (% Done)

* 0%  :起票中、起票直後、未着手
* 20% :着手中
* 60% :作業完了後に差し戻しが行われた状態
* 80% :作業完了後にチェック待ちをしている状態や、レビュアのレビュー中
* 100%:クローズされた状態

## 準備

```yaml
version: '2'

services:
  redmine:
    image: redmine
    ports:
      - 4444:3000
    environment:
      REDMINE_DB_MYSQL: db
      REDMINE_DB_PASSWORD: password
    depends_on:
      - db
    restart: always

  db:
    image: mariadb
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: redmine
    command: mysqld --character-set-server=utf8 --collation-server=utf8_unicode_ci
    volumes_from:
      - datastore
    restart: always

  datastore:
    image: busybox
    volumes:
      - redmine-data:/var/lib/mysql
      - ./backups:/var/backups/
volumes:
  redmine-data:
    driver: local
```