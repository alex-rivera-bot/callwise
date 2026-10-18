import os
 
from fastapi import FastAPI
from pydantic import BaseModel, Field
 
from app.model import MODEL_PATH, predict_proba
 
# 阈值：概率大于等于它才值得打电话，可用环境变量改
THRESHOLD = float(os.environ.get("THRESHOLD", "0.5"))
 
app = FastAPI(title="CallWise", version="1.0")
 
 
class Customer(BaseModel):
    age: int = Field(ge=18, le=100)
    job: str
    marital: str
    education: str
    default: str
    balance: int
    housing: str
    loan: str
    contact: str
    day: int = Field(ge=1, le=31)
    month: str
    campaign: int = Field(ge=1, le=100)
    pdays: int
    previous: int = Field(ge=0)
    poutcome: str
 
 
@app.get("/health")
def health():
    return {"status": "ok"}
 
 
@app.get("/model-info")
def model_info():
    return {"model_path": MODEL_PATH, "threshold": THRESHOLD}
 
 
@app.post("/predict")
def predict(customer: Customer):
    probability = predict_proba(customer.model_dump())
    decision = "call" if probability >= THRESHOLD else "skip"
    return {
        "probability": round(probability, 4),
        "decision": decision,
        "threshold": THRESHOLD,
    }
