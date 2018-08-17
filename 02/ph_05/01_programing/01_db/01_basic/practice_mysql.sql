--mysqlにログイン
xampp¥mysql¥bin¥mysql -u root -p

--管理者として接続
mysql -u root -p

--データベースの作成
CREATE DATABASE sampledb character set utf8 collate utf8_general_ci;

--データベースの作成確認
SHOW DATABASES;

--ユーザーの存在確認
SELECT USER FROM mysql.user;

--ユーザーの作成
CREATE USER 'sample'@'localhost' identified by 'password';

--ユーザーの存在確認
SELECT USER FROM mysql.user;

--権限の付与
GRANT all privileges ON sampledb.* TO 'sample'@'localhost';

--権限の確認
SHOW GRANTS for 'sample'@'localhost';

--パターン２(２周目で利用してください)
GRANT SELECT,UPDATE,INSERT,DELETE ON `sampledb`.* TO 'sample'@'localhost';

--権限の反映
FLUSH PRIVILEGES;

--rootユーザーを抜ける
exit

--ユーザーの切り替え
mysql -u sample -p

--データベースの切り替え
use sampledb;

--テーブルの作成
CREATE TABLE member(
id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
last_name varchar(50),
first_name varchar(50),
PRIMARY KEY(id)
);

--テーブルの作成
SHOW fields FROM member;

--テーブルの削除
DROP TABLE member;

--テーブルの作成
CREATE TABLE member(
id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
last_name varchar(50),
first_name varchar(50),
age TINYINT UNSIGNED,
PRIMARY KEY(id)
);

--テーブルの作成
SHOW fields FROM member;

--データの挿入(データ内容は自由)
INSERT  INTO member (last_name, first_name, age) VALUES('test1','test1', 30);
INSERT  INTO member (last_name, first_name, age) VALUES('test2','test2', 35);
INSERT  INTO member (last_name, first_name, age) VALUES('test3','test3', 25);
INSERT  INTO member (last_name, first_name, age) VALUES('test4','test4', 34);
INSERT  INTO member (last_name, first_name, age) VALUES('test5','test5', 33);


--条件で検索する
SELECT * FROM member WHERE age > 30;

--first_nameだけ表示する
SELECT first_name FROM member WHERE age > 30;

--データの更新
UPDATE member SET age = 20 WHERE id = 4;

--データの削除
DELETE FROM member where id = 5;

--テーブルの削除
DROP TABLE member;

--テーブル削除確認
SHOW TABLES;

--sampledbの存在を確認する
SHOW DATABASES;

--sampledbを削除する
DROP DATABASE sampledb;

--sampledbの存在を再度確認する
SHOW DATABASES;

--ユーザーsampleから抜ける
quit

--rootで入り直す
mysql -u root -p

--sampledbが消えていることを確認する
SHOW DATABASES;

--ユーザーの存在確認
SELECT USER FROM mysql.user;

--ユーザーの削除
DROP USER 'sample'@'localhost';

--ユーザーの存在を再確認
SELECT USER from mysql.user;

