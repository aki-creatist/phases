# ディレクトリ操作

## ディレクトリを作成する

* `mkdir`コマンド
    * Make DIRectory

```bash
mkdir	[-p] ディレクトリ名
```

```bash
# contactというディレクトリを作成
mkdir contact
# 確認
ls
```

* サブディレクトリを作成する場合は注意
    * 先に親ディレクトリを作成してから、その下のサブディレクトリを作成する

のにとエラーになる

```bash
# 失敗する例
ls            # dirディレクトリがまだ存在しない
mkdir dir/sub # subディレクトリを作成しようする
mkdir: dir: No such file or directory # エラーメッセージ (そのようなファイルやディレクトリはありません。)

# 正しい例
mkdir dir     # dirディレクトリを作成
mkdir dir/sub # dirディレクトリの下にsubディレクトリを作成
```

### サブディレクトリまで一気に作成する

`-p`オプションを指定すれば存在しない階層も含めて一気に作成可能

```bash
mkdir -p dir/sub
```
