import requests

def verify_captcha(token):
    secret = "YOUR_RECAPTCHA_SECRET_KEY"
    resp = requests.post("https://www.google.com/recaptcha/api/siteverify", data={
        'secret': secret,
        'response': token
    })
    return resp.json().get("success", False)
