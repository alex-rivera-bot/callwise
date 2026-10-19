# 部署说明

## 触发规则

| 事件 | 工作流 | 做什么 |
|---|---|---|
| PR → dev / staging / main | CI | ruff 检查、pytest 全量测试、docker build |
| push → staging | CD | 用 STAGING_ENV 生成 .env，构建 callwise:staging |
| push → main | CD | 用 PROD_ENV 生成 .env，构建 callwise:main |

## 完整流程

commit → push feature 分支 → 向 dev 提 PR → CI 通过 → 合并进 dev
→ 向 staging 提 PR → 合并 → CD 构建 staging 镜像
→ 向 main 提 PR → 合并 → CD 构建 main 镜像

## Secrets

- STAGING_ENV：staging 环境变量，内容形如 APP_ENV=staging
- PROD_ENV：生产环境变量，内容形如 APP_ENV=prod

真实值只保存在 GitHub Secrets 中，不写入仓库。

## 说明

本作业不要求真实部署，CD 阶段只构建 Docker 镜像，不上传到服务器。
