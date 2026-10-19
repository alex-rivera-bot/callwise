# CallWise — 电话营销认购预测

输入一位客户的信息，预测他会不会认购定期存款，帮业务决定"要不要打这通电话"。

## 快速开始

    pip install -r requirements-dev.txt
    python ml/train.py
    uvicorn app.main:app --reload

打开 http://127.0.0.1:8000/docs 试用。

## 项目结构

    app/                 接口与模型加载
    ml/train.py          训练脚本（调用 MLflow）
    ml/data_pipeline.py  数据清洗 v1 → v2
    ml/models/           训练产物
    ml/README_*.md       数据说明与实验记录
    tests/               3 个测试文件
    data/                DVC 指针（原始数据在 Azure）

## Docker

    docker build -t callwise:latest .
    docker run -p 8000:8000 callwise:latest

## 数据

两版数据用 DVC 管理，原始数据在 Azure 上，Git 里只有指针：

    dvc pull

- v1：原始数据（含 duration）
- v2：去掉 duration（泄漏列）、去重、新增 was_contacted_before

## 分支策略

feature/* → dev → staging → main

## CI/CD

- PR 到 dev / staging / main → CI：ruff 检查 + pytest 全量测试 + docker build
- push 到 staging → CD：用 STAGING_ENV 生成 .env，构建 callwise:staging
- push 到 main → CD：用 PROD_ENV 生成 .env，构建 callwise:main
- CI 不通过时 PR 无法合并（分支保护已开启）

## 实验

两次实验见 ml/README_experiments.md，当前生产模型见 ml/registry/current_model.md。
