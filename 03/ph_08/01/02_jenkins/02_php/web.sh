#!/bin/bash

#Local
source ~/.bashrc
web1

#Container - web
/etc/init.d/ssh restart
passwd jenkins #test

#Container - jenkins
jenkins
ssh web1
# 確認
# php -v