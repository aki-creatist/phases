# 概要

マウスポインターの移動に合わせて画像を変更する

## 構成

```bash
`-- html
    |-- image
    |   |-- close_00.png
    |   |-- close_001.png
    |   |-- open_01.png
    |   |-- open_02.png
    |   |-- open_03.png
    |   |-- open_04.png
    |   `-- open_05.png
    |-- index.html
    `-- js
        `-- jquery-3.2.1.min.js
```
## 準備

```bash
cd docker
docker-compose build
docker-compose up -d
```

以下のURLにアクセス
http://localhost:8081/

## 動作確認

画面左端から右端に向け、マウスポインタを移動させる