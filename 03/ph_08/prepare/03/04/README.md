# Selenium

## Mac

## ***.env

* https://qiita.com/luckypool/items/f1e756e9d3e9786ad9ea
* https://github.com/riywo/anyenv
* https://qiita.com/h_digitalhearts/items/a4cbff763b9ee8a7879a

### anyenv

```bash
# anyenvをGitHubからダウンロード
git clone https://github.com/riywo/anyenv ~/.anyenv
```

* .bash_profileに下記を追記

```text
#anyenv
if [ -d $HOME/.anyenv ] ; then

    # $PATHにディレクトリ名を格納
    export PATH="$HOME/.anyenv/bin:$PATH"
    
    # 初期設定を行うコマンドを追記
    eval "$(anyenv init -)"
    
fi
```

```bash
source ~/.bash_profile
# シェルを再起動
exec $SHELL -l
```

```bash
# 各種コマンド表示
anyenv
# インストールされているenvを表示
anyenv versions
# インストール可能なリスト
anyenv install --list
```

### ***env

```bash
# インストール
anyenv install ${TARGET}env
# 反映
exec ${SHELL} -l
# ***envのコマンドの説明を表示
${TARGET}env
```

### 目的の言語をインストール

```bash
# installコマンドの説明を表示
${TARGET}env install
# install可能なバージョンを表示
${TARGET}env install --list
# 目的のバージョンをインストール
${TARGET}env install ${VERSION}
# インストールできたか確認
${TARGET}env versions
# バージョンを選択
${TARGET}env global ${VERSION}
```

## インストール

```bash
anyenv install ndenv
anyenv install rbenv
anyenv install pyenv
anyenv install phpenv
```

```bash
ndenv install v9.11.1
rbenv install 2.5.0
pyenv install 3.5.0
phpenv install 7.2.0
# 確認
anyenv versions
```

```bash
ndenv global v9.11.1
rbenv global 2.5.0
pyenv global 3.5.0
phpenv global 7.2.0
# 確認
anyenv versions
```

```bash
node -v
ruby -v
python --version
php -v
```

## 対話式

```bash
# node
node
# ruby
irb
# python
python
```

## node

```bash
node
console.log("hello world");
.help # 使えるコマンドを参照
.exit # 対話環境から抜ける
```

## ruby

```bash
irb
puts "hello world"
exit
```

## python

```bash
python
"hello world"
exit()
```

## php

```bash
php -a
echo "hello world";
```

# selenium

```bash
brew install chromedriver
```


```bash
# node
npm -g install selenium-webdriver
```

* https://qiita.com/edo_m18/items/ba7d8a95818e9c0552d9

```bash
# ruby
gem install selenium-webdriver
```

```bash
irb
require "selenium-webdriver"

# Firefox用のドライバを使う
driver = Selenium::WebDriver.for :firefox

# Googleにアクセス
driver.navigate.to "http://google.com"

# `q`というnameを持つ要素を取得
element = driver.find_element(:name, 'q')

# `Hello WebDriver!`という文字を、上記で取得したinput要素に入力
element.send_keys "Hello WebDriver!"

# submitを実行する（つまり検索する）
element.submit

# 表示されたページのタイトルをコンソールに出力
puts driver.title

# テストを終了する（ブラウザを終了させる）
driver.quit
```

* https://qiita.com/motoki1990/items/a59a09c5966ce52128be

```bash
# python
pip install selenium
```

```bash
python

from selenium import webdriver
#Chromeを操作
driver = webdriver.Chrome()

#Firefoxを操作
driver = webdriver.Firefox()

// フルパスを指定
driver.get("https://www.yahoo.co.jp/");

from selenium.webdriver.common.by import By
#単一の要素を取得
driver.find_element_by_xpath("//*[@id='srchtxt']")
#このような指定方法もある
driver.find_element(By.XPATH, "//*[@id='srchtxt']")

#複数の要素を取得する場合
driver.find_elements_by_xpath("//*[@class='srchtxt']")
```
