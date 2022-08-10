from datetime import datetime 
import pytz
import requests
from xml.etree import ElementTree
import config as cfg

class ExchangeRate():
    exchange_rate = None
    exchange_day = None
    CBR_URL = cfg.CBR_URL
    
    @classmethod
    def set_exchange_rate(cls):
            response = requests.get('?date_req='.join([cls.CBR_URL, cls.exchange_day]))
            tree = ElementTree.fromstring(response.content)
            node = tree.find('.//Valute[@ID="R01235"]/Value').text
            cls.exchange_rate = float(node.replace(',','.'))
            print(f"set_exchange_rate {cls.exchange_rate}") 

    @classmethod
    def check_new_exchange_date(cls):
        return cls.exchange_day!=cls.get_today()

    @classmethod
    def set_exchange_day(cls):
        cls.exchange_day = cls.get_today()

    @classmethod
    def get_today(cls):
        return datetime.now(pytz.timezone('Europe/Moscow')).strftime("%d/%m/%Y")
    
    @classmethod
    def get_exchange_rate(cls):
        if not cls.exchange_rate or cls.check_new_exchange_date():
            cls.set_exchange_day()
            cls.set_exchange_rate()
        return cls.exchange_rate