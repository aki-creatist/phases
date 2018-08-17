--インストール
$ brew install postgresql

--環境変数の設定
export PGDATA=/usr/local/var/postgres

--サーバー始動
$ pg_ctl start

--ログイン
$ psql postgres

--DB作成
postgres=# create database project;

--DB一覧
postgres=# \l

--ユーザ作成
postgres=# create role testuser with createdb login password 'password';

--ユーザ確認
postgres=# \du

--ログアウト
postgres=# \q

--作成したユーザでログイン
$ psql -U testuser -d project

--ログアウト
project=> \q

--ログイン
$ psql postgres

--ユーザ削除
postgres=# drop role testuser;

--DB削除
postgres=# drop database project;

--DB削除
$ pg_ctl stop
