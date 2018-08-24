# クローンとプル

```bash
mkdir git_practice
mkdir local friend
```

* git bashをもう一枚開く

```bash
#local
cd local
#friend
cd friend
#local
git init 
ls -al
echo "local01" > sample.txt
git add .
git commit -m "local01"
git log
#friend
git clone ../local .
ls -al
git log
echo "friend01" >> sample.txt
git add .
git commit -m "friend01"
git log
#local
git pull ../friend/
git log
```