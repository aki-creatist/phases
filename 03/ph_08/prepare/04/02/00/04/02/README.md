# Randomクラス

* 概要
* コンストラクタ
* メソッド

## 概要

* Randomクラスは乱数の発生に用いられる乱数はMathクラスの`random()`でも発生可能し、通常であればその方がよほど簡単
* ただし、様々な方の乱数を発生させたい場合や、シミュレーションなどの要請で正規分布に従う乱数を使いたい場合に、Randomクラスを用いることがある
* Randomクラスのメソッドはstaticではない
* そのため、メソッドを使うためにはRamdomクラスのインスタンスを生成しなければならない
* このインスタンスは乱数ジェネレータと呼ばれる
* いわば乱数の発生装置最初に乱数ジェネレータを作る
    * 後はそこから次々と乱数を引っ張ってくることが可能
* int 型の乱数が欲しければ`"次"はint型でお願い`と依頼するだけRandomクラスのメソッド名が"nextXXX"となっているのは、この理由

## コンストラクタ

*  Random() : 新規乱数ジェネレータを生成する
*  Random() : long型のシードを使って乱数ジェネレータを生成する

シードは乱数の種(seed)で、種の等しい乱数ジェネレータは同じ順序で生成する

* [Sample](SampleRandom01.txt)

## メソッド

| メソッド | 説明 |
|:----|:----|
| boolean nextBoolean() : boolean型の乱数を返する |
| double nextDouble() : 0.0以上1.0未満のdouble型の乱数を返する |
| float nextFloat() : 0.0以上1.0未満のfloat型の乱数を返する |
| int nextInt() : int型の乱数を返する |
| long nextLong() : long型の関数を返する |
| int nextInt( int n ) | 0〜nの範囲(nは含まない)でint型の乱数を返する |
| void nextBytes( byte[] bytes ) | byte型の乱数を生成し、引数の配列にセットする |
| double nextGaussian() : 平均0.0、標準偏差1.0の正規分布に従う乱数を返する |
| void setSeed( long seed ) | 乱数ジェネレータのシードを設定する |