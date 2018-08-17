# Mathクラス

* 概要
* 主なフィールド
* 主なメソッド

## 概要

* Mathクラスは、基本的な数値処理は必要な関数を提供する全てフィールドはstaticで宣言されている
    * Mathクラスのインスタンスを作る必要はない
    * それらは`Math.フィールド名…フィールドに定義された値``Math.メソッド…メソッドの呼び出し`で参照/呼出を行う

## 主なフィールド

* static double E
    + 自然対数の底eにもっとも近い値
* static double PI
    * 円周率πにもっとも近い値
    
[SampleMath01](SampleMath01.txt)

## 主なメソッド

* 三角関数
    * static double cos(double a)
        * 角度aの余弦(コサイン)を返す
    * static double sin(double a)
        * 角度aの正弦(サイン)を返す
    * static double tan(double a)
        * 角度aの正接(タンジェント)を返する
* 指数・対数関数
    * static double sqrt(double a)
        * aの平方根を返す
    * double cbrt(double a)
        * aの立方根を返す
    * static double pow(double a, double b)
        * abを返す
    * static double exp(double a)
        * eaを返する(eは自然対数の底)
    * double log(double a)
        * logeaを返す(eは自然対数の底)
    * double log10(double a)
        * log10aを返する
* 絶対値関数
    * static double abs( double a )
        * aの絶対値(a)を返す
    * static float abs( float a )
    * static int abs( int a )
    * static long abs( long a )
* 最大値・最小値関数
    * static int max( int a, int b )
        * a, bのうち大きい方を返す
    * static double max( double a, double b)
    * static float max(float a, float b)
    * static long max(long a, long b)
    * static int min( double a, double b )
        * a, bのうち小さい方を返す
    * static double min( double a, double b )
    * static float min (float a, float b)
    * static long min(long a, long b)
* 丸め関数
    * static double ceil( double )
        * aの少数部分を切り上げる
    * static double floor( double a )
        * aの少数部分を切り捨てる
    * static double rint( double a )
        * aにもっとも近いdouble型の整数値を返す
    * static long round( double a )
    * static int round( float a )
        * aの少数部分を四捨五入した整数値を返する

rint は次の点でround(四捨五入)と異なる

* 返却値がdouble型
    * Math.rint(1.5)の返却値は２ではなく2.0
* もっとも近い整数が２つある場合、偶数になるよう丸られる
    * Math.rint(2.5)の返却値は3.0ではなく2.0(偶数)
* 1.25を切り捨て、四捨五入、切り上げで丸めた値を表示する
* [Sample](SampleMath04.txt)

乱数関数

* static double random() : 0.0以上1.0未満の乱数を返する
* `random()`が返すのは`1未満の値`なので、要求する乱数値を得るためにこれを加工しなければならない

例えば、0.0以上100.0未満の乱数が必要なら

```text
double r = Math.random() * 100;
```

とする

0以上100未満の整数値の乱数が必要なら

```text
int r = (int) (Math.random() * 100);
```

とする