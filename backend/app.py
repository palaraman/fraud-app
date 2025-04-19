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
client = MongoClient("mongodb+srv://perumalnambi7:Arjunking2003@cluster0.dg88to1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
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

if __name__ == '__main__':
    app.run(debug=True)
