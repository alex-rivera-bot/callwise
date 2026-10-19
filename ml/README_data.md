# 数据说明

## 来源

UCI Machine Learning Repository — Bank Marketing
https://archive.ics.uci.edu/dataset/222/bank+marketing
文件：bank-full.csv，45,211 行 × 17 列，葡萄牙某银行电话营销记录。

## v1（原始版）

- 文件：data/v1_raw.csv
- 行数：45211
- 提交：b0d04e6
- DVC 标签：v1-data

## v2（清洗版）

- 文件：data/v2_clean.csv
- 行数：45195
- 改动：
  1. 删除 duration 列——它只有打完电话才知道，属于数据泄漏
  2. 删除完全重复的行
  3. 新增 was_contacted_before 列（pdays != -1）
- 提交：55fe43a
- DVC 标签：v2-data
- DVC md5：c80e7619f7efc4d645acafe6f604c072

## 复现

    dvc pull
    python ml/data_pipeline.py
