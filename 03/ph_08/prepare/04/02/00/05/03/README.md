# Doubleクラス

* 主なフィールド
* コンストラクタ
* 主なメソッド

Doubleクラスは、double型に対応するラッパークラスコンストラクタやメソッドの役割は、型の違いを除けばIntegerクラスと変わりない

## 主なフィールド

* static double MAX_VALUE: doubleで表現可能な最大値
* static double MIN_VALUE: doubleで表現可能な最小値

## コンストラクタ

* Double(double value): valueをラップしたオブジェクトを生成する
* Double(String s): sが表す実数値をラップしたオブジェクトを生成する

## 主なメソッド

* int compareTo(Double anotherDouble)
    * 自身とanotherDoubleを比較する
* boolean equals(Object another)
    * 自身とanotherを比較する
* sattic double parseDouble(String s)
    * 文字列sを実数に変換する
* String toString()
    * 自身がラップする実数値の文字列形式を返する
* static String toString( double d )
    * 実数dの文字列形式を返する
* double doubleValue()
    * 自身がラップする実数値を返する
* static Double valueOf( double d )
    * 実数dをラップするDouble型のオブジェクトを返する