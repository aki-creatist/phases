# Stringクラス

* 概要
* コンストラクタ
* 主なメソッド
* 文字列長取得メソッド
* 比較メソッド
* 検索・置換メソッド
* 抽象メソッド
* 変換メソッド
* 基本型などから文字列への変換メソッド

## 概要

* Stringクラスのメソッドの中には、文字列をあたかも加工しているように振る舞うものもある
* しかしそれは文字列そのものを加工しているのではなく、指定の加工を行った`新たな文字列`を作成しているのであり、元の文字列は変化していない
* 文字列に対する`+`演算子は、文字列を連結する
* たとえば"12"+"34"の結果は"1234"この場合でも結果の"1234"は新たな文字列で、"12"や"34"が変化したわけではない

## コンストラクタ

* オブジェクトを使用する際は、本来は以下のように『呼び出す』という手順がある

```text
new オブジェクト("生成したい文字列");
```

* String`(String original)`
    * originalと同じ内容の文字列を新たに生成する
        * 引数: original:元となる文字列

しかし、通常は、プログラム中で文字列リテラルを使用すると、`その時点でインスタンスが生成`される

このため、コンストラクタを明示的に呼び出すことは`ほとんどない`の

以下のような命令がある

## 主なメソッド

## 文字列長取得メソッド

* int length()
    * 自身の文字列の長さ(文字列)を数える
    * 戻り値: 文字数

文字列の長さはアルファベットや漢字などの文字種によらずどんな文字種であっても、１文字につき１と数える

## 比較メソッド

* bolean equals(object another)
    * 自身とanotherが等しい文字列かどうか判断する
        * 引数: another:比較対象オブジェクト
        * 戻り値: 自身の文字列anotherが等し場合trueそうでなければfalse

文字列どうしを比較する場合は、`equels()`を利用する`==`演算子を用いると、インスタンスが同じかどうかを比べることにより、文字列の内容を比較することにはなる

*  `str1==str2`
    * true(等しい)
* `str1.equels(str2)`
    * true(等しい)
* `str1==str2`
    * false(異なる)
* `str1.equals(str2)`
    * true(等しい)
* [SampleString01](SampleString01.txt)
* 関連メソッド:equals
    * 文字列を線形検索する
    * 名前を格納する配列namesと住所を配列addressを用意し、tanakaさんを探索して住所を表示する
* `int compareTo(String anotherString)`
    * 自身とanotherを自書式に比較する
    * 引数: anotherString:比較対象の文字列
    * 戻り値
        * 負の整数
            * 自身がanotherStringよりも自書式に小さいとき
        * 0
            * 自身とanotherStringと等しいとき
        * 正の整数
            * 自身とanotherStringよりも自書式に大きいとき
* `compareTo()`は、文字列の大小をUnicodeの順番で自書式に判定する
* Unicodeでは、文字は`0～9、A～Z、a～z、平仮名、片仮名、漢字`の順に大きくなる
* 例: "America"、"August"、"apple"は、一般の辞書順では、
    * `Amerika<apple<August`が、`compareTo()`(Unicode順)では、`America<August<apple`と判定されるので注意

```text
if(str.compareTo(another) < 0){
    // str < anotherの場合の処理
}
else if(str.compareTo(another) > 0){
    // str > anotherの場合の処理
}else{
    // str = anotherの場合の処理
}
```

* `boolean matches(String regex)`
    * 自身がregexの正規表現に一致するかどうかを判定する
    * 引数: regex:比較対象を表す正規表現
    * 戻り値: 自身がregexの正規表現と一致する場合、真
    * 例外: PatternSyntaxException:regexの表現に誤りがある場合

正規表現は文字列パターンを記述する表現で、文字列の検索などに用いられる`matches()`は指定された正規表現に自身が一致するかどうかを調べる

これらのほかにも、次のメソッドがある

* `boolean equalsIgnoreCase(String another)`
    * 大文字小文字を区別せず、同じかどうかを判定
* `int compareToIgnoreCase(String another)`
    * 大文字小文字を区別せず、自書式に比較
* `boolean startWith(String prefix)`
    * prefixで始まるかどうかを判定
* `boolean startWith(String prefix,int toffset)`
    * toffsetの位置からprefixで始まるかどうかを判定
* `boolean endWith(String suffix)`
    * suffixで終わるかどうかを判定

## 検索・置換メソッド

検索・置換メソッドからは文字列内の位置(インデックス)という概念が登場する特に断らない限り、位置は`先頭文字を0`として数えた値を意味する

