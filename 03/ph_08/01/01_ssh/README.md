# 鍵の管理

## 構築

* [環境作成](provisioning.sh)
    * ディレクトリ作成
    * 設定ファイル作成
* 鍵の作成
* 構成

## 鍵の作成

```bash
#GIT
DIR=keys/commons
cd ${DIR}
ssh-keygen -t rsa
chmod 600 ${DIR}/git
cat ${DIR}/git.pub #公開鍵をGitに登録

#Jenkins
DIR=keys/local
cd ${DIR}
ssh-keygen -t rsa
chmod 600 ${DIR}/jenkins
```

## 構成

* `config`
    * 鍵を設定ファイルを読み込み
* `conf.d/`
    * 鍵の場所を指定
* `keys`
    * `commons/git`
        * ソースコード管理用
    * `local/jenkins`
        * コンテナ間のSSH用
    * `servers`
        * 外部のサーバに接続するid_rsaなど

```text
.
├── conf.d
│   ├── commons
│   │   └── git.conf
│   ├── local
│   └── servers
├── config
└── keys
    ├── commons
    │   ├── git
    │   └── git.pub
    ├── local
    │   ├── jenkins
    │   └── jenkins.pub
    └── servers
```