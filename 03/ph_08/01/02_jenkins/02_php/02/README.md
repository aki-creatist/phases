# パスワードの登録

* 種類: ユーザ名とパスワード
    * ユーザ名: jenkins
    * パスワード: test

```bash
PORT=8090
HOST="http://localhost"
FILE_PATH="credentials/store/system/domain/_/newCredentials"
URL="${HOST}:${PORT}/${FILE_PATH}"
open -a Google\ Chrome ${URL}
```