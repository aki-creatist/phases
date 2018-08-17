# Curry化

* 関数の部分実行のための方法を提供する点でバインドと関連している
* 引数のプレフイルだけを行うという点でバインドとは異なる

## thisの値を設定しない

* 関数やメソッドの暗黙のthisを維持しながら、これらに引数をバインド可能
* この暗黙のthisのおかげで、Curry化を使えば、オブジェクトのプロトタイプの関数に引数をバインドしつつ、与えられたオブジェクトをthis値として関数を実行可能

## テストの記述

* [test/curry_test.js](test/curry_test.js)
* `Function.prototype.curry`を使用
    * `String.prototype.replace`から`String.prototype.trim`を実装する
* Curryに引数が渡されないときの最適化はないが、それは引数なしでcurryを呼び出しても無意味であり、避けるべき

## 実装

* [src/curry.js](src/curry.js)