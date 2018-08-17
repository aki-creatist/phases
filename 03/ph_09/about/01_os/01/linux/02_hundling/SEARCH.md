# 検索

## ファイル内検索

* `grep`
    * ファイル内から特定の文字列が含まれる行を検索し標準出力
* `egrep`
    * grepの機能拡張版 (拡張正規表現が使用可能)
* `fgrep`
    * マッチさせたい文字列が多いときに効果を発揮

### オプション

* `-E`: grepに付与するとegrepになる
* `i`: 大文字小文字を区別しない
* `--color=auto`: 結果を色付きにする

### grepとegrep

```bash
echo -e "abc\nABC\n123" > grep_test.txt
grep grep '^(1|a)' grep_test.txt # 結果なし
egrep '^(1|a)' grep_test.txt # ヒットする
```

### grepとfgrep

時間を計測すると `fgrep` の方が高速

```bash
ls -l /usr/share/dict/words # 英単語がリストアップされているファイル
time grep 'impossible' /usr/share/dict/words
time fgrep 'impossible' /usr/share/dict/words # 高速
```
