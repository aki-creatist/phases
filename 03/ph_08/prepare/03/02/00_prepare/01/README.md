# contextの切り替え

```bash
#操作対象のクラスタの確認
kubectl config get-contexts
#切り替え
kubectl config use-context  docker-for-desktop
#ノードの表示
kubectl get node
```