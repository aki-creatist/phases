# Smarty

## Install

```bash
git clone https://github.com/aki-creatist/docker_article.git
mv docker_article dock
cd dock
docker-compose up -d
cd ../var/www/
mkdir app
cd app
composer require smarty/smarty
mkdir templates
mkdir templates_c
chmod 777 templates_c
touch index.php
touch templates/header.tpl
touch templates/index.tpl
```

## html/index.php

```php
<?php
require_once '../app/init.php';

$smarty->assign('hello', 'Hello, Smarty!!');
$smarty->assign('today', new DateTime());
$smarty->assign('animal', array('rabbit','cat','dog'));

$smarty->display('index.tpl');
```

## app/templates/header.tpl

```html
<!DOCTYPE html>
<meta charset="utf-8">
<title> {$page_title} </title>
```

## app/init.php

```php
<?php
define('ROOT_DIR', __DIR__ );

require_once ROOT_DIR . '/vendor/autoload.php';


ini_set('date.timezone', 'Asia/Tokyo');
define('MY_TITLE', 'TEST');

$smarty = new Smarty();

// 使うテンプレートが入っているディレクトリを指定
$smarty->setTemplateDir(ROOT_DIR . '/templates/')
    ->setCompileDir(ROOT_DIR . '/templates_c');
```

## app/templates/index.tpl

```html
{*
  コメントアウト
*}

{include file='header.tpl' page_title={$smarty.const.MY_TITLE}}

{* 普通の変数 *}
<p>{$hello}

    {* メソッド *}
<p>{$today->format('Y/m/d (D)')}

    {* 予約変数 *}
<dl>
    <dt>現在のタイムスタンプ
    <dd>{$smarty.now}

    <dt>現在処理中のテンプレートファイル名
    <dd>{$smarty.template}

    <dt>Smarty version
    <dd>{$smarty.version}
</dl>

{* 配列を逆順でループ(step=-1だから) *}
<ul>
    {section name=i loop=$animal step=-1}
    <li>{$animal[i]}
        {/section}
</ul>
```
