"""模型本身：概率范围、没有用泄漏特征、结果稳定、极端输入不崩。"""
 
from app.model import load_model, predict_proba
from tests.fixtures import VALID
 
 
def test_probability_is_between_0_and_1():
    p = predict_proba(VALID)
    assert 0.0 <= p <= 1.0
 
 
def test_model_does_not_use_duration():
    model = load_model()
    used = list(model.named_steps["pre"].feature_names_in_)
    assert "duration" not in used
 
 
def test_same_input_same_output():
    a = predict_proba(VALID)
    b = predict_proba(VALID)
    assert abs(a - b) < 1e-9
 
 
def test_extreme_values_do_not_crash():
    row = dict(VALID, balance=-1000000, campaign=100, pdays=-1)
    p = predict_proba(row)
    assert 0.0 <= p <= 1.0
