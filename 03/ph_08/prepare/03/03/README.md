# GitLabサーバーとGitLab Runnerを連携する

```bash
#起動
docker-compose up -d gitlab
```

## RunnerのRegistration tokenを確認する

* http://localhost:10080/test/gitlab-ci-demo/settings/ci_cd
* プロジェクトを選択
    * `Settings` - サイドバー
        * `CI / CD` - サイドバー
            * `Runners settings`をExpand

