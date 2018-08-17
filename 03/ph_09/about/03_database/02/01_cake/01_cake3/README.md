# テーブル自動生成

## migrationファイルからテーブルを作成する

```bash
bin/cake migrations migrate
```

```text
Migrating: 2017_06_05_203131_create_meeting_rooms_table
Migrated:  2017_06_05_203131_create_meeting_rooms_table
Migrating: 2017_06_05_203159_create_meetings_table
Migrated:  2017_06_05_203159_create_meetings_table
Migrating: 2017_06_05_203210_create_meetings_members_table
Migrated:  2017_06_05_203210_create_meetings_members_table
Migrating: 2017_06_05_203219_create_members_table
Migrated:  2017_06_05_203219_create_members_table
```

実行した際に、状態を確認するには以下のコマンドを利用する

```bash
#適応状況を確認
bin/cake migrations rollback
```

適応したものを元に戻すには下記のようにする

```bash
#元に戻す
bin/cake migrations rollback
```

* ロールバックは正確には『１つ前に戻す』
* そのほかには以下のようなものがある

```bash
#migrationsテーブルを作成する
#ない

#migrationを再実行してテーブルを再構築する
#ない

#全てのmigration操作を元に戻す
#ない
```
