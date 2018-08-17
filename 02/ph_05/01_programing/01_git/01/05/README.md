# コミットをまとめる

```bash
#rebaseSquashブランチを作成する
git branch rebaseSquash
#ブランチが生成できたことを確認する
git branch
#ブランチを移動する
git checkout rebaseSquash
```

## rebaseSquash ブランチ

```bash
#ブランチが移動していることを確認する
git branch
git log —oneline
```

```text
f56574b(HEAD) add Fx CC()
2501611 add Fx BB()
795341c add Fx AA()
```

```bash
#合体したいコミットの２つ前を指定する
#add Fx CC()とadd Fx BB()を合体したいので、add Fx AA()のIDを指定する
git rebase -i 795341c
```

```text
pick 2501611 add Fx BB()
pick f56574b add Fx CC()
```

* 新しい方(下)のpickを書き換える
    * pickをsに書き換え

```text
pick 2501611 add Fx BB()
s f56574b add Fx CC()
```

* エディタが再度開く
    * 保存して終了
    
```text
Successfully rebased and updated refs/heads/rebaseSquash
```

```bash
#コミットがまとめられていることを確認する
git log —oneline
#マスターブランチに戻る
git checkout master
```

## master ブランチ

```bash
#マスターブランチに戻ったことを確認する
git branch
```