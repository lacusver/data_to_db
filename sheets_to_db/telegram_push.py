import telegram
import config as cfg


class TelegramBot():
    tel_bot = None
    @classmethod
    def init_bot(cls):
        if cls.tel_bot is None:
            cls.tel_bot = telegram.Bot(token=cfg.TELEGRAM_BOT_TOKEN)

    @classmethod
    def send_message(cls, message):
        try:
            cls.init_bot()
            cls.tel_bot.send_message(chat_id = cfg.TELEGRAM_CHAT_ID, text = message)
        except Exception as e:
            print(f"Telegram error: {e}")
