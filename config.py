import os

DATABASE_CONFIG = {    
    'db_name':'delivery',
    'user': 'postgres',
    'password': 'password',
    'host': 'localhost',
    'port': 5432
}
    
TABLE_CONFIG = {
    'table_name': 'delivery_orders',
    'table_cols': ['id', 'order_num', 'price_d', 'price_ru', 'delivery_time']
}

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

SHEET_ID = 'enter_sheet_id'

CBR_URL = 'https://www.cbr.ru/scripts/XML_daily.asp'

TELEGRAM_BOT_TOKEN = 'bot_token'
TELEGRAM_CHAT_ID = 'chat_id'