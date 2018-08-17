# CakePHP

* [Controller](02)
* [Model](04)
* [ページネータ](05)
* [バリデーション](06)
* [レイアウト作成](07)

## プロジェクトの設定

### bootstrap.php

```diff
  try {
      Configure::config('default', new PhpConfig());
      Configure::load('app', 'default', false);
+     Configure::load('constants', 'default', false); // 追加(configure::read用)
  } catch (\Exception $e) {
      exit($e->getMessage() . "\n");
  }
```