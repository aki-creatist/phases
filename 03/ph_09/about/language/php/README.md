# PHP

* [概要](00_about)
* [ヘッダー](01)
* [名前空間](03)
* [フレームワーク](04)

## パッケージ管理

* 便利なパッケージ

```bash
composer require phpunit/phpunit --dev
composer require friendsofcake/search
```

* 開発時のみ必要な依存モジュールはrequire-dev に指定
* composer installのときはインストールされずに以下のように--devを指定した場合にインストールされる

```bash
composer update --dev
```