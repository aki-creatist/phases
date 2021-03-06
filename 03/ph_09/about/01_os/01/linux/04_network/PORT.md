# ネットワーク

* ネットワークの設定
* ダウンロードやリモート接続

## 備考

* ifconfigコマンドやnetstatコマンドは、CentOS 7からは標準インストールから外された
    * ifconfigコマンドの代わり
        * `ip` コマンドが、
    * netstatコマンドの代わり
        * `ss` コマンドが用意されている
* ifconfigコマンド、netstatコマンドはCentOS 7ではnet-toolsパッケージに含まれている

## ネットワーク情報を確認

* ホストに割り当てられているIPアドレスを確認

### ホストに割り当てられているIPアドレスを確認

* ローカルホスト
    * 利用者が操作中のシステムを
* リモート
    * ネットワークで隔たったホスト

```bash
# Mac
ifconfig
# Cent OS
ip addr
```

* `lo` はローカルホスト (localhost)
    * 自分自身に接続する、ローカルループバックという特殊なネットワークインターフェース
* enpOs3がネットワークインターフェースの名前
    * この名前はシステムによって異なる
    * 以前は「eth0」「eth1」といった名前が広く使われていた

```text
lo0: flags=8049<UP,LOOPBACK,RUNNING,MULTICAST> mtu 16384
        〜中略
        inet 127.0.0.1 netmask 0xff000000 
```

| 項目 | 説明 |
|:----|:----|
| ether | MACアドレス |
| inet | IPアドレス(IPv4) |
| broadcast | ブロードキャストアドレス |
| netmask | サブネットマスク |
| inet6 | IPアドレス(IPv6) |

## ネットワークの疎通確認

* `ping` コマンド
    * ネットワーク経由で別のホストに繋がっているか確認
    * 指定したホストに対して `ICMP` パケットを送信し続け、結果を表示
        * ICMP (Internet Control Message Protocol)
            * エラーメッセージや制御メッセージを伝えるためのプロトコル(通信の取り決め)
    * 反応が返った場合、以下が確認できる
        * 少なくともネットワークが繋がっている
        * 接続先ホストも起動している
    * 反応が返らない場合、以下
        * Destination Host Unreachable (宛先ホストに届きません)のメッセージが出る
        * 主な理由は以下
            * 物理的にネットワークが繋がっていない
            * 途中のファイヤウォールでICMPパケットが遮断されている
            * 宛先ホストが起動していない
            * 宛先ホストのネットワークサービスに問題がある
            * 宛先ホストがpingに応答しないよう設定されている
* ホストにはホスト名かIPアドレスを指定する
* 自分が管理しているホスト以外には安易にpingコマンドを使わない
    * 攻撃の事前調査とみなされてしまう可能性がある

```bash
ping [オプション] ホスト
```

例として自分自身にpingをしてみる

```bash
ping 127.0.0.1
# 終了するには LinuxはCtrl+c、MacはCommand+c
```

## 開いているポートを確認

* `ポート番号`
    * 送信元や送信先のアプリケーションを区別するために使われる番号
    * どんなアプリケーションがどのポート番号を使うか、ということは決められている
        * ポート番号から以下が確認できる
            * ローカルホスト上で動作しているサーバーソフトウェア
            + 通信中のソフトウェア
* 開いているポートはnetstatコマンドで確認
    * `netstat` - Mac と 旧Linux
    * `lsof` - Mac と Linux
    * `ss` - Linux
    * 使い方や表示のさせ方が多数ある
    * MacとLinuxでは挙動が異なる
* サーバーでは、開かれているポートは必要最低限にする
* 不要なポートは閉じる(不要なサービスを終了する)ようにする
    * 不要なポートが開いているとセキュリティ上のリスクが増える
    * ポートを開いているサービスを終了すると、ポートは閉じられる


```bash
## Cent OS
ss [オプション]
## Mac
netstat	[オプション]
```

* オプション
    * `a` - 全てのソケット情報を表示する
    * `n` - アドレスやポートを数字で表示する
    * `t` - TCPポートだけを表示する
    * `u` - UDPポートだけを表示する

例

```bash
# Cent OS
ss -antup
# Mac
netstat -antu
lsof -nP -iTCP
lsof -nP -iTCP -sTCP:LISTEN
```

* 用語
    * `ESTABLISHED`
        * 接続が確立している
    * `LISTEN`
        * ポートを開いて接続を待ち受けている
