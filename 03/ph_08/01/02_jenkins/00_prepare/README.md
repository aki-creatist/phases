# 準備

* [Host OS](01)
* Local/Jenkins環境を用意

```bash
GIT=git@github.com
USER=aki-creatist
REPOSITORY=projects
git clone ${GIT}:${USER}/${REPOSITORY}.git
cd ${REPOSITORY}

JENKINS="doc/jenkins"
mkdir -p ${JENKINS}
git clone ${GIT}:jenkinsci/docker.git ${JENKINS}

docker-compose up -d

ALIAS_JENKINS="alias jenkins='docker exec -it jenkins bash'"
echo ${ALIAS_JENKINS} >> ~/.bashrc
source ~/.bashrc
#コンテナ内に入る
jenkins

ALIAS_JENKINS="alias jenkins='docker exec -it web1 bash'"
echo ${ALIAS_JENKINS} >> ~/.bashrc
source ~/.bashrc
#コンテナ内に入る
web1
```
