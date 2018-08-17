#!/bin/bash

mysql -u root -p
#パスワードを求められたら何も入力せずにEnter

# GitBashを使用している場合にはGitBashで以下を実行
# どこからでも入れるように、まずはパスを通す
export PATH=$PATH:/c/xampp/mysql/bin
winpty /c/xampp/mysql/bin/mysql -u root -p
#Enter password: // Enterを押下