# 实验记录

## run1-baseline-lr

- 模型：LogisticRegression(C=1.0, class_weight=balanced)
- 数据：v2
- pr_auc：0.4001659810453086
- f1：0.3784702549575071
- run id：10830ca53d4e41beb0d6969085d79e27

## run2-improved-rf

- 模型：RandomForest(n_estimators=200, max_depth=12)
- 数据：v2
- pr_auc：0.43688933402326174
- f1：0.44572984008166044
- run id：fe769cd131f14ea6a809c0a93c332fbb

## 生产模型

选择 run2-improved-rf，因为它的 PR-AUC 更高，说明在同样的误报水平下能抓出更多真正会认购的客户。

## 为什么以 PR-AUC 为主指标

只有约 11% 的客户会认购，属于类别不平衡。如果只看准确率，全部预测"不买"也能有 88%，
但一个客户都抓不到，对业务毫无价值。PR-AUC 关注"少数类抓得准不准、全不全"，更贴近
实际决策；f1 作为辅助，在阈值 0.5 下衡量精确率与召回率的平衡。
