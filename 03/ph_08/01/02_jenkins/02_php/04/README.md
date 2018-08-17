# Jobの作成

```bash
http://localhost:8090/
PORT=8090
HOST="http://localhost"
URL="${HOST}:${PORT}/view/all/newJob"
open -a Google\ Chrome ${URL}
```

* Jobの新規作成
    * LOCAL_SSH_TEST(任意のJob名)
* ビルド環境
* `リモートホストでシェルを実行`にチェック
    * プルダウンを選択
        * SSHサイト: jenkins@web1:22
    * Test用のJobを入力
        * ビルド前スクリプト: `php -v`