# ユーザ管理

* ユーザー情報は/etc/passwdファイルに記録される
* ユーザーのパスワードは、/etc/shadowファイルに暗号化されて格納される
* ユーザーは、ユーザーに割り当てられた固有の数値であるUIDによって区別される
* `id` コマンド
    * UIDを確認
* 全てのユーザーは１つ以上のグループに所属
* `groups` コマンド
    * ユーザーが所属しているグループを確認

## ユーザー管理の仕組み

* ユーザーアカウントを作成すると、ユーザー情報は `etc/passwd` に記録される
    * １ユーザーにつき１行で情報が格納されている
* パスワードは `/etc/shadow` に記録されている
    * 暗号化されて格納される
    * rootユーザーだけが閲覧可能
    * １ユーザーにつき１行で情報が格納されている

## UIDを確認

* `id` コマンド
    * UIDを確認する
    * `UID`
        * ユーザーに割り当てられた固有の数値
    * 表示される情報は以下
        * UID
        * ユーザー名
        * プライマリグループのGID
        * グループ名
        * 所属グループ名
        
```bash
id [ユーザー名] # ユーザー名を省略すると、自分自身の情報が表示される
uid=1000(student) gid=1000(student) groups=1000(student) # この例では、studentユーザーのUIDは1000
```

### ユーザーの種類によってUIDは変わる

それぞれのユーザーとUIDの対応

| ユーザ | UID |
|:----|:----|
| 管理者ユーザー | 0 |
| システムユーザー | 1〜99 |
| 一般ユーザー | 100以上 |

* rootユーザーのUIDは必ず0
* 1〜99のUIDハシステムユーザー
* 100以上はUIDは通常、一般ユーザーとして使われる
    * CentOSなど多くのディストリビューションでは、1000以上のUIDが使われる

## 所属しているグループを確認

* グループ
    * 複数のユーザーをまとめて管理する仕組み
    * グループ単位でアクセス権を管理することができる
        * グループAに所属しているユーザーはこのファイルを閲覧できるetc
    * Linuxでは、全てのユーザーはいずれかのグループに所属しなければならない
    * 複数のグループに所属することも可能
    * `id` コマンドでも調べられる
    * ユーザーを指定せずにgroupsコマンドを実行
        * groupsコマンドを実行したユーザーが所属するグループの一覧が表示
    * ユーザーのUIDと同様、グループにも固有の番号であるGID (グループID)がある
        
```bash
groups [ユーザー名]
```

### プライマリグループ

* ユーザーを作成するとそのユーザー名と同じ名前のグループが自動的に作成される
    * ユーザーのプライマリグループとして設定される
        * プライマリグループ ＝ 基本グループ
        * セカンダリグループ
            * プライマリグループ以外に所属するグループ




