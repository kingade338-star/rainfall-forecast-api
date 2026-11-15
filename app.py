# app.py
import json, logging, math, time
from fastapi import FastAPI, HTTPException

logging.basicConfig(filename="requests.log", level=logging.INFO,
                    format="%(message)s")
app = FastAPI(title="Rainfall forecast API")

# ---- load once at start-up, not per request ----
MODEL_JSON = '{"version": "1", "features": ["month", "temp_c", "humidity"], "weights": [0.05, 0.02, 0.04], "bias": -3.0}'
FEATURES = ["month", "temp_c", "humidity"]

def load_model(s, expected_features):
    m = json.loads(s)
    if m.get("version") != "1" or m["features"] != expected_features:
        raise ValueError("model version or features mismatch")
    def predict(rows):
        return [1 / (1 + math.exp(-(m["bias"] + sum(w * r[f] for w, f in zip(m["weights"], m["features"])))))
                for r in rows]
    return predict

predict = load_model(MODEL_JSON, FEATURES)

# ---- validator from challenge 95 ----
def validate(payload):
    errors = []
    is_int = lambda v: isinstance(v, int) and not isinstance(v, bool)
    is_num = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
    if not isinstance(payload.get("lga"), str) or not payload["lga"].strip():
        errors.append("lga must be a non-empty string")
    m = payload.get("month")
    if not is_int(m) or not 1 <= m <= 12:
        errors.append("month must be an integer from 1 to 12")
    t = payload.get("temp_c")
    if not is_num(t) or not -10 <= t <= 60:
        errors.append("temp_c must be a number from -10 to 60")
    h = payload.get("humidity")
    if not is_num(h) or not 0 <= h <= 100:
        errors.append("humidity must be a number from 0 to 100")
    return len(errors) == 0, errors

@app.post("/predict")
def predict_rain(payload: dict):
    ok, errors = validate(payload)
    if not ok:
        raise HTTPException(status_code=422, detail=errors)
    p = predict([payload])[0]
    # log time, inputs and prediction (no personal data, only the area name)
    logging.info(json.dumps({"time": time.time(),
                             "inputs": {k: payload[k] for k in ("lga", "month", "temp_c", "humidity")},
                             "prediction": round(p, 4)}))
    return {"rain_probability": round(p, 4)}