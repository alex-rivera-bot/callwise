import json
import os
import pickle
import subprocess
 
import mlflow
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
 
CAT_COLS = ["job", "marital", "education", "default",
            "housing", "loan", "contact", "month", "poutcome"]
NUM_COLS = ["age", "balance", "day", "campaign",
            "pdays", "previous", "was_contacted_before"]
FEATURES = CAT_COLS + NUM_COLS
 
CONFIG_PATH = "ml/configs/train.json"
with open(CONFIG_PATH, encoding="utf-8") as f:
    CONFIG = json.load(f)
 
 
def git_commit():
    try:
        out = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
        return out.decode().strip()
    except Exception:
        return "unknown"
 
 
def data_version(path="data/v2_clean.csv.dvc"):
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                if "md5:" in line:
                    return line.split("md5:")[1].strip()
    except FileNotFoundError:
        return "unknown"
    return "unknown"
 
 
def build_model(which, params):
    pre = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), CAT_COLS),
        ("num", StandardScaler(), NUM_COLS),
    ])
    if which == "lr":
        clf = LogisticRegression(max_iter=1000, class_weight="balanced",
                                 random_state=42, C=params.get("C", 1.0))
    else:
        clf = RandomForestClassifier(
            n_estimators=params.get("n_estimators", 200),
            max_depth=params.get("max_depth", 12),
            min_samples_leaf=5, class_weight="balanced",
            random_state=42, n_jobs=-1)
    return Pipeline([("pre", pre), ("model", clf)])
 
 
def evaluate(model, X_test, y_test):
    proba = model.predict_proba(X_test)[:, 1]
    pred = (proba >= 0.5).astype(int)
    return {"pr_auc": float(average_precision_score(y_test, proba)),
            "f1": float(f1_score(y_test, pred, zero_division=0))}
 
 
def run_experiment(name, which, params, X_train, X_test, y_train, y_test):
    with mlflow.start_run(run_name=name):
        for k, v in params.items():
            mlflow.log_param(k, v)
        mlflow.log_param("git_commit", git_commit())
        mlflow.log_param("data_version", data_version())
 
        model = build_model(which, params)
        model.fit(X_train, y_train)
        metrics = evaluate(model, X_test, y_test)
        mlflow.log_metric("pr_auc", metrics["pr_auc"])
        mlflow.log_metric("f1", metrics["f1"])
 
        os.makedirs("ml/models", exist_ok=True)
        path = f"ml/models/{name}.pkl"
        with open(path, "wb") as f:
            pickle.dump(model, f)
        mlflow.log_artifact(path)
 
    print(name, "pr_auc=", round(metrics["pr_auc"], 4),
          "f1=", round(metrics["f1"], 4))
    return metrics
 
 
def main():
    df = pd.read_csv("data/v2_clean.csv", sep=";")
    y = (df["y"] == "yes").astype(int)
    X = df[FEATURES].copy()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)
 
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("callwise")
 
    m1 = run_experiment("run1-baseline-lr", "lr", CONFIG["baseline"],
                        X_train, X_test, y_train, y_test)
    m2 = run_experiment("run2-improved-rf", "rf", CONFIG["improved"],
                        X_train, X_test, y_train, y_test)
 
    if m1["pr_auc"] >= m2["pr_auc"]:
        best = "run1-baseline-lr"
    else:
        best = "run2-improved-rf"
 
    with open(f"ml/models/{best}.pkl", "rb") as src:
        with open("ml/models/model.pkl", "wb") as dst:
            dst.write(src.read())
    print("best:", best, "-> ml/models/model.pkl")
 
 
if __name__ == "__main__":
    main()
