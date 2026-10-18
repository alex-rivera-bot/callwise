import pandas as pd
 
df = pd.read_csv("data/v1_raw.csv", sep=";")
before = len(df)
 
# 1) 删掉打完电话才知道的列（数据泄漏）
df = df.drop(columns=["duration"])
 
# 2) 删掉完全重复的行
df = df.drop_duplicates()
 
# 3) 把 pdays = -1（从没联系过）变成更直观的 0/1 列
df["was_contacted_before"] = (df["pdays"] != -1).astype(int)
 
df.to_csv("data/v2_clean.csv", sep=";", index=False)
 
print("v1 rows:", before)
print("v2 rows:", len(df))
print("v2 columns:", len(df.columns))
print("yes rate:", round((df["y"] == "yes").mean(), 3))
