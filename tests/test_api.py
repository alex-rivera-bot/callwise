"""接口行为：健康检查、返回字段、阈值真的会改变结论。"""
 
import app.main as main_module
from app.main import app
from app.model import predict_proba
from fastapi.testclient import TestClient
from tests.fixtures import VALID
 
client = TestClient(app)
 
 
def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
 
 
def test_predict_returns_three_fields():
    body = client.post("/predict", json=VALID).json()
    assert set(body) == {"probability", "decision", "threshold"}
 
 
def test_threshold_boundary(monkeypatch):
    p = predict_proba(VALID)
    monkeypatch.setattr(main_module, "THRESHOLD", p - 1e-6)
    assert client.post("/predict", json=VALID).json()["decision"] == "call"

    monkeypatch.setattr(main_module, "THRESHOLD", p + 1e-6)
    assert client.post("/predict", json=VALID).json()["decision"] == "skip"
 
 
def test_threshold_boundary_counts_as_call(monkeypatch):
    monkeypatch.setattr(main_module, "THRESHOLD", predict_proba(VALID))
    assert client.post("/predict", json=VALID).json()["decision"] == "call"
