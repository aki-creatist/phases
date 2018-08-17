# 準備

## Bootstrapのインストール

* [公式サイト](http://getbootstrap.com/)
    * Download bootstrapボタンをクリック
    * bootstrap[バージョン番号].zipをダウンロード
* ダウンロードしたファイル群のうちWebページを作る際に必要なのは、「dist」フォルダのみ

```bash
mkdir first-bootstrap
cp -r bootstrap/dist/css first-bootstrap
cp -r bootstrap/dist/fonts first-bootstrap
cp -r bootstrap/dist/js first-bootstrap
cd first-bootstrap
touch index.html
```

```text
first-bootstrap
├── index.html
├── css
├── fonts
└── js
```