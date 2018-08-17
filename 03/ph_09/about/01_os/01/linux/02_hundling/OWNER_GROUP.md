# 所有者/所有グループを操作する

## 前提

* Linuxはマルチユーザーシステム
    * ファイルを作成すると、そのファイルの所有者と所有グループが設定される
    * 通常、ファイルを作成したユーザーがファイルの所有者となる
        * ユーザーを作成すると、そのユーザー専用のグループが作られる
    * ユーザーが所属するグループがファイルの所有グループとなる
    
## ファイルの所有者と所有グループを確認

* `ls -l`
    * `-l` オプションで詳細表示
    * `-d` オプション
        * 指定したディレクトリ内ではなく、そのディレクトリそのものの情報を表示する
        
以下の例ではファイルの所有者はstudent、所有グループはstudentグループ

```bash
ls -l ファイル名
- rw-r--r-- 1 student student 158 1月 1 12:00 hosts
```

```bash
# ディレクトリの詳細情報を表示
ls -ld ディレクトリ
d rwxr-xr-x 2 teacher root 158 1月 1 12:00 example
```

## 所有者を変更する

* `chown` コマンド
    * CHange OWNer の略
* 所有者や所有グループは変更可能
* 変更できるのはrootユーザーだけ

```bash
chown	[-R] 所有者	ファイル名やディレクトリ名
```

次の例では、ownsampleファイルの所有者をteacherユーザーに変更

```text
[root@centos7 ~]# chown teacher example.txt
[root@centos7 ~]# ls -l
- rw-r--r-- 1 teacher root 158 1月 1 12:00 example
```

次の例では、dataディレクトリの所有者をteacherユーザーに変更

```text
[root@centos7 ~]# chown teacher exampledir # 中にあるファイルやディレクトリの所有者は変更されない
[root@centos7 ~]# ls -dl exampledir
d rwxr-xr-x 2 teacher root 158 1月 1 12:00 example
```

### ディレクトリ内も丸ごと変更する

* `R` オプション
    * ディレクトリ内のファイルも含めて丸ごと変更する

```bash
chgrp -R ディレクトリ
```

## 所有グループを変更

* `chgrp` コマンド

```bash
chgrp [-R] 所有者グループ ファイル名やディレクトリ名
```

次の例では、dataディレクトリの所有グループをschoolに変更

```text
[root@centos7 ~]# chgrp exampledir
[root@centos7 ~]# ls -dl exampledir
d rwxr-xr-x 2 teacher school 158 1月 1 12:00 example
```

## 所有者と所有グループを同時に変更

* chownコマンドを使って、所有者と所有グループを同時に変更可能
    * `所有者：所有グループ` という形式で指定

次の例では、 sample.txtファイルの所有者をteacher、所有グループをschoolに変更

```text
[root@centos7 ~]# chown teacher:school sample.txt
[root@centos7 ~]# ls -l sample.txt
d rwxr-xr-x 1 teacher school 158 1月 1 12:00 sample.txt
```

