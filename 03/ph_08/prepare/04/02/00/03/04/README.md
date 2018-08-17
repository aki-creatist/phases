# 独自例外を作る

* プログラム特有の独自例外を使うことも可能
* これを使うためには、独自の例外クラスを用意しなければならない独自例外は、通常はExceptionクラスを拡張して作成する
* ただし、非チェック例外を作成したい場合はRuntimeExceptionクラスを拡張する
* [SampleException05](SampleException05.txt)