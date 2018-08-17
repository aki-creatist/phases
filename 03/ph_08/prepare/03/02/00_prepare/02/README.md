# ダッシュボードの作成

* https://k-miyake.github.io/blog/docker-k8s-mysql/

```bash
#dashboad用のPodを作
kubectl create -f https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/recommended/kubernetes-dashboard.yaml
#ServiceのtypeをClusterIPからNodePortに変更
kubectl -n kube-system edit service kubernetes-dashboard
```

```yaml
apiVersion: v1
kind: Service
.
.
.
spec:
  clusterIP: 10.108.208.167
  externalTrafficPolicy: Cluster
  ports:
  - nodePort: 32744 # 外部からのアクセス用Port
    port: 443
    protocol: TCP
    targetPort: 8443
  selector:
    k8s-app: kubernetes-dashboard
  sessionAffinity: None
  type: NodePort # typeをNodePortに変更
status:
  loadBalancer: {}
```

* アクセス
    * https://localhost:32744