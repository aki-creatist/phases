# ログ操作

* [参考](https://qiita.com/bezeklik/items/f5c292c4360cde140bef)

```bash
LOG_FILE=xxx.gz
# 全リクエスト数/日
zcat ${LOG_FILE} | awk '$9==200{print $NF/1000, $7}' | wc -l
# 3秒以上のリクエスト数/日
zcat ${LOG_FILE} | awk '$9==200 && $NF >=3000000{print $NF/1000, $7'} | wc -l
# 転送量(30日)
zcat ${LOG_FILE} | awk '$9==200{TRAFFIC += $10}END{print TRAFFIC/1024/1024/1024*30}'
```

```bash
grep 01/Feb/2016:01 ${LOG_FILE} | awk -F '"' '{print $2}' | awk '{print $2}' | sort | uniq -c | sort -n -r
```

```bash
#アクセスログ一覧を取得
SERVER=IPまたはHost名
ssh ${SERVER} 'ls /var/log/rsyslog/httpd/app-web/api/'
LOG_FILE=調査したいログ.gz
scp ${SERVER}:/var/log/rsyslog/httpd/app-web/api/${LOG_FILE} ./
gzcat ${LOG_FILE} | awk -F '"' '{print $2}' | awk '{print $2}' | sort | uniq -c | sort -n -r
```

