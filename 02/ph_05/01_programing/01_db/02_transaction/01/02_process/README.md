# プロセス

プロセスはスレッドよりも独立性が高い

* プロセスを起動するのもスレッドと同じような理由
    * 複雑なスレッドプログラムを開発する必要もない
    * 仮にプロセスに問題が発生したとしても、他のプロセスに影響を与えることはない
* ただしスレッドプールのスレッドを使うよりもプロセスの起動には時間がかかる

