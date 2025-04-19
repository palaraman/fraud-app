import os
import sys

# ⛔ Disable GPU (to avoid CUDA errors in cloud environments)
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# ✅ Hide TensorFlow info messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# ✅ Add current directory to sys.path so 'utils' can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from tensorflow.keras.models import load_model
from pymongo import MongoClient
import datetime

from utils.alert import send_alerts
from utils.gps_blocker import block_location
from utils.sms_alert import send_sms
from utils.captcha import verify_captcha

app = Flask(__name__)
CORS(app)

model = load_model("model/fraud_model.h5")
client = MongoClient("your-mongodb-connection-string")
db = client['fraud_detection']
transactions = db['transactions']

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    if not verify_captcha(data.get("captcha_token")):
        return jsonify({"error": "CAPTCHA failed"}), 403

    features = np.array(data["features"]).reshape(1, 1, -1)
    prediction = model.predict(features)[0][0]
    is_fraud = prediction > 0.5

    record = {
        "user_id": data["user_id"],
        "features": data["features"],
        "amount": data["amount"],
        "location": data["location"],
        "confidence": float(prediction),
        "is_fraud": is_fraud,
        "timestamp": datetime.datetime.now()
    }
    transactions.insert_one(record)

    if is_fraud:
        send_alerts(record)
        send_sms(record)
        block_location(record["location"])

    return jsonify({"fraud": is_fraud, "confidence": float(prediction)})

@app.route("/transactions/<user_id>", methods=["GET"])
def get_user_transactions(user_id):
    user_transactions = list(transactions.find({"user_id": user_id}))
    for tx in user_transactions:
        tx["_id"] = str(tx["_id"])
    return jsonify(user_transactions)

@app.route("/download/<user_id>", methods=["GET"])
def download_csv(user_id):
    import csv
    from io import StringIO
    records = list(transactions.find({"user_id": user_id}))
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(records[0].keys())
    for row in records:
        writer.writerow(row.values())
    return output.getvalue(), 200, {'Content-Type': 'text/csv'}

# 🔽 This will run send_alerts for testing when the app starts
test_record = {
    "user_id": "test_user",
    "features": [0.1, 0.2, 0.3],
    "amount": 100.0,
    "location": "Chennai",
    "confidence": 0.95,
    "is_fraud": True,
    "timestamp": datetime.datetime.now()
}
send_alerts(test_record)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
