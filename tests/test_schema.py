"""接口输入校验：缺字段、类型错、越界、多余字段、没见过的类别。"""
 
from fastapi.testclient import TestClient

from app.main import app
from tests.fixtures import VALID

client = TestClient(app)
 
 
def test_valid_payload_returns_200():
    r = client.post("/predict", json=VALID)
    assert r.status_code == 200
 
 
def test_missing_field_returns_422():
    bad = dict(VALID)
    del bad["job"]
    assert client.post("/predict", json=bad).status_code == 422
 
 
def test_wrong_type_returns_422():
    bad = dict(VALID, age="not-a-number")
    assert client.post("/predict", json=bad).status_code == 422
 
 
def test_age_out_of_range_returns_422():
    bad = dict(VALID, age=200)
    assert client.post("/predict", json=bad).status_code == 422
 
 
def test_extra_field_is_ignored():
    bad = dict(VALID, duration=999)
    assert client.post("/predict", json=bad).status_code == 200
 
 
def test_unknown_category_still_works():
    bad = dict(VALID, job="astronaut")
    assert client.post("/predict", json=bad).status_code == 200
