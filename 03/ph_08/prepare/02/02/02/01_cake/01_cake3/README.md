# CakePHP3.x

```bash
cd プロジェクト
#bakeの実行(3.x)
bin/cake bake
```

* 3.xは2.xと異なり、bin/cake bakeで起動するのはヘルプ機能
* 「Available bake commands:」の下に表示されているのが、bakeに用意されているコマンド

```bash
#bakeの書式 作成したい内容のコマンドをbakeの後ろに続けて記述し実行
bin\cake bake コマンド
```

```bash
#MVCの各ファイルを全てまとめて生成する機能
bin\cake bake all
```

* 以下のようなテキストメッセージが出力される

```text
>Welcome to CakePHP v3.1.2 Console
----------------------------------------
App:src
Path: C:\Users\ユーザー名\Desktoop\samplecake\src\
PHP : 5.6.11
----------------------------------------
Bake All
----------------------------------------
Possible model names based on your database:
-members
-messages
-mydatas
-persons
Run `cake bake all [name]` to generate skeleton files.
```

* bake allで生成可能なDBのテーブル名が出力される
* `bake all`は、DBのテーブルを指定し、これに基づいてMVCを生成する
* 以下のようなテーブルを用意し、bake allを使ってソースコードを生成させる

```sql
CREATE TABLE `Samples` (
    `id`    INTEGER PRIMARY KEY AUTOINCREMENT,
    `data1` INTEGER NOT NULL,
    `data2` REAL,
    `data3` TEXT
);
```

```bash
bin¥cake bake bake all samples
```

```text
Welcome to CakePHP v3.1.2 Console
----------------------------------------
App:src
Path: C:\Users\ユーザー名\Desktoop\samplecake\src\
PHP : 5.6.11
----------------------------------------
Bake All
----------------------------------------
One moment while associations are detected.

Baking table class for Samples...
Creating....略....
```

* このような出力がされていき、しばらくすると再び入力待ち状態に戻る

## 生成ファイルの確認

```bash
ls src/
```

* テスト関連も自動生成されるため、後から一から描く必要がない
* bake allで注目すべきは、CRUDの基本機能も自動的に実装されている点
    * 単にコントローラーやモデルの基本コードが生成されているだけではない
    * `SamplesController`を見ると、５つのアクションメソッドが作成されている
    * `index`
        * テーブルの一覧データを表示(ページネーション使用)
    * `add`
        * 選択したIDのデータを詳細表示
    * `edit`
        * データの新規追加
    * `view`
        * 選択したIDのデータの編集
    * `delete`
        * 選択したIDのデータの削除

## 機能を生成する

* 機能をみる限り、meetings_membersはModel以外は不要なのでModelのみ作成する

```bash
bin/cake bake all meeting_rooms
bin/cake bake all meetings
bin/cake bake model meetings_members
bin/cake bake all members

#bakeで会議室予約システムを生成する
bin/cake bake all meeting_rooms
bin/cake bake all meetings
bin/cake bake model meetings_members
bin/cake bake all members
```

## 動作確認

* ocalhost:8765/meeting-rooms
    * もしくはlocalhost:8765/MeetingRooms
* bake allを使えば、MVCの基本を一括して作成可能
* 「既にモデルはできてる、CRUDのテンプレートだけ作りたい」というように必要な部分だけを作成したいこともある
    * これも可能

```bash
#MVCの必要な部分のみを作成

#コントローラーの作成
bin\cake bake controller 名前
#モデル(エンティティ、テーブル)の作成
bin\cake bake model 名前
#テンプレート(add,edit,index,view)の作成
bin\cake bake template 名前
```

## 注意

* MVCの一部分のみを作る場合の注意
    * アクションはindex,view,add,edit,deleteの固定
        * コントローラーやテンプレートを作成する場合、生成されるアクションは以下に固定される
        * index,view,add,edit,deleteの５種類に固定
        * 他のアクションを追加することはない
        * コントローラーの内容とは無関係に用意された５種類のテンプレートを作成するだけ
* ファイルの上書きに注意
    * 既に作成するファイルが存在する場合、bakeは「Do you want to overwrite? (y/n/a/q)」と訪ねてくる
    * `y`を入力すると、既にあるファイルを上書きして新たにファイルを作る
    * また`a`を入力すると、その後、また作成するファイルが既にあったとしても「上書きするか？」を訪ねず、無条件で全て上書きする
    * 前にあったファイルの中身は完全に失われてしまう
* 必ずデータベーステーブルを用意
    * bakeはDBに用意されているテーブルを調べ、それに基づいてファイルを生成していく
    * このため、まずDBテーブルをきちんと用意する必要がある
    * また、特にView関係は、データベーステーブルに用意さている項目情報をもとにフォームなどを生成する
        * 「適当に項目を用意しておいて、後で修正すればいいだろう」なんて考えていると、かえって面倒なことになる
        * 必ず、最初にデータベーステーブルを確定してから作業すること
