# 数据与模型溯源

| 环节 | 产物 | 对应版本 |
|---|---|---|
| 原始数据 | data/v1_raw.csv | DVC 标签 v1-data |
| 清洗数据 | data/v2_clean.csv | DVC 标签 v2-data，md5 c80e7619f7efc4d645acafe6f604c072 |
| 训练代码 | ml/train.py | git 55fe43a |
| 实验记录 | MLflow run | run id fe769cd131f14ea6a809c0a93c332fbb |
| 模型文件 | ml/models/model.pkl | 来自 run2-improved-rf |
| 服务 | app/ | Docker 镜像 callwise:latest |
