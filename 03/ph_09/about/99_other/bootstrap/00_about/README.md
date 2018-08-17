# 概要

* Webサイトのフロントエンドツール
* CSSフレームワークの一種

## 特徴

* グリッドレイアウトを基本としている
* 豊富なUIコンポーネントが用意されている
* レスポンスデザインがサポートされている
    * 様々なデバイスに最適化したWebサイトを一つのソースコードで実現する手法
    * CSS3の`media query`という技術を使って、解像度に合わせて異なるデザインを定義している

## 使用方法

基本的なHTMLタグに対して用意された「class」を指定する

## その他CSSフレームワーク

* Foudation (http://foundation.zurb.com/)
* UIKit (http://www.getuikit.com)
* Pure (http://purecss.jp)
* Kube (http://imperavi.com/kube/)
* HTML Kickstart (http://www.99lime.com/)

## サポートするブラウザ

* Chrome (Mac、Windows、iOS、Android)
* Safari
* Firefox (Mac、Windows)
* Internet (8以上)
* Opera (Mac、Windows)

## IE8 (またはそれ以下)の場合
   
* `IE8`は、`CSS3`や`media query`をサポートしていない
    * レスポンシブ・デザインに対応するために、`respond.js`を読み込みが必要
* `<head>`タグ内に読み込みを記述

```html
<!--[if lt IE 9]>
    <script src="{respond.jsのパス}/respond.min.js"></script>
<! [endif]-->
<meta http-equiv="X-UA-Compatible" content="IE=edge">
```

## Bootstrapの構成

* bootstrap.cssがBootstrapの本体となるCSSファイル
* bootstrap.jsは、インタラクティブなUIを実現するためのJSで、必要に応じて読み込む
    * min: 圧縮版
        * 本番用
    * minなし: 非圧縮版
        * 開発用
* fonts/: フォルダ以下には、bootstrapで使うアイコンが配置されている
