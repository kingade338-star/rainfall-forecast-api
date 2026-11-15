# Rainfall forecast API

Predicts the probability of rain for an Oyo State area from month,
temperature and humidity.

## Run
pip install fastapi uvicorn
python -m uvicorn app:app --reload

## Example request
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"lga": "Ibadan North", "month": 6, "temp_c": 27.5, "humidity": 81}'

Response: {"rain_probability": 0.4...}

## Bad input
{"lga": "", "month": 13, "temp_c": "hot", "humidity": 250}
returns HTTP 422 with one message per bad field.

## Limits
- Trained on a small dataset; not a replacement for official forecasts.
- Only covers Oyo State and the temperature range -10 to 60 C.
- Does not use wind, pressure or satellite data.
- Probabilities are not calibrated and should not guide safety decisions.
- The weights are placeholders, so the probabilities are for demonstration only.

## Logging
Each request's time, inputs and prediction go to requests.log.
No names, phone numbers or other personal data are stored.