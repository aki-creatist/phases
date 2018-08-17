# レジストリサーバを立てる

* [参考](https://qiita.com/rsakao/items/617f54579278173d3c20)
* Docker Hubではなく自分だけのレジストリが欲しい場合はレジストリサーバーをコンテナで立てる

## 準備

* https://hub.docker.com/r/library/registry/tags/

```bash
#レジストリを取得
docker pull registry:2.3.0
#Registryのコンテナをたてる
#docker run -d -p 5000:5000 -v /var/opt:/var/lib/registry registry:2.3.0
docker run -d -p 5000:5000 -v ~/projects/opt:/var/lib/registry registry:2.3.0
```

## push

### TAGをつける

* [参考](https://docs.docker.com/engine/reference/commandline/tag/#tag-an-image-referenced-by-id)

```bash
IMAGE_NAME=dock_web1
IMAGE_TAG=latest
NEW_TAG=version1.1
REGISTRY_IP=localhost
REGISTRY_PORT=5000
REGISTRY_NAME=test
TARGET="${IMAGE_NAME}:${IMAGE_TAG}"
TO=${REGISTRY_IP}:${REGISTRY_PORT}/${REGISTRY_NAME}/${IMAGE_NAME}
docker tag ${TARGET} ${TO}:${NEW_TAG}

#例
#docker tag dock_web1 localhost:5000/web1/dock_web1:version1.0
#タグ削除
docker rmi ${IMAGE_NAME}:${TAG}
```

### Pushする

```bash
docker push ${TO}:${NEW_TAG}
#例
docker push localhost:5000/web1/dock_web1:version1.0
```

## pull

```bash
#削除
docker rmi localhost:5050/test/dock_web1:version1.1
#Pullする
docker pull ${TO}:${NEW_TAG}
#例
#docker pull localhost:5050/test/dock_web1:version1.1
```

## UIで確認

* [参考](https://github.com/kwk/docker-registry-frontend)

```bash
docker run \
  -d \
  -e ENV_DOCKER_REGISTRY_HOST=192.168.0.1 \
  -e ENV_DOCKER_REGISTRY_PORT=5000 \
  -p 8086:80 \
  konradkleine/docker-registry-frontend:v2
```

もしくは以下

```bash
docker-compose up -d registry registryui
```

## 動作確認

```bash
#テスト用のイメージをpull
docker pull hello-world
#タグをつける
docker tag hello-world localhost:5000/hello-world
#DockerレジストリにPush
docker push localhost:5000/hello-world
#確認
curl http://localhost:5000/v2/_catalog
#{"repositories":["hello-world"]} と出力されればok

#削除
docker rmi localhost:5000/hello-world
#pullして見る
docker pull localhost:5000/hello-world

#動作確認が終わったら削除
docker rmi localhost:5000/hello-world
docker rmi hello-world
```