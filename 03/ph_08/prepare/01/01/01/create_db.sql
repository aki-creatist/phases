--Wordpress用のDBの作成
--SQL文は慣例的に大文字で表しているが、小文字で入力しても問題ない
--それぞれの行を入力するごとに「Query OK」と表示されれば成功
--SQL文は行末に「;」が必要。「;」を入力するまでは、行の途中で改行しても構わない

--DBサーバーのrootユーザにパスワードを設定する
set password for root@localhost=password('p@ssword');

--DBの作成
CREATE DATABASE wordpressdb;
--このデータベースを管理するユーザーとしてwpuser (パスワードはpassw0d）を作成
GRANT ALL PRIVILEGES ON wordpressdb.* TO 'wpuser'@'localhost' IDENTIFIED BY 'passw0rd';
FLUSH PRIVILEGES;

--MySQLコマンドを終了
EXIT