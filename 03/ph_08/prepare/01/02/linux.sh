#!/bin/bash

#Cent OS
yum install -y php-pear
yum install -y php-mysql

#Debian
apt-get install -y mysql-server
#=> password #パスワードは『password』

service mysql restart
