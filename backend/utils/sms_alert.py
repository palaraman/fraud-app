from twilio.rest import Client

def send_sms(data):
    try:
        client = Client("TWILIO_SID", "TWILIO_AUTH_TOKEN")
        msg = f"ALERT: Fraud detected for {data['user_id']} at {data['location']}."
        client.messages.create(body=msg, from_="+1234567890", to="+recipient_number")
    except Exception as e:
        print("SMS failed:", e)
