# HTTPアクセス

* [pod.yaml作成と起動](01)
* [service.yaml作成と起動](02)

## 確認

```bash
#起動確認
kubectl get all
#疎通確認
curl localhost:8080
```

## 削除

```bash
kubectl delete svc http-service
```

## podの詳細

```bash
kubectl describe pods ${ポッド名}
```