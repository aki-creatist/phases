# 名前空間

* test_a.php

```php
<?php function methodA() {} ?>
```

* test_b.php

```php
<?php function methodA() {} ?>
```

* call.php

```php
<?php
require_once 'test_a.php';
require_once 'test_b.php';

echo methodA();
```

* エラーになる

```text
Fatal error: Cannot redeclare methodA() ...
```

## 名前空間を定義する

```text
名前空間名\関数名;
名前空間名\クラス名;
```

```php
<?php
namespace a;

function methodA() {}
```

```php
<?php
namespace b;

function methodA() {}
```

```php
<?php
require_once 'test_a.php';
require_once 'test_b.php';

echo a\methodA();
```