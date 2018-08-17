# ネットワーク設定

* 設定を変更するには設定ファイルを編集
* 設定方法は、ティストリビューションによって大きく異なる
* システム設定の多くに設定ファイルが使われる
    * 設定ファイルはテキストファイル
    * 設定ファイルを編集することで設定が変更される
* 設定ファイルの変更にはroot権限が必要
* 設定ファイルを閲覧するだけなら一般ユーザーでも可能

今回は、Red Hat系ディストリビューションが対象

## ネットワークインターフェースの設定ファイル

* ネットワークインターフェースの設定ファイル
    * `/etc/sysconfig/network-scripts/` 配下
* ファイルの命名規則
    * ネットワークインターフェースの名前が「enp0s3」である場合
        * 設定ファイル名は、`/etc/sysconfig/network-scripts/ifcfg-enp0s3`となる
        * このファイルでは「設定項目名＝値」という形式で設定を記述
            * `＝` の前後に空白なし
* ホストには固有のIPアドレスが割り当てられる

| 設定項目 | 説明 |
|:----|:----|
| TYPE | ネットワークタイプ |
| BOOTPROTO | staticなら固定IPアドレス、chcpならDHCPを利用する |
| NAME | ネットワークインターフェースの名前 |
| ONBOOT | yesならこのネットワークインターフェースをシステム起動時に有効にする |
| IPADDR | IPアドレス |
| NETMASK | サブネットマスク |
| GATEWAY | デフォルトゲートウェイ |

### 割り当てるIPアドレスがあらかじめ決まっている場合

次のようにしてIPアドレスを設定する

```bash
cat /etc/sysconfig/network-scripts/ifcfg-inp0s3
BOOTPROTO=static
IPADDR=192.168.100.100
NETMASK=255.255.255.0
GATEWAY=192.168.100.254
```

### DHCPサービスを使ってIPアドレスを自動割り当てにしている場合

* `DHCP`
    * `Dynamic Host Configuration Protocol`
    * IPアドレスなどのネットワーク設定を自動的に割り当てるプロトコル

設定は以下のようになる

```text
cat /etc/sysconfig/network-scripts/ifcfg-inp0s3
BOOTPROTO=dhcp
```

### ファイルの内容を変更した場合

ネットワークサービスの再起動が必要

```bash
sudo system restart network.service
```

## NetworkManager

* CentOS 7で使ってネットワークを管理に推奨されているツール
* 有線ネットワーク・無線ネットワークを問わず、ネットワークを検知して動的にシステム設定を行う
    * スムーズにネットワークに接続することができる
    * NetworkManagerの管理コマンド
        * `nmtui` コマンド
        * `nmcli` コマンド

## DNSの設定ファイル

* `DNS`
    * Domain Name Service
    * `名前解決` をするサービス
        * ホスト名に対応するIPアドレスを検索
        * IPアドレスからホスト名を割り出す
    * どのDNSサーバーを利用するか、という情報は、`/etc/resolv.conf`に格納されている
        * nameserver行にDNSサーバーのIPアドレスが記される
            * 一般的なユーザーが利用するDNSサーバーは、インターネットプロバイダーなどが提供
            * `8.8.8.8`は、Google社が提供しているオープンなDNSサーバー
        * このファイルは、DHCP接続をしていると自動的に書き換えられる
        * nameserver行は複数設定することができます
            * 必要があれば追加
        * 上の方に書かれたDNSサーバーから順に問い合わせを行う
        * DHCPを利用している場合は、DHCPによって自動的に設定が更新される
            * NetworkManagerによって自動的に更新される

```bash
cat /etc/resolv.conf
nameserver 8.8.8.8
nameserver 192.168.11.1
```
