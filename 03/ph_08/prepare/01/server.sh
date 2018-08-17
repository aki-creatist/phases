#!/bin/bash

# レンタルサーバでPHP7のセッティング
# 現在設定されているパスを消去し、php7.1までのパスを引く

ssh アカウント@サーバ -p 2222
php -v
#PHP 5.5.35 (cli) // 筆者の場合は5.5.35だった

## サーバ内の用意されているバージョンを確認
ls usr/local/
#bin/    perl/   php/    php5.3/ php5.4/ php5.5/ php5.6/ php7.1/ python/ ruby/
echo $PATH
#/usr/local/bin:/bin:/usr/bin:

unset PATH # $は付けない
echo $PATH # 削除されていることを確認
php -v
#-bash: php: No such file or directory # PHPまでのパスは削除されている
export PATH=$PATH:/usr/local/php7.1/bin/ # 新たにパスを設定する
php -v # 再度確認をする
#PHP 7.1.5 (cli)

cd ~
ls
#-bash: ls: command not found

# 先ほどパスを全て削除してしまったので、消してしまったパスのうち必要なものを改めて追加
# vimが使用できるように/usr/binを、lsコマンドを使用できるように/binを追加する
export PATH=$PATH:/usr/bin/:/bin/
echo $PATH
#:/usr/local/php7.1/bin/:/usr/bin/:/bin/
php -v
#PHP 7.1.5

# この設定の仕方の場合、再度ログインした際にはリセットされる
# 通常は~/.bashrcなどに記述をする
# ロリポップは~./bashrcが効かない
# 効かないにしても~/.bashrcを作成しておいて、コピペで設定できるようにしておくと便利
vim ~/.bashrc
#export PATH=$PATH:/usr/local/php7.1/bin/:/usr/bin:/bin/

# Laravel5.4のphp artisanなどは現状のロリポップはPHP7でしか動作しないので、ログインのたびに以下の手順を行う
unset PATH
source ~/.bashrc

#気を取り直してプロジェクトを作成する
php composer.phar create-project laravel/laravel Laravel
php artisan
#最後にphp artisanと入力して無事に動けばプロジェクトの作成までが終了