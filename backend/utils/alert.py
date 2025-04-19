def send_alerts(data):
    try:
        import telegram
        bot = telegram.Bot(token='YOUR_TELEGRAM_BOT_TOKEN')
        bot.send_message(chat_id='YOUR_CHAT_ID', text=f"FRAUD DETECTED:\\nUser: {data['user_id']}\\nAmount: ${data['amount']}\\nLocation: {data['location']}")
    except Exception as e:
        print("Telegram alert failed:", e)
