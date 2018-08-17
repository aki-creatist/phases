# service.yaml作成と起動

## service.yaml作成

```yaml
# service.yaml
kind: Service
apiVersion: v1
metadata:
  name: http-service
  labels:
    app: http-app
spec:
  selector:
    app: http-app
  ports:
    - port: 8080
      targetPort: http-port
  type: LoadBalancer
```

### service.yamlの起動

```bash
#createコマンドで先程作成したManifestfileを指定して起動
kubectl create -f service.yaml
#まとめて書くこともできる
#kubectl create -f service.yaml -f pod.yaml
```
