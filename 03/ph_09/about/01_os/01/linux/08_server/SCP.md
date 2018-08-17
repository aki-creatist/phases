# SSHでファイルコピーする

* SSHでネットワーク経由でファイルをコピーする

## SCP

* `scp` コマンド
    * ファイルをリモートからローカルにコピー
    * ファイルをローカルからリモートにコピー

```bash
scp [-r] コピー元 コピー先
```

コピー先の指定方法

```bash
[ユーザー名@]ホスト:][ファイル名]
```

リモートの書式の例

* `exam.jp:sample.txt`
    * ホストexam.jpのホームディレクトリにあるsample.txt
* `exam.jp/tmp/sample.txt`
    * ホストexam.jpの/tmp/sample.txt
* `foo@exam.jp.sample.txt`
    * ホストexam.jpの/home/foo/sample.txt
* `sample.txt` (ファイル名だけを指定)
    * ローカルホストのファイルを指定したとみなされる

### ローカル/リモート

* `ホスト:`
    * ファイル名の前に `ホスト:`
    * リモートホストのファイルを指定したとみなされる

```bash
#ローカルホストからリモートホストへのコピー
#カレントディレクトリにあるsample.txtを、192.168.11.5のホストの/tmpディレクトリ以下にコピー
scp sample.txt 192.168.11.5:/tmp
#ローカルホストからリモートホストへのファイルのコピー
#/etc/resolv.confファイルを、ホストexam.jpのuserユーザーのホームディレクトリ以下にコピー
#コピー先のディレクトリ名を指定しない場合は、ホームディレクトリ以下を指定したのと同じものとみなされる
scp /etc/resolv.conf user@exam.jp:
#リモートホストからローカルホストへのファイルのコピー
#ホストexam.jpのuserユーザーのホームディレクトリ以下にあるsample.txtをカレントディレクトリ以下にコピー
scp user@exam.jp:sample .
```

SSHを利用すると、ユーザーAのホームディレクトリにあるファイルをユーザーBのホームディレクトリにコピーすることも可能

```bash
#studentユーザーのホームディレクトリにあるファイルsampleを、
#teacherユーザーのホームディレクトリにコピーする
#studentユーザーとして実行
scp sample teacher@localhost:
```

teacherユーザー側で同じことをする

```bash
#teacherのファイルをstudentのホームディレクトリにコピー
#studentとして実行
scp student@localhost:sample .
```
