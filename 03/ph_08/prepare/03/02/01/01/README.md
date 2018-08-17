# pod.yaml作成と起動

* http://blue1st-tech.hateblo.jp/entry/2018/01/06/162306

## pod.yaml作成

```yaml
# pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: http
  labels:
    app: http-app
spec:
  containers:
    - name: nginx
      image: nginx:latest
      ports:
        - name: http-port
          containerPort: 80
      volumeMounts:
        - name: docroot
          mountPath: ./html
  volumes:
    - name: docroot
      hostPath:
        path: /Users/a_nakanishi/Documents/develop/dock # 作業ディレクトリ
```

## 起動

```bash
kubectl create -f pod.yaml
```
