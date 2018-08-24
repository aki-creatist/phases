# タグ

## タグをつける

```bash
touch sample.txt
git add .
git commit "will tag"
git tag v0.1
git tag
git checkout v0.1
git checkout master
```

```bash
#メッセージを記入する
git tag -a Version-0.1
#メッセージ付きでタグ一覧を表示する
git tag -n
#メッセージを10行まで表示させながらタグ一覧を表示する
git tag -n10
#特定のファイルのみ表示する
git tag -l -n10 Version-0.1
#git showでも代用可能
git show Version-0.1
#Vertionで始まるタグを全て表示する
git tag -l -n10 Version*
```

```bash
git push origin Version-0.1
pushされた側でgit pull
git tag
#全てのタグをアップロードする ただし不要なタグまでアップロードするのはご法度
git push —tags
#不要にアップロードしたタグを削除する
git push origin :Version-0.1
#ローカルの不要になったタグを削除する
git tag -d Version-0.1
```

