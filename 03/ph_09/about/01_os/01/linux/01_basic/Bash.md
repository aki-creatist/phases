# シェル

[概要](https://github.com/aki-creatist/about/blob/master/02_server/SHELL.md)

## シェルとコマンド操作

* `type` コマンド
    * コマンドが内部コマンドかそうでないかを調べる
    * 内部コマンドの場合は「シェル組み込み関数です」と表示される

## どのシェルが使われているか確認

* `ps` コマンド
    * どのシェルが使われているか確認
    * Linuxでは`bash`というシェルが一般的
        * CentOSでもbashが標準で使われる

```bash
ps
```

### シェルの変更

* 実行したいシェルの名前を入力
* `exit`で戻る
* ログインしたときに使われるデフォルトのシェルは、`/etc/passwd`ファイルで設定

```bash
#shに変更
sh
#bashに変更
bash
#元のシェルに戻るにはexitコマンド
```

### 実行シェルを選択

bashで書かれたスクリプトを実行するには以下のようにする

```bash
bash 実行ファイル.sh
```

### ログインシェルを選択

Dockerコンテナに入る際にシェルを選択できる

```bash
docker exec -it コンテナ名 sh
docker exec -it コンテナ名 bash
```

## Bashのバージョンアップ

Bashのバージョンが３系の場合、４系に変更する

```bash
bash --version     # 3.2.51(1)-release
echo $BASH_VERSION # 3.2.51(1)-release
brew install bash
sudo vim /etc/shells # 一番下に/usr/local/bin/bashを追記
chsh -s /usr/local/bin/bash
# ターミナルを再起動
echo $BASH_VERSION # 4.3.18(1)-release
bash --version     # 4.3.18(1)-release
```

確認

```bash
echo a_{01..10} # ３系は以下の結果
#a_1 a_2 a_3 a_4 a_5 a_6 a_7 a_8 a_9 a_10
echo a_{01..10} # ４系は以下の結果
#a_01 a_02 a_03 a_04 a_05 a_06 a_07 a_08 a_09 a_1
```

```bash
LOCALE=JA
echo ${LOCALE,,} # ３系は以下の結果
# bash: ${LOCALE,,}: bad substitution
echo ${LOCALE,,} # ４系は以下の結果
# ja                
```
