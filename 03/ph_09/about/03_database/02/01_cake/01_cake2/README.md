# テーブル自動生成

## Schemaファイルからテーブルを作成する</h2>

* スキーマシェルからテーブルを生成
* スキーマシェルの実行はGit Bashから行う

```bash
cd /c/xampp/htdocs¥cake2
#スキーマファイルからテーブルを作成する
app/Console/cake schema create
```

```text
welcome to CakePHP v2.9.8 Console
-------------------------------------
App : app
Path: C:\xampp\htdocs\cake2\app\
-------------------------------------
Cake Schema Shell
-------------------------------------
The following table(s) will be dropped.
meeting_rooms
meetings
members
meetings_members
Are you sure you want to drop the table(s)? (y/n)
```

* 上記の質問にyと答える

```text
The following table(s) will be created.
meeting_rooms
meetings
members
meetings_members
Are you sure you want to create the table(s)? (y/n)
```

* こちらもyと答える
    * 下記のようにテーブルが自動生成される

```text
Creating table(s)
meeting_rooms updated.
meetings updated.
members updated.
meetings_members updated.
End create.
```

* 以上のように表示されれば正常終了し、テーブルの作成は終了
* 以下のようなエラーメッセージが表示されることがある
    * ファイルの置き場所が間違っている

```text
welcome to CakePHP v2.9.8 Console
-------------------------------------
App : app
Path: C:\xampp\htdocs\cake2\app\
-------------------------------------
Cake Schema Shell
-------------------------------------
Error: The chosen schema could not be loaded. Attempted to load:
- file: C:\xampp\htdocs\cake2\app\Config\Schema\schema.php
- name: App
```

* schemaを実行しようとすると、`phpが見つかりません`と言った趣旨のエラーが出ることがある
* そこでPHPに対してパスを設定する

## Linuxの設定

```bash
FILE=app/Console/cake
OLD='exec php -q "$CONSELE"/cake.php -working "$APP" "$@"'
NEW='exec /opt/lampp/bin/php -q "$CONSELE"/cake.php -working "$APP" "$@"'
sed -ie "s/${OLD}/${NEW}/g" ${FILE}
```

## Windowsの設定

```bash
#パスの設定
export PATH=$PATH:/c/xampp/php
```

## 既存のテーブルからスキーマファイルを作る

* CakePHPには既存のテーブルからスキーマファイルを生成するコマンドも用意されている
    * DDLを書いた方が早いという場合のため
    
```bash
#これで接続先DBの、全テーブルのスキーマファイル(app¥Config¥Schema¥schema.php)を作ってくれる
app¥Console¥cake schema generate -f
```

## スキーマファイルからSQLを作って画面表示

* スキーマファイルはDDLを完全に再現可能ではない
* DBの性能を引き出すためには、一旦SQL文の形で出力して、それを手で加工したい場合がある
    * CakePHPにはスキーマファイルからSQLを組み立てるだけ組み立てる
        * 実行はせずに画面に表示する

```bash
#これでスキーマファイル(app¥Config¥Schema¥shema.php)の内容からDDLを生成して画面に表示してくれる
app¥Console¥cake schema dump
```

## スキーマファイルの変更をDBに反映

* 最初に作ったスキーマファイルを１回も修正せずに完成することはまずない
* スキーマファイルを修正したら、以下のコマンドを実行する
    * スキーマファイルの内容(新)と現在のDBテーブル定義(旧)とを比較
    * 修正内容をDBに反映するSQL文(ALTER TABLE)を自動生成して更新してくれる

```bash
app¥Console¥cake schema update
```

