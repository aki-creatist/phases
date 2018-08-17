# Host OS

MacにJenkinsをセットアップする

```bash
#インストール
brew install jenkins
#caskを入れ泣けれなばならない場合は入れて再度インストール
brew cask install caskroom/versions/java8
#jekinsをhomebrewでアップデートすると起動ファイルも更新されるためコピーする
cp -p /usr/local/opt/jenkins/*.plist ~/Library/LaunchAgents
#Portを変更する
FILE=~/Library/LaunchAgents/homebrew.mxcl.jenkins.plist
DEFAULT_PORT=8080
grep ${DEFAULT_PORT} ${FILE}
PORT_YOU_WANT_TO_CHANGE=8099
sed -ie "s/${DEFAULT_PORT}/${PORT_YOU_WANT_TO_CHANGE}/g" ${FILE}
#sedで生成されたバックアップファイルの削除
rm ${FILE}e
#自動起動の設定
launchctl load ~/Library/LaunchAgents/homebrew.mxcl.jenkins.plist
#ブラウザで起動
open -a Google\ Chrome http://localhost:8099/
```

```bash
#自動起動の解除
launchctl unload ~/Library/LaunchAgents/homebrew.mxcl.jenkins.plist
```

```bash
#停止
launchctl stop homebrew.mxcl.jenkins
#起動
launchctl start homebrew.mxcl.jenkins
```