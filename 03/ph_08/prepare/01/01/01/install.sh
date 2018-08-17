#MySQLのインストール
yum -y install mariadb mariadb-server

#DBを開始する
systemctl start mariadb.service

#DBが動作しているか確認する
systemctl is-active mariadb.service
#active

#次回から自動的にMariaDBを起動する
systemctl enable mariadb.service
#active

#PHPをインストール
su
#パスワード:
cd ~

#php: パッケージはPHP本体
#php-mbstring: PHPで日本語などのマルチバイト文字を扱うためのパッケージ
#php-gd: PHPで画像ライブラリを扱うためのパッケージ
#php-mysql: MariaDB/MySQLを連携するパッケージ
yum -y install php php-mbstring php-gd php-mysql

#PHPのバージョンを確認する
php --version

#この時点では、まだApacheとPHPが連携できていない
#ApacheはPHPがインストールされたことを知らない
#ApacheがPHPプログラムを実行できるよう、Apacheを再起動
#(ApacheとPHPを一緒にインストールした場合は、Apacheの再起動は不要)
systemctl restart httpd.service

#PHPの動作を確認するテストプログラムを作成
sudo echo "<?php echo phpinfo() ?>" > /var/www/html/test.php

