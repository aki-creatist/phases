# Threadクラス

* 概要
* 主なコンストラクタ
* 主なメソッド

## 概要

* Treadクラスは、プログラムをマルチスレッドで実行するための基本機能を提供する
* マルチスレッドで動作するプログラムは、Threadクラスを拡張するか、Treadクラスと連携していなければならない

## 主なコンストラクタ

* Thread()
    * 新しいスレッドを作成する

新しいスレッドを作成するこのスレッドは、`start()`が呼び出されるまで実行を開始しない

* Thread(Runnable target)
    * targetのプログラムを実行する新しいスレッドを作成する
    * Runnableインターフェースを実装したクラス

targetと連携する新しいスレッドを作成するマルチスレッドで実行するプログラム(`run()`)は、target側のクラスに用意する

## 主なメソッド

* void start()
    * スレッドの実行を開始する
    * スレッドの実行を開始する具体的にはスレッドが起動され、`run()`に記述された処理を実行する
* static void sleep(long m) throws InterruptedException
    * スレッドの実行をmミリ秒間停止する
    * スレッドの実行をmミリ秒間停止(スリープ)するmミリ秒経過後、スレッドは実行を再開する
* final void join() throws InterruptedException
    * スレッドの終了を待ち合わせる
    * このメソッドは、親スレッド(スレッドを起動した側)のプログラムから呼び出される
    * 親スレッドは、joinを呼び出したスレッドが終了するまで、実行を停止する

[java_08](image/java_08.png)

[Sample](SampleThread01.txt)
    
* final void join(long m) throws InterruptedException
    * スレッドの終了を最大mミリ秒間待ち合わせする
    * 待ち合わせるスレッドが終了していない場合でも、mミリ秒間が経過すると親スレッドの実行を再開する
    * スレッドに割り込んだり、割り込みを受けたかどうかを調べるために次のメソッドを使うことが可能
*  void interrupt()
    * スレッドに割り込む
* static boolean interrupted()
    * スレッドが割り込みを受けているかどうかを調べる
* boolean isInterrupted()
    * スレッドが割り込みを受けているかどうかを調べる