* `int indexOf(int ch)`
    * 自身から、chを検索する
    * 引数: ch:検索文字
    * 戻り値: chが最初に見つかった位置を返す見つからなかったときは-1を返す
* `String replace(charSequence target, CharSequece replacement)`
    * すべてのtargetをreplacementで置き換えた文字列を生成する
    * 引数: target:置換される文字列
    * replacement:置き換わる文字列
    * 戻り値: 置き換えた文字列
    * 例外: NullPointerException:targetまたはreplacementがnullの場合

※CharSequeceは固定/可変を問わない文字列型で、StringやStringBufferなどを含む

文字列の置換は、対象文字列を置き換えるのではなく、痴漢した新たな文字列を生成する元の文字列は最初の状態から変化しない

* [SampleString02](SampleString02.txt)
    * 関連メソッド:replace
    * "きゃく"を"客"に置換して表示する
* `int indexOf(int ch, intfromIndex)`
* int inexOf(String str)* 
* int lastIndexOf(int ch)* 
* int indexOf(String str, int fromIndex)* 
* int lastIndexOf(int str)* 
* int lastIndexOf(int ch, int fromIndex)* 
* int lastIndexOf(String str)* 
* String replaceAll(String regex, String replacement* 
* String replaceFirst(String regex, String replacement)* 

## 抽象メソッド

* `char charAt(int index)`
    * indexの位置にある一文字を返す
    * 引数: index:文字の位置
    * 戻り値: indexの位置にある文字
    * 例外: IndexOutOfBoundsException:indexの値が文字列の範囲外の場合

文字の抽出は、文字列からインデックスの位置にある文字を返す

* [SampleString03](SampleString03.txt)
    * 関連メソッド:length, charAt
    * 文字列(HELLO)を`縦表示`する
* String[] split(string regex)
    * regexで指定された正規表現に一致する位置で分割する
    * 引数: regex:区切りとなる鵜正規表現
    * 戻り値: regexで分割した文字列の配列
    * 例外: PatternSyntaxException:regexの正規表現に誤りがある場合

`split()`による抽出では、正規表現に一致する文字を区切りとして分割した文字列を生成する

* String substring(int beginIndex, int endIndex
    * 自身の文字列から、beginIndexから始まりendIndexの直前で終わる範囲のぶ武運文字列を生成する
    * 引数: beginIndex:文字列の開始位置
    * endIndex:文字列の終了位置(この位置は部分文字列に含まれない)
    * 戻り値: 指定した部分文字列
    * 例外: IndexOutOfBoundsException:beginIndex、endIndexが文字列の範囲外か、beginIndexがendIndexより大きい場合

`substring()`による抽出では、範囲を指定して部分文字列を生成する終了位置の文字れは含まれないので注意

これらのほかにも、次のメソッドがある

* String substring(int beginIndex)
    * beginIndexの位置から始まる部分文字列を抽出
* String trim()
    * 前後の空白を取り除いた部分文字列を抽出
* [SampleString04](SampleString04.txt)
    * 関連メソッド:indexOf、substring
    * メールアドレスからユーザ名(@以前)を切り出し、それぞれ表示する

## 変換メソッド

* static String format(String format, Object...args)
    * argsをformatの初期に従って編集し、文字列を生成する
    * 引数: format:書式文字列
    * args:書式文字列の書式指示詞に対応する引数の並び
    * 戻り値: 編集した文字列
    * 例外: IlliegalFormatException:formatの書式とargsの指定に誤りがある場合
        * NullPointerException:formatがnullの場合

`Object...args`はargsが連続することを表す

* String toLowerCase()
    * 自身を小文字に変換する
    * 戻り値: 小文字に変換した文字列
* String toUpperCase()
    * 自身を大文字に変換する
    * 戻り値: 大文字に変換した文字列

## 基本型などから文字列への変換メソッド

整数や実数などの基本型の値を文字列に変換するためには、空文字列との加算(連結)を行うのが一般的

なお、次のメソッドを用いて明示的に変換することも可能

* static String valueOf(object obj)
    * objの文字列表現を返する
    * 引数: obj:対象のオブジェクト
    * 戻り値: objの文字列表現objがnullの場合は、文字列"null"

すべての基本型に対応した`valueOf()`が用意されている

byte型やshort型はint型で対応する

* static String valueOf(int i)
    * int型を文字列に変換する
* static String valueOf(boolean b)
    * bookean型を"true"または"false"に変換する
* static String valueOf(double d)
    * double型を文字列に変換
* static String valueOf(float f)
    * float型を文字列に変換
* static String valueOf(long l)
    * long型の文字列に変換

objがあるクラスのインスタンスである場合は、そのクラスの`toString()`の結果を返却する