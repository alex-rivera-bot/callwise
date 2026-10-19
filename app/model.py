import os
import pickle
 
import pandas as pd
 
MODEL_PATH = os.environ.get("MODEL_PATH", "ml/models/model.pkl")
 
_model = None
 
 
def load_model():
    global _model
    if _model is None:
        with open(MODEL_PATH, "rb") as f:
            _model = pickle.load(f)
    return _model
 
 
def predict_proba(record: dict) -> float:
    model = load_model()
    row = dict(record)
    # 从 pdays 自动推出"以前联系过没有"，保证和训练时一致
    row["was_contacted_before"] = int(row["pdays"] != -1)
    frame = pd.DataFrame([row])
    return float(model.predict_proba(frame)[0][1])
